from dataclasses import dataclass, field
from typing import Optional

from anyscale._private.workload import WorkloadConfig


@dataclass(frozen=True)
class JobConfig(WorkloadConfig):
    """Configuration options for a job."""

    # Override the `name` field from `WorkloadConfig` so we can document it separately for jobs and services.
    name: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Name of the job. Multiple jobs can be submitted with the same name."
        },
    )

    description: Optional[str] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Description of the job that can be viewed in the UI or status output."
        },
    )

    def _validate_description(self, description: Optional[str]):
        if description is not None and not isinstance(description, str):
            raise TypeError("'description' must be a string.")

    entrypoint: str = field(
        default="",
        repr=False,
        metadata={
            "docstring": "Command that will be run to execute the job, e.g., `python main.py`."
        },
    )

    def _validate_entrypoint(self, entrypoint: str):
        if not isinstance(entrypoint, str):
            raise TypeError("'entrypoint' must be a string.")

        if not entrypoint:
            raise ValueError("'entrypoint' cannot be empty.")

    max_retries: int = field(
        default=1,
        repr=False,
        metadata={
            "docstring": "Maximum number of times the job will be retried before being marked failed. Defaults to `1`."
        },
    )

    def _validate_max_retries(self, max_retries: int):
        if not isinstance(max_retries, int):
            raise TypeError("'max_retries' must be an int.")

        if max_retries < 0:
            raise ValueError("'max_retries' must be >= 0.")
