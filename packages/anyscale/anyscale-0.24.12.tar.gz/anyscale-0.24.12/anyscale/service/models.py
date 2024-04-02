from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from anyscale._private.models import ModelBase
from anyscale._private.workload import WorkloadConfig


@dataclass(frozen=True)
class RayGCSExternalStorageConfig(ModelBase):
    enabled: bool = True

    def _validate_enabled(self, enabled: bool):
        if not isinstance(enabled, bool):
            raise TypeError("'enabled' must be a boolean.")

    address: Optional[str] = None

    def _validate_address(self, address: Optional[str]):
        if address is not None and not isinstance(address, str):
            raise TypeError("'address' must be a string.")

    certificate_path: Optional[str] = None

    def _validate_certificate_path(self, certificate_path: Optional[str]):
        if certificate_path is not None and not isinstance(certificate_path, str):
            raise TypeError("'certificate_path' must be a string.")


@dataclass(frozen=True)
class ServiceConfig(WorkloadConfig):
    applications: List[Dict[str, Any]] = field(default_factory=list, repr=False)

    def _validate_applications(self, applications: List[Dict[str, Any]]):
        if not isinstance(applications, list):
            raise TypeError("'applications' must be a list.")
        if len(applications) == 0:
            raise ValueError("'applications' cannot be empty.")

        # Validate import paths.
        for app in applications:
            import_path = app.get("import_path", None)
            if not import_path:
                raise ValueError("Every application must specify an import path.")

            if not isinstance(import_path, str):
                raise TypeError(f"'import_path' must be a string, got: {import_path}")

            if (
                import_path.count(":") != 1
                or import_path.rfind(":") in {0, len(import_path) - 1}
                or import_path.rfind(".") in {0, len(import_path) - 1}
            ):
                raise ValueError(
                    f"'import_path' must be of the form: 'module.optional_submodule:app', but got: '{import_path}'."
                )

    query_auth_token_enabled: bool = field(default=True, repr=False)

    def _validate_query_auth_token_enabled(self, query_auth_token_enabled: bool):
        if not isinstance(query_auth_token_enabled, bool):
            raise TypeError("'query_auth_token_enabled' must be a boolean.")

    grpc_options: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def _validate_grpc_options(self, grpc_options: Optional[Dict[str, Any]]):
        """Validate the `grpc_options` field.

        This will be passed through as part of the Ray Serve config, but some fields are
        disallowed (not valid when deploying Anyscale services).
        """
        if grpc_options is None:
            return
        elif not isinstance(grpc_options, dict):
            raise TypeError("'grpc_options' must be a dict.")

        banned_options = {
            "port",
        }
        banned_options_passed = {o for o in banned_options if o in grpc_options}
        if len(banned_options_passed) > 0:
            raise ValueError(
                "The following provided 'grpc_options' are not permitted "
                f"in Anyscale: {banned_options_passed}."
            )

    http_options: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def _validate_http_options(self, http_options: Optional[Dict[str, Any]]):
        """Validate the `http_options` field.

        This will be passed through as part of the Ray Serve config, but some fields are
        disallowed (not valid when deploying Anyscale services).
        """
        if http_options is None:
            return
        elif not isinstance(http_options, dict):
            raise TypeError("'http_options' must be a dict.")

        banned_options = {"host", "port", "root_path"}
        banned_options_passed = {o for o in banned_options if o in http_options}
        if len(banned_options_passed) > 0:
            raise ValueError(
                "The following provided 'http_options' are not permitted "
                f"in Anyscale: {banned_options_passed}."
            )

    logging_config: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def _validate_logging_config(self, logging_config: Optional[Dict[str, Any]]):
        if logging_config is not None and not isinstance(logging_config, dict):
            raise TypeError("'logging_config' must be a dict.")

    ray_gcs_external_storage_config: Union[
        None, Dict, RayGCSExternalStorageConfig
    ] = field(default=None, repr=False)

    def _validate_ray_gcs_external_storage_config(
        self,
        ray_gcs_external_storage_config: Union[None, Dict, RayGCSExternalStorageConfig],
    ) -> Optional[RayGCSExternalStorageConfig]:
        if ray_gcs_external_storage_config is None:
            return None

        if isinstance(ray_gcs_external_storage_config, dict):
            ray_gcs_external_storage_config = RayGCSExternalStorageConfig.from_dict(
                ray_gcs_external_storage_config
            )

        if not isinstance(ray_gcs_external_storage_config, RayGCSExternalStorageConfig):
            raise TypeError(
                "'ray_gcs_external_storage_config' must be a RayGCSExternalStorageConfig or corresponding dict."
            )

        return ray_gcs_external_storage_config


class ServiceState(str, Enum):
    UNKNOWN = "UNKNOWN"
    STARTING = "STARTING"
    # TODO(edoakes): UPDATING comes up while rolling out and rolling back.
    # This is very unexpected from a customer's point of view, we should fix it.
    UPDATING = "UPDATING"
    ROLLING_OUT = "ROLLING_OUT"
    ROLLING_BACK = "ROLLING_BACK"
    RUNNING = "RUNNING"
    UNHEALTHY = "UNHEALTHY"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"

    def __str__(self):
        return self.name


class ServiceVersionState(str, Enum):
    UNKNOWN = "UNKNOWN"
    STARTING = "STARTING"
    UPDATING = "UPDATING"
    RUNNING = "RUNNING"
    UNHEALTHY = "UNHEALTHY"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"

    def __str__(self):
        return self.name


# TODO(edoakes): we should have a corresponding ServiceVersionState.
@dataclass(frozen=True)
class ServiceVersionStatus(ModelBase):
    name: str

    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("'name' must be a string.")

    state: ServiceVersionState

    def _validate_state(self, state: ServiceVersionState) -> ServiceVersionState:
        if isinstance(state, str):
            # This will raise a ValueError if the state is unrecognized.
            state = ServiceVersionState(state)
        elif not isinstance(state, ServiceVersionState):
            raise TypeError("'state' must be a ServiceVersionState.")

        return state

    weight: int

    def _validate_weight(self, weight: int):
        if not isinstance(weight, int):
            raise TypeError("'weight' must be an int.")

    config: Union[Dict, ServiceConfig] = field(repr=False)

    def _validate_config(self, config: Union[Dict, ServiceConfig]) -> ServiceConfig:
        if isinstance(config, dict):
            config = ServiceConfig.from_dict(config)

        if not isinstance(config, ServiceConfig):
            raise TypeError("'config' must be a ServiceConfig or corresponding dict.")

        return config


@dataclass(frozen=True)
class ServiceStatus(ModelBase):
    name: str

    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("'name' must be a string.")

    id: str

    def _validate_id(self, id: str):  # noqa: A002
        if not isinstance(id, str):
            raise TypeError("'id' must be a string.")

    state: ServiceState

    def _validate_state(self, state: ServiceState) -> ServiceState:
        if isinstance(state, str):
            # This will raise a ValueError if the state is unrecognized.
            state = ServiceState(state)
        elif not isinstance(state, ServiceState):
            raise TypeError("'state' must be a ServiceState.")

        return state

    query_url: str = field(repr=False)

    def _validate_query_url(self, query_url: str):
        if not isinstance(query_url, str):
            raise TypeError("'query_url' must be a string.")

    query_auth_token: Optional[str] = field(default=None, repr=False)

    def _validate_query_auth_token(self, query_auth_token: Optional[str]):
        if query_auth_token is not None and not isinstance(query_auth_token, str):
            raise TypeError("'query_auth_token' must be a string.")

    primary_version: Union[None, Dict, ServiceVersionStatus] = field(
        default=None, repr=False
    )

    def _validate_primary_version(
        self, primary_version: Union[None, Dict, ServiceVersionStatus]
    ) -> Optional[ServiceVersionStatus]:
        if primary_version is None:
            return None

        if isinstance(primary_version, dict):
            primary_version = ServiceVersionStatus.from_dict(primary_version)

        if not isinstance(primary_version, ServiceVersionStatus):
            raise TypeError(
                "'primary_version' must be a ServiceVersionStatus or corresponding dict."
            )

        return primary_version

    canary_version: Union[None, Dict, ServiceVersionStatus] = field(
        default=None, repr=False
    )

    def _validate_canary_version(
        self, canary_version: Union[None, Dict, ServiceVersionStatus]
    ) -> Optional[ServiceVersionStatus]:
        if canary_version is None:
            return None

        if isinstance(canary_version, dict):
            canary_version = ServiceVersionStatus.from_dict(canary_version)

        if not isinstance(canary_version, ServiceVersionStatus):
            raise TypeError(
                "'canary_version' must be a ServiceVersionStatus or corresponding dict."
            )

        return canary_version
