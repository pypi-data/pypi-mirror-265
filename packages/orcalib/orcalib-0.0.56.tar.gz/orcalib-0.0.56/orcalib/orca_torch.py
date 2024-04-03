import logging
import time
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Any, Callable, NamedTuple, Optional, cast
from uuid import UUID

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from orca_common import ColumnName
from torch import Tensor
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from orcalib.batched_scan_result import BatchedScanResult
from orcalib.client import OrcaClient
from orcalib.data_classes import VectorScanResult
from orcalib.database import OrcaDatabase
from orcalib.index_handle import IndexHandle
from orcalib.orca_expr import ColumnHandle
from orcalib.orca_types import OrcaTypeHandle
from orcalib.table import TableHandle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class CurateRunInfo:
    run_ids: list[int]
    model_id: str
    model_version: Optional[str]
    batch_size: int
    tags: list[str]
    metadata: dict[str, Any]
    seq_id: Optional[UUID]


# TODO: Consider making this a metaclass instead
def OrcaModel(  # noqa: C901
    db: OrcaDatabase,
    model_id: Optional[str] = None,
    model_version: Optional[str] = None,
    tags: Optional[list[str]] = None,
    metadata: Optional[dict[str, Any]] = None,
    **module_settings_override: Any,
) -> Callable[[nn.Module], nn.Module]:
    """A decorator that enables Orca on a PyTorch model.

    Primary purpose is attaching a database to the model, but it also supports applying various settings, notably: enabling curate tracking.

    :param db: (OrcaDatabase) The OrcaDatabase instance to be used for this model.
    :param model_id: (Optional[str]) The ID (aka name) of the model to be curated. (default: None)
    :param model_version: (Optional[str]) A version string of the model being run. (e.g., "v1.0.0") (default: None)
    :param tags: (Optional[list[str]]) A list of tags to be added to the model run. (e.g., ["production", "v1"]) (default: None)
    :param metadata: (Optional[dict[str, Any]]) A dictionary of metadata to be added to the model run. (default: None)
    :param module_settings_override: (Any) Any additional settings to be applied to the model.

    Example usage:
    .. code-block:: python

            import torch
            from orcalib import OrcaModel

            @OrcaModel(db, model_id="my_model", model_version="v1", tags=["production"])
            class MyModel(torch.nn.Module):
                def __init__(self):
                    super().__init__()
                    self.linear = torch.nn.Linear(10, 10)

                def forward(self, x):
                    return self.linear(x)

            model = MyModel()
            model.init_curate(batch_size=32)
            model.enable_curate()
            model.disable_curate()
            model.disable_memory()
            model.enable_memory()
            model.last_curate_run_info()
    """
    _batch_size: Optional[int] = None
    _seq_id: Optional[UUID] = None

    _model_id: Optional[str] = model_id
    _model_version: Optional[str] = model_version
    _tags: list[str] = tags or []
    _metadata: dict[str, Any] = metadata or {}
    _latest_run_ids: Optional[list[int]] = None

    def memory_setting_passthrough(inst: nn.Module, enable: bool) -> None:
        """
        A passthrough function to enable/disable memory access for the model and all its children.
        :param inst: A PyTorch model instance.
        :param enable: Whether to enable or disable memory access.
        """
        for child in inst.children():
            child._orca_memory_toggle(enable)  # type: ignore

    # TODO: this will break in weird ways if someone is monkey patching a model after instantiation (an edge case we can live with for now)
    def build_layer_names(inst: nn.Module, root_name: Optional[str] = None) -> None:
        """
        Builds layer names for the model and all its children.
        :param inst: A PyTorch model instance.
        :param root_name: The name of the root layer. (default: None)
        """
        if isinstance(inst, OrcaModule):
            inst.set_curate_layer_name(root_name)
        for name, child in inst.named_children():
            build_layer_names(
                child,
                f"{root_name + '.' if root_name is not None else ''}{name}",
            )

    def apply_global_settings(inst: nn.Module, module_settings_override: dict[str, Any]) -> None:
        """
        Applies global settings to the model and all its children.
        :param inst: A PyTorch model instance.
        :param module_settings_override: The settings to be applied to the model.
        """
        if isinstance(inst, OrcaModule):
            inst.apply_orca_settings(**module_settings_override)
        for child in inst.children():
            apply_global_settings(child, module_settings_override)

    def post_init(inst: nn.Module) -> None:
        """
        Post-initialization function to attach the database to the model and all its children.
        :param inst: A PyTorch model instance.
        """
        if isinstance(inst, OrcaModule):
            inst._orca_db_instance = db
        if not hasattr(inst, "_orca_memory_toggle"):
            inst._orca_memory_toggle = memory_setting_passthrough  # type: ignore
        for child in inst.children():
            post_init(child)

    def enable_memory(inst: nn.Module) -> None:
        """
        Enables memory access for the model and all its children.
        :param inst: A PyTorch model instance.
        """
        inst._orca_memory_toggle(inst, True)  # type: ignore

    def disable_memory(inst: nn.Module) -> None:
        """
        Disables memory access for the model and all its children.
        :param inst: A PyTorch model instance.
        """
        inst._orca_memory_toggle(inst, False)  # type: ignore

    def is_curate_enabled_anywhere(inst: nn.Module) -> bool:
        """
        Checks if curate tracking is enabled anywhere in the model or its children.
        :param inst: A PyTorch model instance.
        :return: Whether curate tracking is enabled anywhere in the model or its children.
        """
        if isinstance(inst, OrcaModule) and inst._curate_enabled:
            return True
        for child in inst.children():
            if is_curate_enabled_anywhere(child):
                return True
        return False

    def set_run_ids(inst: nn.Module, run_ids: list[int]) -> None:
        """
        Sets the run IDs for the model and all its children.
        :param inst: A PyTorch model instance.
        :param run_ids: The run IDs to be set.
        """
        if isinstance(inst, OrcaModule):
            inst.set_curate_run_ids(run_ids)
        for child in inst.children():
            set_run_ids(child, run_ids)

    def try_infer_batch_size(*args: Any, **kwargs: Any) -> Optional[int]:
        """
        Attempts to infer the batch size from the model's input arguments.
        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :return: The inferred batch size.
        """
        for arg in args:
            if isinstance(arg, torch.Tensor) and len(arg.shape) > 1:
                return arg.shape[0]
        for kwarg in kwargs.values():
            if isinstance(kwarg, torch.Tensor) and len(kwarg.shape) > 1:
                return kwarg.shape[0]
        return None

    def decorator(cls) -> nn.Module:
        """
        The decorator function that wraps the model class.
        :param cls: The model class to be wrapped.
        :return: The wrapped model class.
        """
        old_init = cls.__init__
        old_forward = cls.forward

        def wrapped_init(self, *args, **kwargs) -> None:
            """
            The wrapped init function that initializes the model and applies global settings.
            :param args: The positional arguments.
            :param kwargs: The keyword arguments.
            """
            old_init(self, *args, **kwargs)
            post_init(self)
            build_layer_names(self)
            apply_global_settings(self, module_settings_override)

        def init_curate(
            self,
            model_id: Optional[str] = None,
            model_version: Optional[str] = None,
            new_tags: Optional[list[str]] = None,
            extra_tags: Optional[list[str]] = None,
            new_metadata: Optional[dict[str, Any]] = None,
            extra_metadata: Optional[dict[str, Any]] = None,
            batch_size: Optional[int] = None,
            seq_id: Optional[UUID] = None,
        ) -> None:
            """
            Initializes the curation process for a model.

            :param model_id: (Optional[str]) The ID (aka name) of the model to be curated. (default: None)
            :param model_version: (Optional[str]) The version of the model being run. (e.g., "v1.0.0") (default: None)
            :param new_tags: (Optional[list[str]]) A list of new tags to be added to the model run (replacing existing tags). (default: None)
            :param extra_tags: (Optional[list[str]]) A list of additional tags to be added to the model run. (default: None)
            :param new_metadata: (Optional[dict[str, Any]]) A dictionary of new metadata to be added to the model. (default: None)
            :param extra_metadata: (Optional[dict[str, Any]]) A dictionary of additional metadata to be added to the model run. (default: None)
            :param batch_size: (Optional[int]) The batch size to be used for the model forward pass. (default: None)
            :param seq_id: (Optional[UUID]) The sequence ID to be used for the model (for sequence models). (default: None)
            """
            nonlocal _model_id
            nonlocal _model_version
            nonlocal _tags
            nonlocal _metadata
            nonlocal _batch_size
            nonlocal _seq_id
            if model_id is not None:
                _model_id = model_id
            if model_version is not None:
                _model_version = model_version
            if new_tags is not None:
                _tags = new_tags
            if extra_tags is not None:
                if _tags is None:
                    _tags = []
                _tags.extend(extra_tags)
            if new_metadata is not None:
                _metadata = new_metadata
            if extra_metadata is not None:
                _metadata.update(extra_metadata)
            if batch_size is not None:
                _batch_size = batch_size
            if seq_id is not None:
                _seq_id = seq_id

        def last_curate_run_info(self) -> CurateRunInfo:
            """
            Returns the information of the last curate run on the model.
            """
            assert (
                _model_id is not None and _batch_size is not None and _latest_run_ids is not None
            ), "It seems there is no last curate run on this model"
            return CurateRunInfo(
                run_ids=_latest_run_ids,
                model_id=_model_id,
                model_version=_model_version,
                batch_size=_batch_size,
                tags=_tags,
                metadata=_metadata,
                seq_id=_seq_id,
            )

        def record_curate_scores(self, scores: list[float] | float) -> None:
            """
            Records the scores of the last curate run on the model.
            :param scores: The scores to be recorded.
            """
            assert _latest_run_ids is not None, "It seems there is no last curate run on this model"
            if isinstance(scores, float):
                scores = [scores]
            assert isinstance(scores, list)
            assert len(scores) == len(_latest_run_ids), "Number of scores must match number of run IDs"
            db.record_model_scores(_latest_run_ids, scores)

        def record_model_input_output(self, inputs: list[Any] | Any, outputs: list[Any] | Any) -> None:
            """
            Records the inputs and outputs of the last curate run on the model.
            :param inputs: The inputs to be recorded.
            :param outputs: The outputs to be recorded.
            """
            assert _latest_run_ids is not None, "It seems there is no last curate run on this model"
            if not isinstance(inputs, list):
                inputs = [inputs]
            if not isinstance(outputs, list):
                outputs = [outputs]
            assert (
                len(inputs) == len(outputs) == len(_latest_run_ids)
            ), f"Inputs/Outputs not of the correct size (got {len(inputs)}, {len(outputs)}, expected {len(_latest_run_ids)})"
            db.record_model_input_output(_latest_run_ids, inputs, outputs)

        def wrapped_forward(self: nn.Module, *args, **kwargs) -> Any:
            """
            The wrapped forward function that enables Curate tracking.
            :param self: A PyTorch model instance.
            :param args: The positional arguments.
            :param kwargs: The keyword arguments.
            :return: The output of the model's forward pass.
            """
            if is_curate_enabled_anywhere(self):
                nonlocal _batch_size
                if _batch_size is None:
                    _batch_size = try_infer_batch_size(*args, **kwargs)
                    if _batch_size is None:
                        raise ValueError(
                            "Batch size could not be inferred. Please set batch size manually via init_curate."
                        )
                assert (
                    _model_id is not None
                ), "Model ID must be set when Curate tracking is enabled. Please set in decorator or via init_curate."
                run_ids = OrcaClient.init_forward_pass(
                    db_name=db.name,
                    model_id=_model_id,
                    model_version=_model_version,
                    batch_size=_batch_size,
                    tags=_tags,
                    metadata=_metadata,
                    seq_id=_seq_id,
                )
                nonlocal _latest_run_ids
                _latest_run_ids = run_ids
                set_run_ids(self, run_ids)
            return old_forward(self, *args, **kwargs)

        cls.__init__ = wrapped_init
        cls.forward = wrapped_forward
        cls.enable_memory = enable_memory
        cls.disable_memory = disable_memory
        cls.init_curate = init_curate
        cls.last_curate_run_info = last_curate_run_info
        cls.record_curate_scores = record_curate_scores
        cls.record_model_input_output = record_model_input_output

        return cls

    return decorator


########################
### Orca PyTorch Layers
########################
class OrcaModule(nn.Module, ABC):
    """Parent Class for all Orca Modules to handle all global settings (e.g. enable/disable curate tracking)

    This currently only operates with the Curate database; it does not handle memory access with a memory database (attached via a separate decorator).

    Example usage:
    .. code-block:: python

            import torch
            from orcalib import OrcaModule

            class MyModule(OrcaModule):
                def __init__(self):
                    super().__init__()
                    self.linear = torch.nn.Linear(10, 10)

                def forward(self, x):
                    return self.linear(x)

            model = MyModel()
            model.init_curate(batch_size=32)
            model.enable_curate()
            model.disable_curate()
            model.disable_memory()
            model.enable_memory()
            model.last_curate_run_info()
    """

    # TODO: enable/disable memory access should move here from the decorator

    def __init__(self, **settings):
        """
        :param settings: Additional settings to be applied to the module.
        """
        super().__init__()
        self._orca_db_instance: Optional[OrcaDatabase] = None
        self.apply_orca_settings(**settings)

    def apply_orca_settings(
        self,
        curate_enabled: bool = False,
        orca_db_instance: Optional[OrcaDatabase] = None,
        curate_layer_name: Optional[str] = None,
    ) -> None:
        """
        Applies global settings to the module.
        :param curate_enabled: Whether curate tracking is enabled. (default: False)
        :param orca_db_instance: The OrcaDatabase instance to be used for this module. (default: None)
        :param curate_layer_name: The name of the layer to be used for curate tracking. (default: None)
        """
        self._curate_enabled = curate_enabled
        if orca_db_instance is not None:
            self._orca_db_instance = orca_db_instance
        if curate_layer_name is not None:
            self._layer_name = curate_layer_name

    def _set_curate_enabled(self, enabled: bool) -> None:
        """
        Sets the curate tracking status for the module and all its children.
        :param enabled: Whether curate tracking is enabled.

        NOTE: This method should not be called directly. It is used internally.
        """
        self._curate_enabled = enabled

        def set_curate_enable_for_children(root: nn.Module) -> None:
            """
            Sets the curate tracking status for the module and all its children.
            :param root: The root module.
            """
            for child in root.children():
                if isinstance(child, OrcaModule):
                    child._set_curate_enabled(enabled)
                else:
                    set_curate_enable_for_children(child)

        set_curate_enable_for_children(self)

    def enable_curate(self) -> None:
        """
        Enables curate tracking for the module and all its children.
        """
        self._set_curate_enabled(True)

    def disable_curate(self) -> None:
        """
        Disables curate tracking for the module and all its children.
        """
        self._set_curate_enabled(False)

    def set_curate_layer_name(self, name: Optional[str]) -> None:
        """
        Sets the name of the layer for curate tracking.
        :param name: The name of the layer.
        """
        self._layer_name = name

    def set_curate_run_ids(self, run_ids: list[int]) -> None:
        """
        Sets the run IDs for the module and all its children.
        :param run_ids: The run IDs to be set.
        """
        self._run_ids = run_ids


class _LinearClassificationHead(OrcaModule):
    """A 2-Layer linear classification head generally used for a transformer model.
    Example usage:
        .. code-block:: python

                import torch
                from orcalib import OrcaModule, _LinearClassificationHead

                class MyModule(OrcaModule):
                    def __init__(self):
                        super().__init__()
                        self.linear = torch.nn.Linear(10, 10)
                        self.classifier = _LinearClassificationHead(10, 5)

                    def forward(self, x):
                        x = self.linear(x)
                        x = self.classifier(x)
                        return x

                model = MyModel()
    """

    def __init__(
        self,
        model_dim: int,
        num_labels: int,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_labels: (int) The size of the output vector.
        :param activation: (Callable[[Tensor], Tensor]) The activation function to be used between the two linear layers. (default: F.relu)
        :param dropout: (float) The dropout rate to be used between the two linear layers. (default: 0.1)
        """
        super().__init__()

        self.activation = activation

        self.linear1 = nn.Linear(model_dim, model_dim)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(model_dim, num_labels)

    def forward(self, x) -> torch.Tensor:
        """
        Performs a forward pass through the linear classification head.
        :param x: The input tensor.
        :return: The output tensor.
        """
        x = self.linear1(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = self.linear2(x)
        return x


class OrcaLookupType(NamedTuple):
    """
    A dataclass that represents the type of lookup to be performed in an OrcaDatabase index.
    """

    index_type: OrcaTypeHandle
    return_column_types: tuple[OrcaTypeHandle, ...]


@dataclass(slots=True)
class OrcaLookupConfig:
    """
    A dataclass that represents the configuration for looking up in an OrcaDatabase index.
    """

    orca_db_name: str
    index_name: str
    lookup_column_names: tuple[ColumnName, ...]
    num_memories: int

    def __eq__(self, other):
        if not isinstance(other, OrcaLookupConfig):
            return False
        my_db_name = self.orca_db_name
        other_db_name = other.orca_db_name
        return (
            my_db_name == other_db_name
            and self.index_name == other.index_name
            and self.lookup_column_names == other.lookup_column_names
            and self.num_memories == other.num_memories
        )

    def __hash__(self):
        return hash((self.orca_db_name, self.index_name, self.lookup_column_names, self.num_memories))


class OrcaGenericLookupLayer(OrcaModule):
    """
    A generic layer that instantiates a OrcaLookupType, and allows
    for swapping of a OrcaLookupConfig for looking up in an OrcaDatabase index and returning the top k results,
    based on the OrcaLookupType.

    Currently this is only being used by the ChatBot Demo. A larger refactor is needed to change all interfaces
    here and in all demos currently using OrcaLookupLayer. The merge should be fairly clean, with the only
    larger issue being that the interface in user-land will change to use OrcaLookupType and OrcaLookupConfig
    rather than passing db names, index names, column names, num memories, separately.
    """

    _cache: dict[tuple, Any] = {}

    def __init__(
        self,
        orca_lookup_type: OrcaLookupType,
        orca_lookup_config: Optional[OrcaLookupConfig] = None,
        cache_ttl: Optional[float] = None,
        **orca_module_settings,
    ):
        """
        :param orca_lookup_type: The OrcaLookupType to use.
        :param orca_lookup_config: The OrcaLookupConfig to use. If None, needs to be specified later. (default: None)
        :param cache_ttl: The time to live (in seconds) for the lookup cache. If None, the cache is disabled. (default: None)
        :param **orca_module_settings: Additional settings to pass to the parent OrcaModule constructor.
        """

        self._orca_lookup_type: OrcaLookupType = orca_lookup_type
        self._orca_lookup_config: Optional[OrcaLookupConfig] = None
        self._orca_db_instance: Optional[OrcaDatabase] = None

        if orca_lookup_config:
            self._orca_lookup_config = self._verify_compatible_lookup_config(orca_lookup_config)
            self._orca_db_instance = OrcaDatabase(self._orca_lookup_config.orca_db_name)
            super().__init__(orca_db_instance=self._orca_db_instance, **orca_module_settings)
        else:
            super().__init__(**orca_module_settings)

        self.use_lookup_cache = cache_ttl is not None
        assert (
            not self.use_lookup_cache or not self._curate_enabled
        ), "Curate tracking is not supported when using the lookup cache"
        assert cache_ttl is None or isinstance(cache_ttl, (int, float))
        self.cache_ttl = cache_ttl

    @property
    def orca_lookup_type(self) -> OrcaLookupType:
        """
        Returns the OrcaLookupType for this layer.
        :return: The OrcaLookupType for this layer.
        """
        return self._orca_lookup_type

    @property
    def orca_lookup_config(self) -> OrcaLookupConfig | None:
        """
        Returns the OrcaLookupConfig for this layer.
        :return: The OrcaLookupConfig for this layer.
        """
        return self._orca_lookup_config

    @property
    def orca_db_instance(self) -> OrcaDatabase | None:
        """
        Returns the OrcaDatabase instance for this layer.
        :return: The OrcaDatabase instance for this layer.
        """
        return self._orca_db_instance

    @lru_cache(maxsize=16)
    def _verify_compatible_lookup_config(self, lookup_config: OrcaLookupConfig) -> OrcaLookupConfig:
        """
        Verifies that the lookup config is compatible with the lookup type.

        The verification results are cached to avoid redundant checks.

        :param lookup_config: The OrcaLookupConfig to be verified.
        :return: The verified OrcaLookupConfig.

        NOTE: This method should not be called directly. It is used internally.
        """

        db = OrcaDatabase(lookup_config.orca_db_name)

        new_index = db.get_index(lookup_config.index_name)
        assert (
            new_index.column_type == self.orca_lookup_type.index_type
        ), f"Index type mismatch. Expected: {self.orca_lookup_type.index_type}, got: {new_index.index_type}"

        assert len(lookup_config.lookup_column_names) == len(
            self.orca_lookup_type.return_column_types
        ), f"Column count mismatch. Expected: {len(self.orca_lookup_type.return_column_types)}, got: {len(lookup_config.lookup_column_names)}"

        # get the table info for this index and verify the column types
        table_info = db._get_index_table(lookup_config.index_name)

        assert len(lookup_config.lookup_column_names) == len(
            self.orca_lookup_type.return_column_types
        ), f"Column count mismatch. Expected: {len(self.orca_lookup_type.return_column_types)}, got: {len(lookup_config.lookup_column_names)}"

        for column_name, column_type in zip(
            lookup_config.lookup_column_names, self.orca_lookup_type.return_column_types
        ):
            if column_name in table_info:
                assert (
                    table_info[column_name] == column_type
                ), f"Column type mismatch for {column_name}. Expected: {column_type}, got: {table_info[column_name]}"
            elif column_name[0] == "$" and column_name[1:] in new_index.artifact_columns:
                computed_column_name = column_name[1:]
                assert (
                    new_index.artifact_columns[computed_column_name] == column_type
                ), f"Column type mismatch for {column_name}. Expected: {column_type}, got: {new_index.artifact_columns[computed_column_name]}"
            else:
                raise ValueError(f"Column {column_name} not found in table or index {lookup_config.index_name}")

        return lookup_config

    def set_lookup_config(self, lookup_config: OrcaLookupConfig) -> None:
        """Overrides the OrcaLookupConfig for this layer with a new one if it matches the OrcaLookupType.

        :param lookup_config: The new OrcaLookupConfig to use.
        """
        self._orca_lookup_config = self._verify_compatible_lookup_config(lookup_config)
        self._orca_db_instance = OrcaDatabase(name=self._orca_lookup_config.orca_db_name)

    def _db_lookup(
        self,
        query: Any,
        db: OrcaDatabase,
        orca_lookup_config: OrcaLookupConfig,
    ) -> BatchedScanResult:
        """
        Performs the lookup in the OrcaDatabase index.
        :param query: The query to be used for the lookup.
        :param orca_lookup_config: The OrcaLookupConfig to be used for the lookup.
        :return: The result of the lookup.

        NOTE: This method should not be called directly. It is used internally.
        """

        cache_key = None
        if self.use_lookup_cache:
            cache_key = (
                query,
                orca_lookup_config,
            )
            mem = OrcaGenericLookupLayer._cache.get(cache_key, None)
            if mem is not None:
                result, timestamp = mem
                if timestamp + self.cache_ttl > time.time():
                    return result

        # TODO same hack as in OrcaTextLookupLayer, will change with index refactor
        if isinstance(query, torch.Tensor):
            query = query.detach().cpu().to(torch.float32).numpy().tolist()
        req = db.vector_scan_index(orca_lookup_config.index_name, query)

        # track this particular lookup using Curate
        if self._curate_enabled:
            if isinstance(query, torch.Tensor):
                assert query.shape[0] == len(
                    self._run_ids
                ), f"Batch size inference appears incorrect. Please set batch size manually. Inferred: {query.shape[0]}, expected: {len(self._run_ids)}"
                req = req.track_with_curate(self._run_ids, self._layer_name or "NA")

            elif isinstance(query, list):
                assert len(query) == len(
                    self._run_ids
                ), f"Batch size inference appears incorrect. Please set batch size manually. Inferred: {len(query)}, expected: {len(self._run_ids)}"
                req = req.track_with_curate(self._run_ids, self._layer_name or "NA")

        res = req.select(*orca_lookup_config.lookup_column_names).fetch(orca_lookup_config.num_memories)  # type: ignore

        if self.use_lookup_cache:
            OrcaGenericLookupLayer._cache[cache_key] = (res, time.time())  # type: ignore

        return res

    def forward(
        self,
        x: Any,
        orca_lookup_config: Optional[OrcaLookupConfig] = None,
    ) -> BatchedScanResult:
        """Performs a "forward pass" or call/retrieval to the lookup layer.
        :param x: The input list of length batch_size or tensor of shape (batch_size, vector_dim)
        :param orca_lookup_config: Optional override for the OrcaLookupConfig to use. (default: None)
        :return: dependent on the orca_lookup_config (return column types)
        """
        if orca_lookup_config is not None:
            orca_lookup_config = self._verify_compatible_lookup_config(orca_lookup_config)
            db = OrcaDatabase(name=orca_lookup_config.orca_db_name)
        else:
            orca_lookup_config = self._orca_lookup_config
            db = self._orca_db_instance
            assert orca_lookup_config is not None, "OrcaLookupConfig must be set before lookup, or passed to forward()"
            assert db is not None, "No OrcaDatabase instance, set_lookup_config or pass OrcaLookupConfig to forward()"

        if orca_lookup_config.num_memories is not None and orca_lookup_config.num_memories <= 0:
            raise ValueError(f"num_memories must be > 0, but is {orca_lookup_config.num_memories}")

        res = self._db_lookup(x, db, orca_lookup_config)

        return res


class OrcaLookupLayer(OrcaModule):
    """A layer that looks up a vector in an OrcaDatabase index and returns the top k results.
    This requires a database to be attached to the model, with the index already created.

    Example usage:
    .. code-block:: python

            import torch
            from orcalib import OrcaModule, OrcaLookupLayer

            class MyModule(OrcaModule):
                def __init__(self):
                    super().__init__()
                    self.linear = torch.nn.Linear(10, 10)
                    self.lookup = OrcaLookupLayer("my_index", ["my_label, my_extra_columns"], 10)

                def forward(self, x):
                    x = self.linear(x)
                    x, meta = self.lookup(x)
                    return x, meta

            model = MyModel()

    """

    _orca_db_instance: OrcaDatabase
    _cache: dict[tuple, Any] = {}

    def __init__(
        self,
        index_name: Optional[str] = None,
        lookup_column_names: Optional[list[ColumnName]] = None,
        num_memories: Optional[int] = None,
        cache_ttl: Optional[float] = None,
        orca_db_instance: Optional[OrcaDatabase] = None,
        **settings,
    ):
        """
        :param index_name: The name of the index to use. (default: None)
        :param lookup_column_names: The names of the columns to return from the index. (default: None)
        :param num_memories: The number of memories to return from the index. (default: None)
        :param cache_ttl: The time to live (in seconds) for the lookup cache. If None, the cache is disabled. (default: None)
        :param orca_db_instance: The OrcaDatabase instance to use. If None, the default OrcaDatabase instance is used. (default: None)
        :param **settings: Additional settings to pass to the parent constructor.
        """
        super().__init__(orca_db_instance=orca_db_instance, **settings)
        self.index_name = index_name
        self.lookup_column_names = lookup_column_names
        self.num_memories = num_memories
        self.use_lookup_cache = cache_ttl is not None
        assert (
            not self.use_lookup_cache or not self._curate_enabled
        ), "Curate tracking is not supported when using the lookup cache"
        assert cache_ttl is None or isinstance(cache_ttl, (int, float))
        self.cache_ttl = cache_ttl

    @property
    def orca_db_instance(self) -> OrcaDatabase:
        """
        Returns the OrcaDatabase instance for this layer.
        :return: The OrcaDatabase instance for this layer.
        """
        return self._orca_db_instance

    @orca_db_instance.setter
    def orca_db_instance(self, value: OrcaDatabase) -> None:
        """
        Sets the OrcaDatabase instance for this layer.
        :param value: The OrcaDatabase instance to be set.
        """
        self._orca_db_instance = value

    def _get_index_info_with_overrides(
        self,
        orca_db_instance: Optional[OrcaDatabase] = None,
        index_name: Optional[str] = None,
        lookup_column_names: Optional[list[str]] = None,
        num_memories: Optional[int] = None,
    ) -> tuple[OrcaDatabase, str, list[str], int]:
        """
        Returns the index-lookup info, with overrides applied where provided
        :param orca_db_instance: The OrcaDatabase instance to use. (default: None)
        :param index_name: The name of the index to use. (default: None)
        :param lookup_column_names: The names of the columns to return from the index. (default: None)
        :param num_memories: The number of memories to return from the index. (default: None)
        :return: A tuple of (OrcaDatabase, index_name, lookup_column_names, num_memories)

        NOTE: This method should not be called directly. It is used internally.
        """
        orca_db_instance = orca_db_instance or self.orca_db_instance
        if orca_db_instance is None:
            raise ValueError("OrcaDatabase instance must be set before lookup or passed to forward()")

        index_name = index_name or self.index_name
        if index_name is None:
            raise ValueError("Index name must be set before lookup or passed to forward()")

        lookup_column_names = lookup_column_names or self.lookup_column_names
        if lookup_column_names is None:
            raise ValueError("Lookup column names must be set before lookup or passed to forward()")

        num_memories = num_memories or self.num_memories
        if num_memories is None or num_memories <= 0:
            raise ValueError("num_memories must be set > 0 before lookup or passed to forward()")

        return orca_db_instance, index_name, lookup_column_names, num_memories

    def _db_lookup(
        self,
        x: torch.Tensor,
        orca_db_instance: OrcaDatabase,
        index_name: str,
        lookup_column_names: list[str],
        num_memories: int,
    ) -> BatchedScanResult:
        """
        Performs the lookup in the OrcaDatabase index.
        :param x: The input tensor of shape (batch_size, vector_dim)
        :param orca_db_instance: The OrcaDatabase instance to use.
        :param index_name: The name of the index to use.
        :param lookup_column_names: The names of the columns to return from the index.
        :param num_memories: The number of memories to return from the index.
        :return: The result of the lookup.

        NOTE: This method should not be called directly. It is used internally.
        """
        cache_key = None
        if self.use_lookup_cache:
            cache_key = (
                x,
                orca_db_instance.name,
                index_name,
                lookup_column_names,
                num_memories,
            )
            mem = OrcaLookupLayer._cache.get(cache_key, None)
            if mem is not None:
                result, timestamp = mem
                if timestamp + self.cache_ttl > time.time():
                    return result

        query = x.detach().cpu().to(torch.float32).numpy().tolist()
        req = orca_db_instance.vector_scan_index(index_name, query)

        # track this particular lookup using Curate
        if self._curate_enabled:
            assert x.shape[0] == len(
                self._run_ids
            ), f"Batch size inference appears incorrect. Please set batch size manually. Inferred: {x.shape[0]}, expected: {len(self._run_ids)}"
            req = req.track_with_curate(self._run_ids, self._layer_name or "NA")

        # execute the lookup (fetch), where meta is a list of additional columns to be returned
        # aside from the index vector matches
        res = req.select(*lookup_column_names).fetch(num_memories)  # type: ignore

        if self.use_lookup_cache:
            OrcaLookupLayer._cache[cache_key] = (res, time.time())  # type: ignore

        return res

    def forward(
        self,
        x: torch.Tensor,
        orca_db_instance: Optional[OrcaDatabase] = None,
        index_name: Optional[str] = None,
        lookup_column_names: Optional[list[str]] = None,
        num_memories: Optional[int] = None,
    ) -> BatchedScanResult:
        """Performs a forward pass
        :param x: The input tensor of shape (batch_size, vector_dim)
        :param orca_db_instance: Optional override for the OrcaDatabase instance to use. (default: None)
        :param index_name: Optional override for the name of the index to use. (default: None)
        :param lookup_column_names: Optional override for the names of the columns to return from the index. (default: None)
        :param num_memories: Optional override for the number of memories to return from the index. (default: None)
        :return: A tuple of (memories, extra) where
        memories is a tensor of shape (batch_size, num_memories, vector_dim) and
        extra is a list of lists of metadata values of shape (batch_size, num_memories, num_meta_columns)
        """
        if num_memories is not None and num_memories <= 0:
            raise ValueError(f"num_memories must be > 0, but is {num_memories}")

        index_settings = self._get_index_info_with_overrides(
            orca_db_instance, index_name, lookup_column_names, num_memories
        )

        lookup_column_names = cast(list[str], index_settings[2])

        res = self._db_lookup(x, *index_settings)
        # res "shape" is (batch_size, num_memories, num_meta_columns)
        # res[i][j] is a VectorScanResult object, which includes a vector and extra metadata

        assert isinstance(res, BatchedScanResult)
        return res


class OrcaLabelLookupLayer(OrcaLookupLayer):
    """A layer that looks up the embedding and label in an OrcaDatabase index and returns the top k results.

    A layer that looks up a vector in an OrcaDatabase index and returns a tuple of two tensors that contain
    the embedding and label for the top k results.

    This requires a database to be attached to the model, with the index already created.

    Example usage:
    .. code-block:: python

        import torch
        from orcalib import OrcaModule, OrcaLabelLookupLayer

        class MyModule(OrcaModule):
            def __init__(self):
                super().__init__()
                self.linear = torch.nn.Linear(10, 10)
                self.lookup = OrcaLabelLookupLayer(
                                    index_name="my_index",
                                    label_column_name="my_label",
                                    num_memories=10
                                )

            def forward(self, x):
                x = self.linear(x)
                embeddings,labels = self.lookup(x)
                return embeddings,labels

        model = MyModel()
    """

    def __init__(
        self,
        index_name: str,
        label_column_name: ColumnName,
        num_memories: int,
        cache_ttl: Optional[float] = None,
        orca_db_instance: Optional[OrcaDatabase] = None,
        **settings,
    ):
        """Initializes the OrcaLabelLookupLayer.
        :param index_name: The name of the index to use.
        :param label_column_name: The name of the label column to return from the index.
        :param num_memories: The number of memories to return from the index.
        :param cache_ttl: The time to live (in seconds) for the lookup cache. If None, the cache is disabled. (default: None)
        :param orca_db_instance: The OrcaDatabase instance to use. If None, the default OrcaDatabase instance is used. (default: None)
        :param **settings: Additional settings to pass to the parent constructor.
        """
        super().__init__(
            index_name, ["$embedding", label_column_name], num_memories, cache_ttl, orca_db_instance, **settings
        )

        self._label_column_name = label_column_name

    def forward(
        self,
        x: torch.Tensor,
        orca_db_instance: Optional[OrcaDatabase] = None,
        index_name: Optional[str] = None,
        label_column_name: Optional[ColumnName] = None,
        num_memories: Optional[int] = None,
    ) -> tuple[Tensor, Tensor]:
        """
        Performs a forward pass
        :param x: The input tensor of shape (batch_size, vector_dim)
        :param orca_db_instance: Optional override for the OrcaDatabase instance to use. (default: None)
        :param index_name: Optional override for the name of the index to use. (default: None)
        :param label_column_name: Optional override for the name of the label column to return from the index. (default: None)
        :param num_memories: Optional override for the number of memories to return from the index. (default: None)
        :return: A tuple of (embeddings, labels) where
        embeddings is a tensor of shape (batch_size, num_memories, vector_dim) and
        labels is an int64 tensor of shape (batch_size, num_memories)
        """
        label_override = None
        if label_column_name:
            label_override = ["$embedding", label_column_name]
        else:
            label_column_name = self._label_column_name

        label_column_name = label_column_name or self._label_column_name
        result = super().forward(x, orca_db_instance, index_name, label_override, num_memories)
        memories = result.to_tensor("$embedding", dtype=x.dtype, device=x.device)
        labels = result.to_tensor(label_column_name, dtype=torch.int64, device=x.device).squeeze(-1)
        return memories, labels


class OrcaClassificationMemoryGuideLayer(OrcaModule):
    """
    A PyTorch module that implements a memory-guided classification layer.

    This layer biases the output of a classification model towards a set of memories
    The bias is controlled by a weight parameter, which determines how strongly the model should be biased towards the memories.
    """

    def __init__(
        self,
        num_classes: int,
        memory_index: str,
        memory_label: str,
        num_memories: int,
        guide_weight: float,
        enable_in_training: bool = False,
        **settings,
    ):
        """
        :param num_classes: The number of classes in the classification task.
        :param memory_index: The name of the memory index to use.
        :param memory_label: The column name of the label for the classification task in the table underpinning memory_index.
        :param num_memories: The number of memories the layer should use.
        :param guide_weight: The weight of the memory guide (i.e. how strongly to bias towards the memory distribution)
        :param enable_in_training: Whether to enable the module in training mode. (default: False)
        :param **settings: Additional settings to pass to the parent constructor.
        """
        super().__init__(**settings)

        self.num_classes = num_classes
        self.guide_weight = guide_weight
        self.enable_in_training = enable_in_training
        self.memory_label = memory_label
        self.lookup = OrcaLabelLookupLayer(memory_index, memory_label, num_memories)

    def forward(
        self,
        logits: torch.Tensor,
        memory_key: torch.Tensor,
        ctx: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """
        :param logits: Input tensor of shape (N, C), where N is the batch size and C is the number of classes.
        :param memory_key: Memory key tensor of shape (N, D), where K is the number of memory slots and D is the model embedding dimension.
        :param ctx: Memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. If None, the memory context is looked up based on the memory key. (default: None)
        :param labels: Memory Label tensor of shape (N,K), where N is the batch size, and K is the number of memories. If None, the labels are looked up along with the memory context. (default: None)

        :return: Output tensor of shape (N, C), where N is the batch size and C is the number of classes.
        """
        if self.training and not self.enable_in_training:
            return logits

        if ctx is None:
            assert labels is None
            ctx, labels = self.lookup(memory_key)

        probs = F.softmax(logits, dim=1)
        assert labels is not None
        assert ctx is not None
        lhat = F.one_hot(labels, num_classes=self.num_classes).to(logits.dtype)
        weights = torch.bmm(ctx, memory_key.unsqueeze(2)).squeeze(2)
        bias = weights.unsqueeze(-1) * lhat
        bias = torch.sum(bias, dim=1)
        bias = torch.nn.functional.softmax(bias, dim=1)
        logits = probs + self.guide_weight * bias

        return logits


class ProjectionMode(Enum):
    """
    Determines how the values from the memory should be "projected" into the models embedding space (i.e. what's the V in the attention mechanism QKV).

    Attributes:
        LABEL: Project the memory's label into the model embedding space.
        POSITIONAL: Project the memory's position (0...num_memories-1) into the model embedding space.
    """

    LABEL = 0
    POSITIONAL = 1


class OrcaClassificationCrossAttentionLayer(OrcaModule):
    """A transformer decoder layer block that does cross attention

    Note that this is Classification-specific, and the labels returned by the lookup layer are used as the value-weights for the cross attention.

    The block contains the typical transformer components: multi-head attention, feed forward, and layer norm.
    The block also contains a lookup layer that looks up a vector in an OrcaDatabase index and returns the top k results.
    These results are used as the memory context for the cross attention.
    """

    def __init__(
        self,
        model_dim: int,
        num_heads: int,
        num_classes: int,
        memory_index: str,
        memory_label: str,
        num_memories: int,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
        split_retrieval_path: bool = False,
        projection_mode: ProjectionMode = ProjectionMode.LABEL,
        **settings,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer.
        :param num_classes: (int) The number of classes for the output classification and weights for cross attention.
        :param memory_index: (str) The name of the OrcaDatabase index to be used for the memory lookup.
        :param memory_label: (str) The name of the column in the OrcaDatabase index to be used as the memory label for value weighting. (e.g., "label")
        :param num_memories: (int) The number of memory vectors to be returned from the lookup.
        :param activation: (Callable[[Tensor], Tensor]) The activation function to be used between the two linear layers. (default: F.relu)
        :param dropout: (float) The dropout rate to be used between the two linear layers. (default: 0.1)
        :param split_retrieval_path: (bool) Whether to split the retrieval path from the forward pass. If True, the memory key must be passed in to the forward pass. (default: False)
        :param projection_mode: (ProjectionMode) The mode to be used for projecting the memory into the model embedding space. (default: ProjectionMode.LABEL)
        This is used when the memory key is different from the input vector
        """
        super().__init__(**settings)

        self.num_classes = num_classes
        self.memory_index = memory_index
        self.memory_label = memory_label
        self.activation = activation
        self.split_retrieval_path = split_retrieval_path
        self.projection_mode = projection_mode
        self.num_memories = num_memories

        self.lookup = OrcaLabelLookupLayer(memory_index, memory_label, num_memories)

        self.cross_attention = nn.MultiheadAttention(
            model_dim, num_heads, dropout=dropout, batch_first=True, vdim=num_classes
        )
        self.attn_norm = nn.LayerNorm(model_dim)

        self.linear1 = nn.Linear(model_dim, model_dim * 4)
        self.dropout1 = nn.Dropout(dropout)
        self.linear2 = nn.Linear(model_dim * 4, model_dim)
        self.dropout2 = nn.Dropout(dropout)
        self.ff_norm = nn.LayerNorm(model_dim)

    def forward(
        self,
        x: torch.Tensor,  # Shape (batch_size, vector_dim)
        ctx: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, vector_dim)
        labels: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, meta_column_count)
        memory_key: Optional[torch.Tensor] = None,  # Shape (batch_size, vector_dim)
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """x, ctx, labels act as Q, K, V for the cross attention layer.
        When ctx is None:
            If split_retrieval_path is False, x is used as both Q and K.
            If split_retrieval_path is True, memory_key is used as K (instead of x)
        When ctx is not None:
            values

        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param labels: The memory label tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        """
        if ctx is None:
            if self.split_retrieval_path and memory_key is None:
                raise ValueError("Split retrieval path requires either a memory key or context to be passed in")
            assert labels is None, "Labels must be None if context is None"
            # Shape of ctx: (batch_size, num_memories, vector_dim)
            # Shape of labels: (batch_size, num_memories)
            ctx, labels = self.lookup(memory_key) if self.split_retrieval_path else self.lookup(x)

        x = x.unsqueeze(1)  # x goes from N x D --> N x 1 x D

        if self.projection_mode == ProjectionMode.POSITIONAL:
            labels = torch.arange(self.num_memories).repeat(x.shape[0], 1)

        values = F.one_hot(labels, self.num_classes).to(x.dtype).to(x.device)  # type: ignore

        # this is what you may want to change if you don't have a classifiation problem
        # TODO: merge Ronak's LLM code in research to here, cleanup/refactor commonalities
        x, _ = self.cross_attention(x, ctx, values)  # N x 1 x D

        x = x.squeeze(1)  # N x D
        x = self.attn_norm(x)  # N x D

        y = self.linear1(x)  # N x D*4
        y = self.activation(y)
        y = self.dropout1(y)
        y = self.linear2(y)  # N x D
        y = self.dropout2(y)
        x = self.ff_norm(y + x)  # N x D

        return x


class OrcaMemoryBindingLayer(OrcaModule):
    """
    A PyTorch module that implements a memory binding layer.
    """

    def __init__(self, num_classes: int, memory_index: str, memory_label: str, num_memories: int):
        """
        :param num_classes: The number of classes in the classification task.
        :param memory_index: The name of the OrcaDatabase index to be used for the memory lookup.
        :param memory_label: The name of the column in the OrcaDatabase index to be used as the memory label for value weighting. (e.g., "label")
        :param num_memories: The number of memory vectors to be returned from the lookup.
        """
        super().__init__()

        self.lookup = OrcaLabelLookupLayer(memory_index, memory_label, num_memories)
        self.num_classes = num_classes

    def forward(
        self,
        logits: torch.Tensor,
        memory_key: Optional[torch.Tensor] = None,
        ctx: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        :param logits: Input tensor of shape (N, C), where N is the batch size and C is the number of classes.
        :param memory_key: Memory key tensor of shape (N, D), where K is the number of memory slots and D is the model embedding dimension. (default: None)
        :param ctx: Memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. If None, the memory context is looked up based on the memory key. (default: None)
        :param labels: Memory Label tensor of shape (N,K), where N is the batch size, and K is the number of memories. If None, the labels are looked up along with the memory context. (default: None)
        """
        if ctx is None:
            assert memory_key is not None
            assert labels is None
            _, labels = self.lookup(memory_key)

        mem_labels = (
            torch.nn.functional.one_hot(labels, num_classes=self.num_classes).to(logits.dtype).to(logits.device)  # type: ignore
        )
        return torch.bmm(logits.unsqueeze(1), mem_labels).squeeze()


class ClassificationMode(Enum):
    """
    Determined how the final classification is performed.

    Attributes:
        DIRECT: Predicts directly into `num_classes` like a conventional classification model.
        MEMORY_BOUND: which uses memory binding to make the prediction (i.e. pick from the classes in the memories).
    """

    DIRECT = 0
    MEMORY_BOUND = 1


class OrcaClassificationHead(
    OrcaModule
):  # Input: single vector of size hidden_size, optional memory context (otherwise looked up), Output: single vector of size num_labels
    """A transformer decoder layer block that does cross attention with memory lookup

    Example usage:
    .. code-block:: python
        import torch
        from orcalib.orca_torch import OrcaModule, OrcaClassificationHead

        class MyModule(OrcaModule):
            def __init__(self):
                super().__init__()
                self.linear = torch.nn.Linear(10, 10)
                self.classifier = OrcaClassificationHead(model_dim=10, num_classes=5, "my_index", "my_label", num_memories=10)

            def forward(self, x):
                x = self.linear(x) # N x 10
                x = self.classifier(x)
                return x # N x 5, e.g., where each row may become logits for a softmax
    """

    def __init__(
        self,
        model_dim,
        num_classes,
        memory_index: str,
        memory_label: str,
        num_memories: int,
        num_layers: int = 1,
        num_heads: int = 8,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
        deep_residuals: bool = False,
        split_retrieval_path: bool = False,
        memory_guide_weight: float = 0.0,
        classification_mode: ClassificationMode = ClassificationMode.DIRECT,  # DIRECT implies ProjectionMode.LABEL, MEMORY_BOUND implies ProjectionMode.POSITIONAL
        single_lookup: bool = True,
        **settings,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_classes: (int) The size of the output vector.
        :param memory_index: (str) The name of the OrcaDatabase index to be used for the memory lookup.
        :param memory_label: (str) The name of the column in the OrcaDatabase index to be used as the memory label. (e.g., "label")
        :param num_memories: (int) The number of memory vectors to be returned from the lookup.
        :param num_layers: (int) The number of attention blocks to be used, copies of OrcaClassificationCrossAttentionLayer. (default: 1)
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer. (default: 8)
        :param activation: (Callable[[Tensor], Tensor]) The activation function used throughout the attention blocks. (default: F.relu)
        :param dropout: (float) The dropout rate to be used between the two linear layers. (default: 0.1)
        :param deep_residuals: (bool) Whether to use the residual (skip) connections. (default: False)
        :param split_retrieval_path: (bool) Whether to split the retrieval path from the forward pass. If True, the memory key must be passed in to the forward pass. (default: False)
        :param memory_guide_weight: (float) The weight of the memory guide (i.e. how strongly to bias towards the memory distribution). (default: 0.0)
        :param classification_mode: (ClassificationMode) The mode of classification to be used. (default: ClassificationMode.DIRECT)
        :param single_lookup: (bool) Whether to use a single lookup for the memory context. (default: True)
        :param settings: (Any) Any additional settings to be applied to the model.
        """
        super().__init__(**settings)
        self.classification_mode = classification_mode
        if classification_mode == ClassificationMode.MEMORY_BOUND:
            projection_mode = ProjectionMode.POSITIONAL
            self.memory_binding = OrcaMemoryBindingLayer(num_classes, memory_index, memory_label, num_memories)
            inner_classes = num_memories
        elif classification_mode == ClassificationMode.DIRECT:
            projection_mode = ProjectionMode.LABEL
            self.memory_binding = torch.nn.Identity()
            inner_classes = num_classes
        else:
            raise ValueError(f"Unknown classification mode {classification_mode}")

        self.single_lookup = single_lookup
        # The name of the column containing the memory's label
        self.memory_label = memory_label
        self.lookup = OrcaLabelLookupLayer(memory_index, memory_label, num_memories)

        self.memory_layers = nn.ModuleList(
            [
                OrcaClassificationCrossAttentionLayer(
                    model_dim,
                    num_heads=num_heads,
                    num_classes=inner_classes,
                    memory_index=memory_index,
                    memory_label=memory_label,
                    num_memories=num_memories,
                    activation=activation,
                    dropout=dropout,
                    split_retrieval_path=split_retrieval_path,
                    projection_mode=projection_mode,
                )
                for i in range(num_layers)
            ]
        )
        self.classifier = _LinearClassificationHead(model_dim, inner_classes, dropout=dropout, activation=activation)
        self._memory_enabled = True
        self.deep_residuals = deep_residuals
        self.memory_guide_weight = memory_guide_weight
        self.guide = OrcaClassificationMemoryGuideLayer(
            num_classes=num_classes,
            memory_index=memory_index,
            memory_label=memory_label,
            num_memories=num_memories,
            guide_weight=memory_guide_weight,
        )

    def forward(
        self,
        x: torch.Tensor,
        ctx: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
        memory_key: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """
        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param labels: The memory label tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, C), where N is the batch size and C is the number of classes.
        """
        if ctx is None and self.single_lookup:
            assert labels is None
            if memory_key is None:
                memory_key = x
            ctx, labels = self.lookup(memory_key)
        inpt = x
        if self._memory_enabled:
            for layer in self.memory_layers:
                y = layer(x, ctx, labels, memory_key)
                if self.deep_residuals:
                    x = y + x
                else:
                    x = y
        x = self.classifier(x)
        if self.classification_mode == ClassificationMode.MEMORY_BOUND:
            x = self.memory_binding(x, inpt, ctx, labels)
        if self.memory_guide_weight > 0.0:
            x = self.guide(x, memory_key or inpt, ctx, labels)
        return x

    def _orca_memory_toggle(self, enable: bool) -> None:
        """
        Toggles the memory guide layer on or off.
        :param enable: Whether to enable the memory guide layer.

        NOTE: This method should not be called directly. It is used internally.
        """
        self._memory_enabled = enable


class OrcaLLMMemoryGuideLayer(OrcaModule):
    """
    A PyTorch module that implements a memory-guided generation layer for Language Models.

    This layer biases the output distribution of the model towards a set of memories.
    """

    def __init__(
        self,
        alpha: float,
        beta: float,
        memory_index: str,
        memory_col: str,
        num_memories: int,
        tokenizer: Callable[[str | list[str]], list[int] | list[list[int]]],
        vocab_size: int,
        S_min: int = 3,
        S_max: int = 10,
        enable_in_training: bool = False,
        **settings,
    ):
        """
        :param alpha: How strongly to bias the model output distribution towards similar stirng continuations in the memories. Needs hyperparameter tuning.
        :param beta: How strongly to bias the model output distribution towards tokens that appear in the memories. Needs hyperparameter tuning.
        :param memory_index: The memory index.
        :param memory_col: The memory column.
        :param num_memories: The number of memories.
        :param tokenizer: The tokenizer function for the underlying language model model.
        :param vocab_size: The vocabulary size for the underlying language model.
        :param S_min: The minimum matching length for the string contunuation bias (overall weight controlled by alpha). Should not need hyperparameter tuning. (default: 3)
        :param S_max: The maximum matching length for the string contunuation bias (overall weight controlled by alpha). Should not need hyperparameter tuning. (default: 10)
        :param enable_in_training: Flag to enable in training. (Not recommended) (default: False)
        :param **settings: Additional settings to pass to the parent constructor.
        """
        super().__init__(**settings)
        self.alpha = alpha
        self.beta = beta
        self.S_min = S_min
        self.S_max = S_max
        self.tokenizer = tokenizer
        self.enable_in_training = enable_in_training
        self.vocab_size = vocab_size
        self.memory_col = memory_col

        self.lookup = OrcaLookupLayer(memory_index, ["$embedding", memory_col], num_memories)

    def _compute_lps_array(self, pattern) -> list[int]:
        """
        Compute the longest prefix that is also a suffix (lps) array used in KMP algorithm.
        :param pattern: The pattern to compute the lps array for.
        :return: The lps array.

        NOTE: This method should not be called directly. It is used internally.
        """
        lps = [0] * len(pattern)
        length = 0  # length of the previous longest prefix suffix

        # Loop calculates lps[i] for i = 1 to M-1
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                    # Note that we do not increment i here
                else:
                    lps[i] = 0
                    i += 1

        return lps

    def _find_suffixes_in_sequence(self, S, M, S_min, S_max) -> list[tuple[int, int, str]]:
        """
        Find the starting indexes where the suffixes of S of lengths between S_min and S_max
        are contained in M.
        :param S: The sequence to search for suffixes in M.
        :param M: The sequence to search for suffixes of S.
        :param S_min: The minimum length of the suffixes to search for.
        :param S_max: The maximum length of the suffixes to search for.
        :return: A list of tuples containing the starting index of the suffix in M, the length of the suffix, and the next token in M after the suffix.

        NOTE: This method should not be called directly. It is used internally.
        """
        occurrences = []

        # Iterate through the range of lengths for suffixes of S
        for suffix_length in range(S_min, S_max + 1):
            # Get the suffix of S of length suffix_length
            suffix = S[-suffix_length:]

            # Preprocess the suffix to get the lps array
            lps = self._compute_lps_array(suffix)

            # Start searching for the suffix in M
            i = j = 0  # i is index for M, j is index for suffix
            while i < len(M):
                if suffix[j] == M[i]:
                    i += 1
                    j += 1

                if j == len(suffix):
                    # If we found a complete match, record the index where it starts in M
                    if i < len(M):
                        occurrences.append((i - j, len(suffix), M[i]))
                    else:
                        occurrences.append((i - j, len(suffix), None))
                    j = lps[j - 1]

                # Mismatch after j matches
                elif i < len(M) and suffix[j] != M[i]:
                    # Do not match lps[0..lps[j-1]] characters, they will match anyway
                    if j != 0:
                        j = lps[j - 1]
                    else:
                        i += 1

        return occurrences

    def _extract_occurance_ranks(self, occurrences, ref_length) -> dict[int, float]:
        """
        Extract the occurance ranks from the occurrences.
        :param occurrences: The occurrences to extract the ranks from.
        :param ref_length: The length of the reference sequence.
        :return: A dictionary of token to occurance rank.

        NOTE: This method should not be called directly. It is used internally.
        """
        scores = defaultdict(int)
        for _, length, next_token in occurrences:
            if next_token is None:
                continue
            if length > scores[next_token]:
                scores[next_token] = length / ref_length
        return dict(scores)

    def _bag_of_words_probs(self, bag_of_words: list[tuple[list[int], float]]) -> torch.Tensor:
        """
        Compute the bag of words probabilities.
        :param bag_of_words: The bag of words to compute the probabilities for.
        :return: The bag of words probabilities.

        NOTE: This method should not be called directly. It is used internally.
        """
        res = torch.zeros(self.vocab_size)
        for bag, score in bag_of_words:
            for token in bag:
                res[token] += score
        return torch.Tensor(res).softmax(dim=-1)

    def _weighted_next_tokens_from_memory(
        self, memory_key: torch.Tensor, q_tokens: list[int]
    ) -> tuple[
        dict[int, float], list[tuple[list[int], float]]
    ]:  # suffix max dict (token -> score), bag_of_words list (token list, score)
        """
        Compute the weighted next tokens from memory.
        :param memory_key: The memory key to use for memory lookup.
        :param q_tokens: The input tokens.
        :return: A tuple containing the weighted next tokens from the memory and the bag of words.

        NOTE: This method should not be called directly. It is used internally.
        """
        result = self.lookup(memory_key)
        ctx = result.to_tensor("$embedding", dtype=memory_key.dtype, device=memory_key.device)
        candidates: list[str] = result[0, :, self.memory_col].to_list()
        semantic_scores: list[float] = (ctx.squeeze() @ memory_key.squeeze()).tolist()
        tokens_and_weights: dict[int, float] = {}
        for candidate, semantic_score in zip(candidates, semantic_scores):
            tokens = self.tokenizer(candidate)
            suffixes = self._find_suffixes_in_sequence(q_tokens[0], tokens, self.S_min, self.S_max)
            scores = self._extract_occurance_ranks(suffixes, len(tokens))
            for token, score in scores.items():
                if token not in tokens_and_weights or score > tokens_and_weights[token]:
                    tokens_and_weights[token] = score * semantic_score
        bag_of_words_tokens: list[list[int]] = cast(list[list[int]], self.tokenizer(candidates))
        return {token: score for token, score in tokens_and_weights.items()}, list(
            zip(
                bag_of_words_tokens,
                [x / len(candidates) for x in semantic_scores],
                strict=True,
            )
        )

    def forward(self, memory_key: torch.Tensor, logits: torch.Tensor, inpt_tokens: list[int]) -> torch.Tensor:
        """
        Forward pass.
        :param memory_key: The memory key to use for memory lookup.
        :param logits: The original model logits.
        :param inpt_tokens: The input tokens.
        :return: The updated logits.
        """
        if self.training and not self.enable_in_training:
            return logits

        probs = torch.softmax(logits, dim=-1)
        candidates, bag_of_words = self._weighted_next_tokens_from_memory(memory_key, inpt_tokens)

        if self.alpha > 0.0:
            for token, score in candidates.items():
                probs[0][token] += self.alpha * score

        if self.beta > 0.0:
            probs[0] += self.beta * self._bag_of_words_probs(bag_of_words).to(probs.device)
        return probs


class OrcaRankingCrossAttentionLayer(OrcaModule):
    """A transformer decoder layer block that does cross attention for rankings.

    Note that this is Ranking-specific, and the rankings returned by the lookup layer are used as the value-weights for the cross attention.

    The block contains the typical transformer components: multi-head attention, feed forward, and layer norm.
    The block also contains a lookup layer that looks up a vector in an OrcaDatabase index and returns the top k results.
    These results are used as the memory context for the cross attention.
    """

    def __init__(
        self,
        model_dim: int,
        num_heads: int,
        num_ranks: int,
        memory_index: str,
        memory_col: str,
        num_memories: int,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
        split_retrieval_path: bool = False,
        projection_mode: ProjectionMode = ProjectionMode.LABEL,
        **settings,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer.
        :param num_ranks: (int) The number of ranks for the output classification and weights for cross attention.
        :param orca_lookup_type: (OrcaLookupType) The type of the OrcaLookupLayer to be used for the memory lookup.
        :param orca_lookup_config: (OrcaLookupConfig) The configuration for the OrcaLookupLayer to be used for the memory lookup.
        :param activation: (Callable[[Tensor], Tensor]) The activation function to be used between the two linear layers. (default: F.relu)
        :param dropout: (float) The dropout rate to be used between the two linear layers. (default: 0.1)
        :param split_retrieval_path: (bool) Whether to split the retrieval path from the forward pass. If True, the memory key must be passed in to the forward pass. (default: False)
        :param projection_mode: (ProjectionMode) Determines how the values from the memory should be "projected" into the models embedding space (i.e. what's the V in the attention mechanism QKV). (default: ProjectionMode.LABEL)
        :param settings: (Any) Additional settings to pass to the parent constructor.
        This is used when the memory key is different from the input vector
        """
        super().__init__(**settings)

        self.num_ranks = num_ranks
        self.activation = activation
        self.split_retrieval_path = split_retrieval_path
        self.projection_mode = projection_mode
        self.memory_col = memory_col

        self.lookup = OrcaLabelLookupLayer(memory_index, memory_col, num_memories)

        self.cross_attention = nn.MultiheadAttention(
            model_dim,
            num_heads,
            dropout=dropout,
            batch_first=True,
        )
        self.attn_norm = nn.LayerNorm(model_dim)

        self.linear1 = nn.Linear(model_dim, model_dim * 4)
        self.dropout1 = nn.Dropout(dropout)
        self.linear2 = nn.Linear(model_dim * 4, model_dim)
        self.dropout2 = nn.Dropout(dropout)
        self.ff_norm = nn.LayerNorm(model_dim)

    def forward(
        self,
        x: torch.Tensor,  # Shape (batch_size, vector_dim)
        ctx: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, vector_dim)
        ranks: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, meta_column_count)
        memory_key: Optional[torch.Tensor] = None,  # Shape (batch_size, vector_dim)
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """x, ctx, ranks act as Q, K, V for the cross attention layer.
        When ctx is None:
            If split_retrieval_path is False, x is used as both Q and K.
            If split_retrieval_path is True, memory_key is used as K (instead of x)
        When ctx is not None:
            ranks

        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param ranks: The memory rank tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        """
        if ctx is None:
            if self.split_retrieval_path and memory_key is None:
                raise ValueError("Split retrieval path requires either a memory key or context to be passed in")
            assert ranks is None, "Ranks must be None if context is None"
            # Shape of ctx: (batch_size, num_memories, vector_dim)
            ctx, ranks = self.lookup(memory_key) if self.split_retrieval_path else self.lookup(x)

        x = x.unsqueeze(1)  # x goes from N x D --> N x 1 x D

        # setup the values for the cross attention based on normalizing the ranks from the memory contexts
        # higher rank means higher value
        normalized_ranks = ranks / self.num_ranks  # type: ignore

        values = normalized_ranks.unsqueeze(-1).expand(-1, -1, x.shape[-1])

        x, _ = self.cross_attention(x, ctx, values)  # N x 1 x D
        # x, _ = self.cross_attention(x, ctx, ctx)  # N x 1 x D

        x = x.squeeze(1)  # N x D
        x = self.attn_norm(x)  # N x D

        y = self.linear1(x)  # N x D*4
        y = self.activation(y)
        y = self.dropout1(y)
        y = self.linear2(y)  # N x D
        y = self.dropout2(y)
        x = self.ff_norm(y + x)  # N x D

        return x


class OrcaRankingHead(
    OrcaModule
):  # Input: single vector of size hidden_size, optional memory context (otherwise looked up), Output: single element of size 1
    """A transformer decoder layer block that does cross attention with memory lookup for ranking problems"""

    def __init__(
        self,
        model_dim,
        num_ranks,
        memory_index: str,
        memory_label: str,
        num_memories: int,
        num_layers: int = 1,
        num_heads: int = 8,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
        deep_residuals: bool = False,
        split_retrieval_path: bool = False,
        memory_guide_weight: float = 0.0,
        single_lookup: bool = True,
        **settings,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_ranks: (int) The number of ranks for the output classification and weights for cross attention.
        :param memory_index: (str) The name of the OrcaDatabase index to be used for the memory lookup.
        :param memory_label: (str) The name of the column in the OrcaDatabase index to be used as the memory label. (e.g., "label")
        :param num_memories: (int) The number of memory vectors to be returned from the lookup.
        :param num_layers: (int) The number of attention blocks to be used, copies of OrcaClassificationCrossAttentionLayer. (default: 1)
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer. (default: 8)
        :param activation: (Callable[[Tensor], Tensor]) The activation function used throughout the attention blocks. (default: F.relu)
        :param dropout: (float) The dropout rate to be used between the two linear layers. (default: 0.1)
        :param deep_residuals: (bool) Whether to use the residual (skip) connections. (default: False)
        :param split_retrieval_path: (bool) Whether to split the retrieval path from the forward pass. If True, the memory key must be passed in to the forward pass. (default: False)
        :param memory_guide_weight: (float) The weight to be applied to the memory guide layer. (default: 0.0)
        :param single_lookup: (bool) Whether to use a single lookup for the memory context. (default: True)
        :param settings: (Any) Any additional settings to be applied to the model. (e.g., "device")
        """
        super().__init__(**settings)

        self.single_lookup = single_lookup
        self.memory_label = memory_label
        self.lookup = OrcaLabelLookupLayer(memory_index, memory_label, num_memories)

        self.memory_layers = nn.ModuleList(
            [
                OrcaRankingCrossAttentionLayer(
                    model_dim,
                    num_heads=num_heads,
                    num_ranks=num_ranks,
                    memory_index=memory_index,
                    memory_col=memory_label,
                    num_memories=num_memories,
                    activation=activation,
                    dropout=dropout,
                    split_retrieval_path=split_retrieval_path,
                )
                for i in range(num_layers)
            ]
        )
        self.classifier = _LinearClassificationHead(model_dim, 1, dropout=dropout, activation=activation)
        self._memory_enabled = True
        self.deep_residuals = deep_residuals

    def forward(
        self,
        x: torch.Tensor,
        ctx: Optional[torch.Tensor] = None,
        ranks: Optional[torch.Tensor] = None,
        memory_key: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """
        forward pass
        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param ranks: The memory rank tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, 1), where N is the batch size. The output is the rank of the input vector.
        """
        if ctx is None and self.single_lookup:
            assert ranks is None
            if memory_key is None:
                memory_key = x
            ctx, ranks = self.lookup(memory_key)
        if self._memory_enabled:
            for layer in self.memory_layers:
                y = layer(x, ctx, ranks, memory_key)
                if self.deep_residuals:
                    x = y + x
                else:
                    x = y
        x = self.classifier(x)
        return x

    def _orca_memory_toggle(self, enable: bool) -> None:
        """
        Toggles the memory layer on or off.
        :param enable: (bool) Whether to enable the memory layer.

        NOTE: This method should not be called directly. It is used internally.
        """
        self._memory_enabled = enable


###################
### Training Utils
###################
class OrcaMemoryDatasetV1(Dataset):
    """A PyTorch dataset that pulls the entire index on demand from an OrcaDatabase to be used locally"""

    def __init__(
        self,
        db: OrcaDatabase,
        index: str,
        columns: list[str | ColumnHandle] | str | ColumnHandle,
        memory_index: str,
        mem_columns: list[str | ColumnHandle] | str | ColumnHandle,
        num_memories: int,
        *,
        page_size: int = 1000,
    ):
        """
        :param db: The OrcaDatabase to pull the index from.
        :param index: The name of the OrcaDatabase index to be used for the memory lookup.
        :param columns: The columns to be used for the memory lookup.
        :param memory_index: The name of the OrcaDatabase index to be used for the memory lookup.
        :param mem_columns: The columns to be used for the memory lookup.
        :param num_memories: The number of memory vectors to be returned from the lookup.
        :param page_size: The page size to use for fetching the index. Defaults to 1000.
        """
        self.db = db
        self.index = index
        self.memory_index = memory_index
        self.num_memories = num_memories
        self.table: TableHandle = cast(TableHandle, db._get_index_table(index))
        self.mem_table: TableHandle = cast(TableHandle, db._get_index_table(memory_index))
        self.columns = columns
        self.mem_columns = mem_columns

        if not isinstance(columns, list):
            columns = [columns]

        print(f"Getting query data for index table {index} and columns {columns}")

        self.data = cast(
            list[tuple[int, dict[str, Any]]],
            self.table.select(*columns).fetch(include_ids=True),
        )  # data[i][0] = id, data[i][1] = row dict

        print(f"Fetching vectors for index {index} ({len(self.data)} rows)")

        self.vecs_dict = db._get_index_values_paginated(
            index,
            page_size=page_size,
        )  # row_id -> embedding vector (list of floats)

        if memory_index == index:
            self.mem_vecs_dict = self.vecs_dict
        else:
            print(f"Fetching vectors for memory index {memory_index}")
            self.mem_vecs_dict = db._get_index_values_paginated(memory_index, page_size=page_size)

        if not isinstance(mem_columns, list):
            mem_columns = [mem_columns]

        print(f"Getting query data for memory index table {memory_index} and columns {mem_columns}")

        self.mem_data = dict(
            cast(
                list[tuple[int, dict[str, Any]]],
                self.mem_table.select(*mem_columns).fetch(include_ids=True),
            )
        )  # dict[row_id, dict[str, Any]]

        vecs = Tensor(list(self.vecs_dict.values()))
        self.mem_vecs = Tensor(list(self.mem_vecs_dict.values()))

        print(
            f"Computing nearest neighbors of {len(self.vecs_dict)} vectors against {len(self.mem_vecs_dict)} memory vectors"
        )

        D = vecs @ self.mem_vecs.T
        self.topk = torch.topk(D, self.num_memories)

        self.top_k_dict = {_id: self.topk.indices[i] for i, _id in enumerate(self.vecs_dict.keys())}

        self.mem_id_map = list(self.mem_vecs_dict.keys())

        print(f"Finished preparing OrcaMemoryDataset for index {index} with memory index {memory_index}")

    def __get_mems(self, row_id: int) -> tuple[Tensor, list[Any] | Any]:
        """
        Get the memory vectors and metadata for a given row id.
        :param row_id: The row id to get the memory vectors and metadata for.
        :return: A tuple containing the memory vectors and metadata.
        """
        mem_idxs = self.top_k_dict[row_id]
        mems = self.mem_vecs[mem_idxs]
        mem_data_ids = [int(self.mem_id_map[mem_idx]) for mem_idx in mem_idxs]

        mem_column_dicts = [self.mem_data[mem_data_id] for mem_data_id in mem_data_ids]

        def _get_one_mem(mem_column_dict: dict[str, Any]) -> list[Any] | Any:
            """
            Get one memory vector and metadata.
            :param mem_column_dict: The memory column dictionary to get the memory vector and metadata from.
            :return: A tuple containing the memory vector and metadata.

            NOTE: This method should not be called directly. It is used internally.
            """
            if not isinstance(self.mem_columns, list):
                col_name = (
                    self.mem_columns.column_name if isinstance(self.mem_columns, ColumnHandle) else self.mem_columns
                )
                mem_columns = mem_column_dict[col_name]
            else:
                col_names = [
                    column.column_name if isinstance(column, ColumnHandle) else column for column in self.mem_columns
                ]
                mem_columns = [mem_column_dict[col_name] for col_name in col_names]
            return mem_columns

        mem_columns = [_get_one_mem(mem_column_dict) for mem_column_dict in mem_column_dicts]

        return mems, mem_columns

    def __getitem__(self, index: int) -> tuple[Tensor, list[Any] | Any, Tensor, list[Any] | Any]:
        """
        Get an item from the dataset.
        :param index: The index of the item to get.
        :return: A tuple containing the item vector, item metadata, topk memory vectors, and topk memory metadata.
        """
        itemid, columns_dicts = self.data[index]

        if len(columns_dicts) == 1:
            columns = list(columns_dicts.values())[0]
        else:
            assert isinstance(self.columns, list)
            columns = [
                columns_dicts[column.column_name if isinstance(column, ColumnHandle) else column]
                for column in self.columns
            ]

        vec = self.vecs_dict[itemid]

        mems, mem_columns = self.__get_mems(itemid)

        return Tensor(vec), columns, Tensor(mems), mem_columns

    def __len__(self) -> int:
        return len(self.data)


class OrcaMemoryDatasetV2(Dataset):
    """A PyTorch dataset that pulls the entire index on demand from an OrcaDatabase to be used locally

    A PyTorch dataset that pulls the entire index on demand from an OrcaDatabase to be used locally
    for training Orca-based layers and models. This is useful for small datasets that can
    fit in memory, or for debugging purposes.

    The dataset consists of a list of tuples, where each tuple contains:
    - The item vector
    - The item metadata
    - The topk memory vectors
    - The topk memory metadata

    The item vector is a Tensor of shape (vector_dim,)
    The item metadata is a list of arbitrary metadata values
    The topk memory vectors is a Tensor of shape (num_memories, vector_dim)
    The topk memory metadata is a list of lists of arbitrary metadata values

    Example usage:
    .. code-block:: python
        import torch
        from orcalib.orca_torch import OrcaMemoryDataset

        dataset = OrcaMemoryDataset(db, index="my_index",
                                        columns="my_label",
                                        memory_index="my_index",
                                        mem_columns="my_label",
                                        num_memories=10,
                                        page_size=1000)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
        for batch in dataloader:
            item_vectors, item_metadata, memory_vectors, memory_metadata = batch
            # do something with the batch

    See also: integration_tests/news_classification_integration_test.py
    """

    def __init__(
        self,
        db: OrcaDatabase,
        index: str,
        columns: list[str | ColumnHandle] | str | ColumnHandle,
        memory_index: str,
        mem_columns: list[str | ColumnHandle] | str | ColumnHandle,
        num_memories: int,
        *,
        page_size: int = 1000,
        verbose: bool = False,
    ):
        """
        :param db: The OrcaDatabase to fetch the index data from.
        :param index: The name of the index to fetch the data from.
        :param columns: The columns to fetch from the index. Can be a single column name, or a list of column names.
        :param memory_index: The name of the memory index to fetch the data from. (Generally the same as the index)
        :param mem_columns: The columns to fetch from the memory index. Can be a single column name, or a list of column names.
        :param num_memories: The number of memory vectors to fetch for each item vector.
        :param page_size: (Optional) The page size to use when fetching the data from the database. (default: 1000)
        :param verbose: (Optional) Whether to print verbose logging information. (default: False)
        """
        self.db = db
        self.index = index
        self.memory_index = memory_index
        self.num_memories = num_memories
        self.columns = columns
        self.mem_columns = mem_columns
        self.num_memories = num_memories
        self.verbose = verbose

        print(f"Fetching index-join page 0 for index {index}")

        first_page = self.db.full_vector_memory_join(
            index_name=index,
            memory_index_name=memory_index,
            num_memories=num_memories,
            query_columns=columns,  # type: ignore
            page_size=page_size,
            page_index=0,
        )

        print(f"Fetching vectors for memory index {memory_index}")

        self.memory_vectors = self.db._get_index_values_paginated(memory_index, page_size=page_size)

        print(f"Fetching memory data for memory index {memory_index} with columns {mem_columns}")

        mem_table: TableHandle = cast(TableHandle, db._get_index_table(memory_index))

        self.mem_data = dict(
            cast(
                list[tuple[int, dict[str, Any]]],
                mem_table.select(*self.__ensure_list(mem_columns)).fetch(include_ids=True),
            )
        )

        self.length = first_page["total_size"]
        self.num_pages = first_page["num_pages"]
        self.page_size = first_page["page_size"]

        assert first_page["page_index"] == 0

        self.pages = {0: first_page}

    def __get_page_for_index(self, index: int) -> dict[str, Any]:
        """
        Get the page for the given index.
        :param index: The index to get the page for.
        :return: The page for the given index.
        """
        page_index = index // self.page_size  # type: ignore

        if page_index in self.pages:
            return self.pages[page_index]

        if self.verbose:
            print(
                f"Fetching index-join page {page_index} of {self.num_pages} for index {index} of {self.length} (query index: {self.index}, memory_index: {self.memory_index})"
            )

        page = self.db.full_vector_memory_join(
            index_name=self.index,
            memory_index_name=self.memory_index,
            num_memories=self.num_memories,
            query_columns=self.columns,  # type: ignore
            page_size=self.page_size,  # type: ignore
            page_index=page_index,
        )
        self.pages[page_index] = page
        return page

    def __ensure_list(self, x: Any) -> list[Any]:
        """
        Ensure that the given value is a list.
        :param x: The value to ensure is a list.
        :return: The value as a list.
        """
        if isinstance(x, list):
            return x
        return [x]

    def __get_column_name(self, column: str | ColumnHandle) -> str:
        """
        Get the column name from the given column handle.
        :param column: The column handle to get the column name from.
        :return: The column name.
        """
        if isinstance(column, ColumnHandle):
            return column.column_name
        return column

    def __get_dict_values(
        self,
        d: dict[str, Any],
        keys: list[str | ColumnHandle] | str | ColumnHandle,
    ) -> list[Any]:
        """
        Get the values from the given dictionary for the given keys.
        :param d: The dictionary to get the values from.
        :param keys: The keys to get the values for.
        :return: The values from the dictionary for the given keys.
        """
        if isinstance(keys, list):
            col_names = [self.__get_column_name(column) for column in keys]
            return [d[col_name] for col_name in col_names]
        else:
            col_name = self.__get_column_name(keys)
            return d[col_name]

    def __getitem__(self, index: int) -> tuple[Tensor, list[Any] | Any, Tensor, list[Any]]:
        """returns: item vector, item metadata, topk memory vectors, topk memory metadata
        If the item is in a "page" already in memory, it is retrieved from the page.
        Otherwise, the page is fetched from the database and stored in memory.

        :param index: The index of the item to get.
        :return: A tuple containing the item vector, item metadata, topk memory vectors, and topk memory metadata.
        """

        if index >= cast(int, self.length):
            raise IndexError(f"Index {index} out of range for dataset of size {self.length}")
        page = self.__get_page_for_index(index)
        sub_index = index % self.page_size  # type: ignore
        item = page["items"][sub_index]
        item_vector = Tensor(item["query_vector"])
        item_metadata = item["query_payload"]

        if not isinstance(self.columns, list) or (isinstance(self.columns, list) and len(self.columns) == 1):
            item_metadata = item_metadata[0]

        mem_vectors = Tensor([self.memory_vectors[mem] for mem in item["top_memories"]])

        mem_metadata = [self.__get_dict_values(self.mem_data[mem], self.mem_columns) for mem in item["top_memories"]]

        return item_vector, item_metadata, mem_vectors, mem_metadata

    def __len__(self) -> int:
        """Returns the length of the dataset"""
        return self.length

    def get_dict(self, index: int) -> dict:
        """
        Returns the dictionary for the item at the given index
        :param index: The index of the item to get the dictionary for.
        :return: The dictionary for the item at the given index.
        """
        page = self.__get_page_for_index(index)
        sub_index = index % self.page_size  # type: ignore
        return page["items"][sub_index]

    def get_score(self) -> float:
        """Classification score for the dataset, which is the product of the hit rate and the correct rate

        This is a measure of how well the memory vectors are able to classify the items in the dataset.
        :return: The classification score for the dataset.
        """
        total = 0
        contains_correct = 0
        count_correct = 0
        count_wrong = 0
        total_mems = 0
        for record in tqdm(self):  # type: ignore
            columns = record[1]
            if not isinstance(columns, list):
                label = columns
            else:
                # TODO: This is brittle, because it assumes the position of the label in the columns
                label = columns[1]
            # label = record[1][1]
            mem_labels = record[3]
            total += 1
            if label in mem_labels:
                contains_correct += 1
            for mem_label in mem_labels:  # type: ignore
                total_mems += 1
                if mem_label == label:
                    count_correct += 1
                else:
                    count_wrong += 1

        correct_rate = count_correct / total_mems
        hit_rate = contains_correct / total
        return correct_rate * hit_rate


OrcaMemoryDataset = OrcaMemoryDatasetV2


class OrcaTextClassificationTrainer:
    """A simple trainer class for Text Classification Problems with Orca. Intended for quick prototyping, not to outperform a custom training loop."""

    def __init__(
        self,
        model,
        tokenizer,
        trainloader: DataLoader,
        testloader: DataLoader,
        use_memory: bool = True,
        memory_dropout: float = 0.0,
        device_override: str | None = None,
        param_groups: None | list[dict[str, Any]] = None,
        verbosity: int = 0,
    ):
        """
        :param model: The model to train.
        :param tokenizer: The tokenizer to use for encoding the input data.
        :param trainloader: The DataLoader for the training data.
        :param testloader: The DataLoader for the test data.
        :param use_memory: Whether to use memory for the model.
        :param memory_dropout: The dropout rate to use for the memory.
        :param device_override: (Optional) The device to use for training. If None, the device will be automatically selected based on the availability of CUDA. (default: None)
        :param param_groups: (Optional) The parameter groups to use for training. If None, the model parameters will be used. (default: None)
        :param verbosity: (Optional) The verbosity level to use for training. (default: 0)
        """
        self.model = model
        self.tokenizer = tokenizer
        self.trainloader = trainloader
        self.testloader = testloader
        self.use_memory = use_memory
        self.verbosity = verbosity
        assert 0.0 <= memory_dropout <= 1.0, "memory_dropout must be between 0.0 and 1.0"
        self.memory_dropout = memory_dropout
        if device_override is not None:
            self.device = torch.device(device_override)
            self.dtype = torch.float32
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.dtype = torch.bfloat16
        elif torch.backends.mps.is_available():  # type: ignore
            self.device = torch.device("mps")
            self.dtype = torch.float32
        else:
            self.device = torch.device("cpu")
            self.dtype = torch.float32
        self.param_groups = param_groups
        self.model = self.model.to(self.device, dtype=self.dtype)
        self.criterion = torch.nn.CrossEntropyLoss()
        if param_groups is None:
            param_groups = model.parameters()
        self.optimizer = torch.optim.Adam(param_groups, lr=0.001)  # type: ignore

    def _get_accuracy(self, logits, labels) -> float:
        """
        Computes and returns the accuracy of the model.
        :param logits: The logits from the model.
        :param labels: The labels for the data.
        :return: The accuracy of the model.

        NOTE: This method should not be called directly. It is used internally.
        """
        _, preds = torch.max(logits, 1)
        return (preds == labels).float().mean().item()

    def get_test_accuracy(self, testloader_override: DataLoader | None = None) -> float:
        """
        Computes and returns the average accuray of the model either on the main testset (from the constructor) or on the provided testloader_override
        :param testloader_override: (Optional) The DataLoader to use for the testset. If None, the main testset will be used. (default: None)
        :return: The average accuracy of the model on the testset.
        """
        self.model.eval()
        if testloader_override is not None:
            testloader = testloader_override
        else:
            testloader = self.testloader
        with torch.no_grad():
            test_acc = 0.0
            test_steps = 0
            for _, keys_and_labels, ctxs, ctx_labels in tqdm(testloader, desc="Processing Testset"):
                keys = keys_and_labels[0]
                labels = keys_and_labels[1]
                ctx_labels = torch.stack(ctx_labels).T
                encoding = self.tokenizer(
                    keys,
                    add_special_tokens=True,
                    padding="max_length",
                    return_tensors="pt",
                )
                inputs = encoding["input_ids"]
                mask = encoding["attention_mask"]
                inputs, mask, labels, ctxs, ctx_labels = (
                    inputs.to(self.device),
                    mask.to(self.device),
                    labels.to(self.device),
                    ctxs.to(self.device).to(self.dtype),
                    ctx_labels.to(self.device),
                )
                if self.use_memory:
                    outputs = self.model(inputs, mask, ctxs, ctx_labels)
                else:
                    outputs = self.model(inputs, mask)
                test_acc += self._get_accuracy(outputs, labels)
                test_steps += 1
            avg_test_acc = test_acc / test_steps
        self.model.train()
        return avg_test_acc

    def train_one_epoch(self, epoch=None, num_epochs=None) -> None:
        """
        Trains the model for one epoch.
        :param epoch: (Optional) The current epoch number. (default: None)
        :param num_epochs: (Optional) The total number of epochs. (default: None)
        """
        self.model.train()
        running_loss = 0.0
        running_acc = 0.0
        steps = 0
        for _, keys_and_labels, ctxs, ctx_labels in tqdm(self.trainloader, desc="Processing Trainset"):
            keys = keys_and_labels[0]
            labels = keys_and_labels[1]
            ctx_labels = torch.stack(ctx_labels).T
            encoding = self.tokenizer(keys, add_special_tokens=True, padding="max_length", return_tensors="pt")
            inputs = encoding["input_ids"]
            mask = encoding["attention_mask"]
            if self.memory_dropout > 0.0:
                num_mems_max = 20  # TODO: factor out memory size as global a constant
                cutoff = int(num_mems_max * (1.0 - self.memory_dropout))
                filter = torch.randperm(num_mems_max)[:cutoff]
                ctxs = ctxs[:, filter, :]
                ctx_labels = ctx_labels[:, filter]
            inputs, mask, labels, ctxs, ctx_labels = (
                inputs.to(self.device),
                mask.to(self.device),
                labels.to(self.device),
                ctxs.to(self.device).to(self.dtype),
                ctx_labels.to(self.device),
            )
            self.optimizer.zero_grad()
            if self.use_memory:
                outputs = self.model(inputs, mask, ctxs, ctx_labels)
            else:
                outputs = self.model(inputs, mask)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item()
            running_acc += self._get_accuracy(outputs, labels)
            steps += 1
            if self.verbosity > 0 and steps % self.verbosity == 0:
                avg_loss = running_loss / steps
                avg_acc = running_acc / steps
                print(f"Epoch [{epoch}/{num_epochs}], Step [{steps}], Loss: {avg_loss:.4f}, Accuracy: {avg_acc:.4f}")

        avg_loss = running_loss / steps
        avg_acc = running_acc / steps
        print(
            f"Epoch [{epoch}/{num_epochs}], Loss: {avg_loss:.4f}, Accuracy: {avg_acc:.4f}, Test Accuracy: {self.get_test_accuracy():.4f}"
        )

    def train(self, num_epochs=10) -> None:
        """
        Trains the model for the given number of epochs.
        :param num_epochs: (Optional) The number of epochs to train for. (default: 10)
        """
        for epoch in range(num_epochs):
            self.train_one_epoch(epoch + 1, num_epochs)
