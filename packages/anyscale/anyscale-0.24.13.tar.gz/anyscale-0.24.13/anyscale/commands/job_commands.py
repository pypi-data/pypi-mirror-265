import pathlib
from subprocess import list2cmdline
from typing import Optional, Tuple

import click

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import HaJobStates
from anyscale.controllers.job_controller import JobController
from anyscale.job.models import JobConfig
from anyscale.util import validate_non_negative_arg


log = BlockLogger()  # CLI Logger


@click.group("job", help="Interact with production jobs running on Anyscale.")
def job_cli() -> None:
    pass


@job_cli.command(
    name="submit", short_help="Submit a job.",
)
@click.option("--name", "-n", required=False, default=None, help="Name of the job.")
@click.option(
    "--description", required=False, default=None, help="Description of the job."
)
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log of the created job",
)
@click.option(
    "--wait",
    "-w",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to block this CLI command until the job succeeds (or reaches another terminal state)",
)
@click.option(
    "--config-file",
    required=False,
    default=None,
    type=str,
    help="Path to a YAML config file to use for this job. Command-line flags will overwrite values read from the file.",
)
@click.option(
    "--image-uri",
    required=False,
    default=None,
    type=str,
    help="Container image to use for this job. When running in a workspace, this defaults to the image of the workspace.",
)
@click.option(
    "--containerfile",
    required=False,
    default=None,
    type=str,
    help="Path to a containerfile to build the image to use for the job. This is exclusive with --image-uri.",
)
@click.argument("entrypoint", required=False, nargs=-1, type=click.UNPROCESSED)
def submit(  # noqa: PLR0912 PLR0913 C901
    entrypoint: Tuple[str],
    name: Optional[str],
    description: Optional[str],
    follow: Optional[bool],
    wait: Optional[bool],
    config_file: Optional[str],
    image_uri: Optional[str],
    containerfile: Optional[str],
):
    """Submit a job.

    The job config can be specified in one of the following ways:
    * Job config can be specified with command-line arguments. In this case, the
      entrypoint should be specified as the positional arguments starting with `--`.
      Other arguments can be specified with command-line flags. E.g.
      * `anyscale job submit -- python main.py`: submit a job with the entrypoint `python main.py`.
      * `anyscale job submit --name my-job -- python main.py`: submit a job with the name `my-job` and the
        entrypoint `python main.py`.
    * Job config can also be specified in a YAML file with the `--config-file` flag.
      In this case, you can still override arguments with command-line flags. E.g.
      * `anyscale job submit --config-file config.yaml`: submit a job with the config in `config.yaml`.
      * `anyscale job submit --config-file config.yaml -- python main.py`: submit a job with the config in `config.yaml`
        and override the entrypoint with `python main.py`.
    * [Deprecated] If the positional argument is a single string that ends with .yaml, this is treated as a config file.
      E.g. `anyscale job submit config.yaml`.

    By default, this command submits the job asynchronously and exits. To wait for the job to complete, use the `--wait` flag.
    """

    job_controller = JobController()
    if len(entrypoint) == 1 and entrypoint[0].endswith(".yaml"):
        # If entrypoint is a single string that ends with .yaml, e.g. `anyscale job submit config.yaml`,
        # treat it as a config file, and use the old job submission API.
        if config_file is not None:
            raise click.ClickException(
                "`--config-file` should not be used when providing a config file as the entrypoint."
            )
        if image_uri:
            raise click.ClickException(
                "`--image-uri` should not be used when providing a config file as the entrypoint."
            )
        if containerfile:
            raise click.ClickException(
                "`--containerfile` should not be used when providing a config file as the entrypoint."
            )

        config_file = entrypoint[0]
        if not pathlib.Path(config_file).is_file():
            raise click.ClickException(f"Job config file '{config_file}' not found.")
        log.info(f"Submitting job from config file {config_file}.")

        job_id = job_controller.submit(config_file, name=name, description=description,)
    else:
        # Otherwise, use the new job submission API. E.g.
        # `anyscale job submit -- python main.py`,
        # or `anyscale job submit --config-file config.yaml`.
        if len(entrypoint) == 0 and config_file is None:
            raise click.ClickException(
                "Either a config file or an inlined entrypoint must be provided."
            )
        if config_file is not None and not pathlib.Path(config_file).is_file():
            raise click.ClickException(f"Job config file '{config_file}' not found.")
        if follow:
            log.warning("`--follow` is deprecated, use `--wait` instead.")

        args = {}
        if len(entrypoint) > 0:
            args["entrypoint"] = list2cmdline(entrypoint)
        if name:
            args["name"] = name
        if description:
            args["description"] = description

        if containerfile and image_uri:
            raise click.ClickException(
                "Only one of '--containerfile' and '--image-uri' can be provided."
            )

        if image_uri:
            args["image_uri"] = image_uri

        if containerfile:
            args["containerfile"] = containerfile

        if config_file is not None:
            config = JobConfig.from_yaml(config_file, **args)
        else:
            config = JobConfig.from_dict(args)
        log.info(f"Submitting job with config {config}.")
        job_id = anyscale.job.submit(config)

    if follow or wait:
        job_controller.log.info(
            "Waiting for the job to run. Interrupting this command will not cancel the job."
        )
    else:
        job_controller.log.info(
            "Use `--wait` to wait for the job to run and stream logs."
        )

    if follow:
        job_controller.logs(job_id, should_follow=follow)
    if wait:
        job_controller.wait(job_id=job_id)


@job_cli.command(name="list", help="Display information about existing jobs.")
@click.option("--name", "-n", required=False, default=None, help="Filter by job name.")
@click.option(
    "--job-id", "--id", required=False, default=None, help="Filter by job id."
)
@click.option(
    "--project-id", required=False, default=None, help="Filter by project id."
)
@click.option(
    "--include-all-users",
    is_flag=True,
    default=False,
    help="Include jobs not created by current user.",
)
@click.option(
    "--include-archived",
    is_flag=True,
    default=False,
    help=(
        "List archived jobs as well as unarchived jobs."
        "If not provided, defaults to listing only unarchived jobs."
    ),
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(  # noqa: A001
    name: Optional[str],
    job_id: Optional[str],
    project_id: Optional[str],
    include_all_users: bool,
    include_archived: bool,
    max_items: int,
) -> None:
    job_controller = JobController()
    job_controller.list(
        name=name,
        job_id=job_id,
        project_id=project_id,
        include_all_users=include_all_users,
        include_archived=include_archived,
        max_items=max_items,
    )


@job_cli.command(name="archive", help="Archive a job.")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
def archive(job_id: Optional[str], name: Optional[str]) -> None:
    job_controller = JobController()
    job_controller.archive(job_id=job_id, job_name=name)


@job_cli.command(name="terminate", help="Attempt to terminate a job asynchronously.")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
def terminate(job_id: Optional[str], name: Optional[str]) -> None:
    job_controller = JobController()
    job_controller.terminate(job_id=job_id, job_name=name)


@job_cli.command(name="logs")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log.",
)
@click.option(
    "--all-attempts",
    is_flag=True,
    default=False,
    help="Show logs for all job attempts.",
)
def logs(
    job_id: Optional[str],
    name: Optional[str],
    follow: bool = False,
    all_attempts: bool = False,
) -> None:
    """Print the logs of a job.

    By default from the latest job attempt.

    Example usage:

        anyscale job logs --id prodjob_123

        anyscale job logs --id prodjob_123 -f

        anyscale job logs -n my-job --all-attempts"""
    job_controller = JobController(raise_structured_exception=True)
    job_controller.logs(
        job_id=job_id, job_name=name, should_follow=follow, all_attempts=all_attempts,
    )


@job_cli.command(name="wait")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--state",
    "-s",
    required=False,
    default=HaJobStates.SUCCESS,
    help="The state to wait for this Job to enter",
)
@click.option(
    "--timeout",
    "-t",
    required=False,
    default=None,
    type=float,
    help="The timeout in seconds after which this command will exit.",
)
def wait(
    job_id: Optional[str],
    name: Optional[str],
    state: str = HaJobStates.SUCCESS,
    timeout=None,
) -> None:
    """Wait for a Job to enter a specific state (default: SUCCESS).

    To specify the Job by name, use the --name flag. To specify the Job by id, use the --job-id flag.

    If the Job reaches the target state, the command will exit successfully.

    If the Job reaches a terminal state other than the target state, the command will exit with an error.

    If the command reaches the timeout, the command will exit with an error.
    """
    state = state.upper()
    job_controller = JobController()
    job_id = job_controller.wait(
        job_id=job_id, job_name=name, target_state=state, timeout_secs=timeout,
    )
