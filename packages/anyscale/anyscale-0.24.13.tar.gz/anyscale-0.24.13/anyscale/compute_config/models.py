from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, DefaultDict, Dict, List, Optional, Union

from anyscale._private.models import ModelBase


ResourceDict = Dict[str, float]
AdvancedInstanceConfigDict = Dict[str, Any]


def _validate_resource_dict(r: Optional[ResourceDict], *, field_name: str):
    if r is None:
        return

    if not isinstance(r, dict):
        raise TypeError(f"'{field_name}' must be a Dict[str, float], but got: {r}")

    for k, v in r.items():
        if not isinstance(k, str):
            raise TypeError(f"'{field_name}' keys must be strings, but got: {k}")
        if isinstance(v, (int, float)):
            if v < 0:
                raise ValueError(
                    f"'{field_name}' values must be >= 0, but got: '{k}: {v}'"
                )
        else:
            raise TypeError(
                f"'{field_name}' values must be floats, but got: '{k}: {v}'"
            )


def _validate_advanced_instance_config_dict(c: Optional[AdvancedInstanceConfigDict]):
    if c is None:
        return

    if not isinstance(c, dict) or not all(isinstance(k, str) for k in c):
        raise TypeError("'advanced_instance_config' must be a Dict[str, Any]")


@dataclass(frozen=True)
class _NodeConfig(ModelBase):
    instance_type: str = field()

    def _validate_instance_type(self, instance_type: str):
        if not isinstance(instance_type, str):
            raise TypeError("'instance_type' must be a string.")

    resources: Optional[ResourceDict] = field(default=None, repr=False)

    def _validate_resources(self, resources: Optional[ResourceDict]):
        _validate_resource_dict(resources, field_name="resources")

    advanced_instance_config: Optional[AdvancedInstanceConfigDict] = field(
        default=None, repr=False
    )

    def _validate_advanced_instance_config(
        self, advanced_instance_config: Optional[AdvancedInstanceConfigDict]
    ):
        _validate_advanced_instance_config_dict(advanced_instance_config)


@dataclass(frozen=True)
class HeadNodeConfig(_NodeConfig):
    pass


class MarketType(str, Enum):
    ON_DEMAND = "ON_DEMAND"
    SPOT = "SPOT"
    PREFER_SPOT = "PREFER_SPOT"

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class WorkerNodeGroupConfig(_NodeConfig):
    name: Optional[str] = field(default=None)

    def _validate_name(self, name: Optional[str]) -> str:
        # Default name to the instance type if not specified.
        if name is None:
            name = self.instance_type

        if not isinstance(name, str):
            raise TypeError("'name' must be a string")
        if len(name) == 0:
            raise ValueError("'name' cannot be empty")

        return name

    min_nodes: int = field(default=0)

    def _validate_min_nodes(self, min_nodes: int):
        if not isinstance(min_nodes, int):
            raise TypeError("'min_nodes' must be an int")
        if min_nodes < 0:
            raise ValueError("'min_nodes' must be >= 0")

    max_nodes: int = field(default=10)

    def _validate_max_nodes(self, max_nodes: int):
        if not isinstance(max_nodes, int):
            raise TypeError("'max_nodes' must be an int")
        if max_nodes < 1:
            raise ValueError("'max_nodes' must be >= 1")
        if max_nodes < self.min_nodes:
            raise ValueError(f"'max_nodes' must be >= 'min_nodes' ({self.min_nodes})")

    market_type: MarketType = field(default=MarketType.ON_DEMAND)

    def _validate_market_type(self, market_type: MarketType) -> MarketType:
        if isinstance(market_type, str):
            # This will raise a ValueError if the market_type is unrecognized.
            market_type = MarketType(market_type)
        elif not isinstance(market_type, MarketType):
            raise TypeError("'market_type' must be a MarketType.")

        return market_type


@dataclass(frozen=True)
class ComputeConfig(ModelBase):
    cloud: Optional[str] = field(default=None)

    def _validate_cloud(self, cloud: Optional[str]):
        if cloud is not None and not isinstance(cloud, str):
            raise TypeError("'cloud' must be a string")

    zones: Optional[List[str]] = field(default=None, repr=False)

    def _validate_zones(self, zones: Optional[List[str]]):
        if zones is None:
            return
        if not isinstance(zones, list) or not all(isinstance(z, str) for z in zones):
            raise TypeError("'zones' must be a List[str]")
        if len(zones) == 0:
            raise ValueError(
                "'zones' must not be an empty list. Set `None` to default to all zones."
            )

    enable_cross_zone_scaling: bool = field(default=False, repr=False)

    def _validate_enable_cross_zone_scaling(self, enable_cross_zone_scaling: bool):
        if not isinstance(enable_cross_zone_scaling, bool):
            raise TypeError("'enable_cross_zone_scaling' must be a boolean")

    max_resources: Optional[ResourceDict] = field(default=None, repr=False)

    def _validate_max_resources(self, max_resources: Optional[ResourceDict]):
        _validate_resource_dict(max_resources, field_name="max_resources")

    advanced_instance_config: Optional[AdvancedInstanceConfigDict] = field(
        default=None, repr=False
    )

    def _validate_advanced_instance_config(
        self, advanced_instance_config: Optional[AdvancedInstanceConfigDict],
    ):
        _validate_advanced_instance_config_dict(advanced_instance_config)

    head_node: Union[None, Dict, HeadNodeConfig] = field(default=None, repr=False)

    def _validate_head_node(
        self, head_node: Union[None, Dict, HeadNodeConfig]
    ) -> Optional[HeadNodeConfig]:
        if head_node is None:
            return None

        if isinstance(head_node, dict):
            head_node = HeadNodeConfig.from_dict(head_node)
        if not isinstance(head_node, HeadNodeConfig):
            raise TypeError(
                "'head_node' must be a HeadNodeConfig or corresponding dict"
            )

        return head_node

    worker_nodes: Optional[List[Union[Dict, WorkerNodeGroupConfig]]] = field(
        default=None, repr=False
    )

    def _validate_worker_nodes(
        self, worker_nodes: Optional[List[Union[Dict, WorkerNodeGroupConfig]]]
    ) -> Optional[List[WorkerNodeGroupConfig]]:
        if worker_nodes is None:
            return None

        if not isinstance(worker_nodes, list) or not all(
            isinstance(c, (dict, WorkerNodeGroupConfig)) for c in worker_nodes
        ):
            raise TypeError(
                "'worker_nodes' must be a list of WorkerNodeGroupConfigs or corresponding dicts"
            )

        duplicate_names = set()
        name_counts: DefaultDict[str, int] = defaultdict(int)
        worker_node_models: List[WorkerNodeGroupConfig] = []
        for node in worker_nodes:
            if isinstance(node, dict):
                node = WorkerNodeGroupConfig.from_dict(node)

            assert isinstance(node, WorkerNodeGroupConfig)
            worker_node_models.append(node)
            name = node.name
            assert name is not None
            name_counts[name] += 1
            if name_counts[name] > 1:
                duplicate_names.add(name)

        if duplicate_names:
            raise ValueError(
                f"'worker_nodes' names must be unique, but got duplicate names: {duplicate_names}"
            )

        return worker_node_models
