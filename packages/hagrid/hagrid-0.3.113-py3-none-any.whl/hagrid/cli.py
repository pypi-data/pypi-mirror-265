# stdlib
from collections import namedtuple
from collections.abc import Callable
from enum import Enum
import json
import os
from pathlib import Path
import platform
from queue import Queue
import re
import shutil
import socket
import stat
import subprocess  # nosec
import sys
import tempfile
from threading import Event
from threading import Thread
import time
from typing import Any
from typing import cast
from urllib.parse import urlparse
import webbrowser

# third party
import click
import requests
import rich
from rich.console import Console
from rich.live import Live
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn
from virtualenvapi.manage import VirtualEnvironment

# relative
from .art import RichEmoji
from .art import hagrid
from .art import quickstart_art
from .auth import AuthCredentials
from .cache import DEFAULT_BRANCH
from .cache import DEFAULT_REPO
from .cache import arg_cache
from .deps import DEPENDENCIES
from .deps import LATEST_BETA_SYFT
from .deps import allowed_hosts
from .deps import check_docker_service_status
from .deps import check_docker_version
from .deps import check_grid_docker
from .deps import gather_debug
from .deps import get_version_string
from .deps import is_windows
from .exceptions import MissingDependency
from .grammar import BadGrammar
from .grammar import GrammarVerb
from .grammar import parse_grammar
from .land import get_land_verb
from .launch import get_launch_verb
from .lib import GIT_REPO
from .lib import GRID_SRC_PATH
from .lib import GRID_SRC_VERSION
from .lib import check_api_metadata
from .lib import check_host
from .lib import check_jupyter_server
from .lib import check_login_page
from .lib import commit_hash
from .lib import docker_desktop_memory
from .lib import find_available_port
from .lib import generate_process_status_table
from .lib import generate_user_table
from .lib import gitpod_url
from .lib import hagrid_root
from .lib import is_gitpod
from .lib import name_tag
from .lib import save_vm_details_as_json
from .lib import update_repo
from .lib import use_branch
from .mode import EDITABLE_MODE
from .parse_template import deployment_dir
from .parse_template import get_template_yml
from .parse_template import manifest_cache_path
from .parse_template import render_templates
from .parse_template import setup_from_manifest_template
from .quickstart_ui import fetch_notebooks_for_url
from .quickstart_ui import fetch_notebooks_from_zipfile
from .quickstart_ui import quickstart_download_notebook
from .rand_sec import generate_sec_random_password
from .stable_version import LATEST_STABLE_SYFT
from .style import RichGroup
from .util import fix_windows_virtualenv_api
from .util import from_url
from .util import shell

# fix VirtualEnvironment bug in windows
fix_windows_virtualenv_api(VirtualEnvironment)


class NodeSideType(Enum):
    LOW_SIDE = "low"
    HIGH_SIDE = "high"


def get_azure_image(short_name: str) -> str:
    prebuild_070 = (
        "madhavajay1632269232059:openmined_mj_grid_domain_ubuntu_1:domain_070:latest"
    )
    fresh_ubuntu = "Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest"
    if short_name == "default":
        return fresh_ubuntu
    elif short_name == "domain_0.7.0":
        return prebuild_070
    raise Exception(f"Image name doesn't exist: {short_name}. Try: default or 0.7.0")


@click.group(cls=RichGroup)
def cli() -> None:
    pass


def get_compose_src_path(
    node_name: str,
    template_location: str | None = None,
    **kwargs: Any,
) -> str:
    grid_path = GRID_SRC_PATH()
    tag = kwargs["tag"]
    # Use local compose files if in editable mode and
    # template_location is None and (kwargs["dev"] is True or tag is local)
    if (
        EDITABLE_MODE
        and template_location is None
        and (kwargs["dev"] is True or tag == "local")
    ):
        path = grid_path
    else:
        path = deployment_dir(node_name)

    os.makedirs(path, exist_ok=True)
    return path


@click.command(
    help="Restore some part of the hagrid installation or deployment to its initial/starting state.",
    context_settings={"show_default": True},
)
@click.argument("location", type=str, nargs=1)
def clean(location: str) -> None:
    if location == "library" or location == "volumes":
        print("Deleting all Docker volumes in 2 secs (Ctrl-C to stop)")
        time.sleep(2)
        subprocess.call("docker volume rm $(docker volume ls -q)", shell=True)  # nosec

    if location == "containers" or location == "pantry":
        print("Deleting all Docker containers in 2 secs (Ctrl-C to stop)")
        time.sleep(2)
        subprocess.call("docker rm -f $(docker ps -a -q)", shell=True)  # nosec

    if location == "images":
        print("Deleting all Docker images in 2 secs (Ctrl-C to stop)")
        time.sleep(2)
        subprocess.call("docker rmi $(docker images -q)", shell=True)  # nosec


@click.command(
    help="Start a new PyGrid domain/network node!",
    context_settings={"show_default": True},
)
@click.argument("args", type=str, nargs=-1)
@click.option(
    "--username",
    default=None,
    required=False,
    type=str,
    help="Username for provisioning the remote host",
)
@click.option(
    "--key-path",
    default=None,
    required=False,
    type=str,
    help="Path to the key file for provisioning the remote host",
)
@click.option(
    "--password",
    default=None,
    required=False,
    type=str,
    help="Password for provisioning the remote host",
)
@click.option(
    "--repo",
    default=None,
    required=False,
    type=str,
    help="Repo to fetch source from",
)
@click.option(
    "--branch",
    default=None,
    required=False,
    type=str,
    help="Branch to monitor for updates",
)
@click.option(
    "--tail",
    is_flag=True,
    help="Tail logs on launch",
)
@click.option(
    "--headless",
    is_flag=True,
    help="Start the frontend container",
)
@click.option(
    "--cmd",
    is_flag=True,
    help="Print the cmd without running it",
)
@click.option(
    "--jupyter",
    is_flag=True,
    help="Enable Jupyter Notebooks",
)
@click.option(
    "--in-mem-workers",
    is_flag=True,
    help="Enable InMemory Workers",
)
@click.option(
    "--enable-signup",
    is_flag=True,
    help="Enable Signup for Node",
)
@click.option(
    "--build",
    is_flag=True,
    help="Disable forcing re-build",
)
@click.option(
    "--no-provision",
    is_flag=True,
    help="Disable provisioning VMs",
)
@click.option(
    "--node-count",
    default=1,
    required=False,
    type=click.IntRange(1, 250),
    help="Number of independent nodes/VMs to launch",
)
@click.option(
    "--auth-type",
    default=None,
    type=click.Choice(["key", "password"], case_sensitive=False),
)
@click.option(
    "--ansible-extras",
    default="",
    type=str,
)
@click.option("--tls", is_flag=True, help="Launch with TLS configuration")
@click.option("--test", is_flag=True, help="Launch with test configuration")
@click.option("--dev", is_flag=True, help="Shortcut for development mode")
@click.option(
    "--release",
    default="production",
    required=False,
    type=click.Choice(["production", "staging", "development"], case_sensitive=False),
    help="Choose between production and development release",
)
@click.option(
    "--deployment-type",
    default="container_stack",
    required=False,
    type=click.Choice(["container_stack", "single_container"], case_sensitive=False),
    help="Choose between container_stack and single_container deployment",
)
@click.option(
    "--cert-store-path",
    default="/home/om/certs",
    required=False,
    type=str,
    help="Remote path to store and load TLS cert and key",
)
@click.option(
    "--upload-tls-cert",
    default="",
    required=False,
    type=str,
    help="Local path to TLS cert to upload and store at --cert-store-path",
)
@click.option(
    "--upload-tls-key",
    default="",
    required=False,
    type=str,
    help="Local path to TLS private key to upload and store at --cert-store-path",
)
@click.option(
    "--no-blob-storage",
    is_flag=True,
    help="Disable blob storage",
)
@click.option(
    "--image-name",
    default=None,
    required=False,
    type=str,
    help="Image to use for the VM",
)
@click.option(
    "--tag",
    default=None,
    required=False,
    type=str,
    help="Container image tag to use",
)
@click.option(
    "--smtp-username",
    default=None,
    required=False,
    type=str,
    help="Username used to auth in email server and enable notification via emails",
)
@click.option(
    "--smtp-password",
    default=None,
    required=False,
    type=str,
    help="Password used to auth in email server and enable notification via emails",
)
@click.option(
    "--smtp-port",
    default=None,
    required=False,
    type=str,
    help="Port used by email server to send notification via emails",
)
@click.option(
    "--smtp-host",
    default=None,
    required=False,
    type=str,
    help="Address used by email server to send notification via emails",
)
@click.option(
    "--smtp-sender",
    default=None,
    required=False,
    type=str,
    help="Sender email used to deliver PyGrid email notifications.",
)
@click.option(
    "--build-src",
    default=DEFAULT_BRANCH,
    required=False,
    type=str,
    help="Git branch to use for launch / build operations",
)
@click.option(
    "--platform",
    default=None,
    required=False,
    type=str,
    help="Run docker with a different platform like linux/arm64",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show verbose output",
)
@click.option(
    "--trace",
    required=False,
    type=str,
    help="Optional: allow trace to be turned on or off",
)
@click.option(
    "--template",
    required=False,
    default=None,
    help="Path or URL to manifest template",
)
@click.option(
    "--template-overwrite",
    is_flag=True,
    help="Force re-downloading of template manifest",
)
@click.option(
    "--no-health-checks",
    is_flag=True,
    help="Turn off auto health checks post node launch",
)
@click.option(
    "--oblv",
    is_flag=True,
    help="Installs Oblivious CLI tool",
)
@click.option(
    "--set-root-email",
    default=None,
    required=False,
    type=str,
    help="Set root email of node",
)
@click.option(
    "--set-root-password",
    default=None,
    required=False,
    type=str,
    help="Set root password of node",
)
@click.option(
    "--azure-resource-group",
    default=None,
    required=False,
    type=str,
    help="Azure Resource Group",
)
@click.option(
    "--azure-location",
    default=None,
    required=False,
    type=str,
    help="Azure Resource Group Location",
)
@click.option(
    "--azure-size",
    default=None,
    required=False,
    type=str,
    help="Azure VM Size",
)
@click.option(
    "--azure-username",
    default=None,
    required=False,
    type=str,
    help="Azure VM Username",
)
@click.option(
    "--azure-key-path",
    default=None,
    required=False,
    type=str,
    help="Azure Key Path",
)
@click.option(
    "--azure-repo",
    default=None,
    required=False,
    type=str,
    help="Azure Source Repo",
)
@click.option(
    "--azure-branch",
    default=None,
    required=False,
    type=str,
    help="Azure Source Branch",
)
@click.option(
    "--render",
    is_flag=True,
    help="Render Docker Files",
)
@click.option(
    "--no-warnings",
    is_flag=True,
    help="Enable API warnings on the node.",
)
@click.option(
    "--low-side",
    is_flag=True,
    help="Launch a low side node type else a high side node type",
)
@click.option(
    "--set-s3-username",
    default=None,
    required=False,
    type=str,
    help="Set root username for s3 blob storage",
)
@click.option(
    "--set-s3-password",
    default=None,
    required=False,
    type=str,
    help="Set root password for s3 blob storage",
)
@click.option(
    "--set-volume-size-limit-mb",
    default=1024,
    required=False,
    type=click.IntRange(1024, 50000),
    help="Set the volume size limit (in MBs)",
)
def launch(args: tuple[str], **kwargs: Any) -> None:
    verb = get_launch_verb()
    try:
        grammar = parse_grammar(args=args, verb=verb)
        verb.load_grammar(grammar=grammar)
    except BadGrammar as e:
        print(e)
        return

    node_name = verb.get_named_term_type(name="node_name")
    snake_name = str(node_name.snake_input)
    node_type = verb.get_named_term_type(name="node_type")

    # For enclave currently it is only a single container deployment
    # This would change when we have side car containers to enclave
    if node_type.input == "enclave":
        kwargs["deployment_type"] = "single_container"

    compose_src_path = get_compose_src_path(
        node_type=node_type,
        node_name=snake_name,
        template_location=kwargs["template"],
        **kwargs,
    )
    kwargs["compose_src_path"] = compose_src_path

    try:
        update_repo(repo=GIT_REPO(), branch=str(kwargs["build_src"]))
    except Exception as e:
        print(f"Failed to update repo. {e}")
    try:
        cmds = create_launch_cmd(verb=verb, kwargs=kwargs)
        cmds = [cmds] if isinstance(cmds, str) else cmds
    except Exception as e:
        print(f"Error: {e}\n\n")
        return

    dry_run = bool(kwargs["cmd"])

    health_checks = not bool(kwargs["no_health_checks"])
    render_only = bool(kwargs["render"])

    try:
        tail = bool(kwargs["tail"])
        verbose = bool(kwargs["verbose"])
        silent = not verbose
        if tail:
            silent = False

        if render_only:
            print(
                "Docker Compose Files Rendered: {}".format(kwargs["compose_src_path"])
            )
            return

        execute_commands(
            cmds,
            dry_run=dry_run,
            silent=silent,
            compose_src_path=kwargs["compose_src_path"],
            node_type=node_type.input,
        )

        host_term = verb.get_named_term_hostgrammar(name="host")
        run_health_checks = (
            health_checks and not dry_run and host_term.host == "docker" and silent
        )

        if run_health_checks:
            docker_cmds = cast(dict[str, list[str]], cmds)

            # get the first command (cmd1) from docker_cmds which is of the form
            # {"<first>": [cmd1, cmd2], "<second>": [cmd3, cmd4]}
            (command, *_), *_ = docker_cmds.values()

            match_port = re.search("HTTP_PORT=[0-9]{1,5}", command)
            if match_port:
                rich.get_console().print(
                    "\n[bold green]⠋[bold blue] Checking node API [/bold blue]\t"
                )
                port = match_port.group().replace("HTTP_PORT=", "")

                check_status("localhost" + ":" + port, node_name=node_name.snake_input)

            rich.get_console().print(
                rich.panel.Panel.fit(
                    f"✨ To view container logs run [bold green]hagrid logs {node_name.snake_input}[/bold green]\t"
                )
            )

    except Exception as e:
        print(f"Error: {e}\n\n")
        return


def check_errors(
    line: str, process: subprocess.Popen, cmd_name: str, progress_bar: Progress
) -> None:
    task = progress_bar.tasks[0]
    if "Error response from daemon: " in line:
        if progress_bar:
            progress_bar.update(
                0,
                description=f"❌ [bold red]{cmd_name}[/bold red] [{task.completed} / {task.total}]",
                refresh=True,
            )
            progress_bar.update(0, visible=False)
            progress_bar.console.clear_live()
            progress_bar.console.quiet = True
            progress_bar.stop()
            console = rich.get_console()
            progress_bar.console.quiet = False
            console.print(f"\n\n [red] ERROR [/red]: [bold]{line}[/bold]\n")
        process.terminate()
        raise Exception


def check_pulling(line: str, cmd_name: str, progress_bar: Progress) -> None:
    task = progress_bar.tasks[0]
    if "Pulling" in line and "fs layer" not in line:
        progress_bar.update(
            0,
            description=f"[bold]{cmd_name} [{task.completed} / {task.total+1}]",
            total=task.total + 1,
            refresh=True,
        )
    if "Pulled" in line:
        progress_bar.update(
            0,
            description=f"[bold]{cmd_name} [{task.completed + 1} / {task.total}]",
            completed=task.completed + 1,
            refresh=True,
        )
        if progress_bar.finished:
            progress_bar.update(
                0,
                description=f"✅ [bold green]{cmd_name} [{task.completed} / {task.total}]",
                refresh=True,
            )


def check_building(line: str, cmd_name: str, progress_bar: Progress) -> None:
    load_pattern = re.compile(
        r"^#.* load build definition from [A-Za-z0-9]+\.dockerfile$", re.IGNORECASE
    )
    build_pattern = re.compile(
        r"^#.* naming to docker\.io/openmined/.* done$", re.IGNORECASE
    )
    task = progress_bar.tasks[0]

    if load_pattern.match(line):
        progress_bar.update(
            0,
            description=f"[bold]{cmd_name} [{task.completed} / {task.total +1}]",
            total=task.total + 1,
            refresh=True,
        )
    if build_pattern.match(line):
        progress_bar.update(
            0,
            description=f"[bold]{cmd_name} [{task.completed+1} / {task.total}]",
            completed=task.completed + 1,
            refresh=True,
        )

    if progress_bar.finished:
        progress_bar.update(
            0,
            description=f"✅ [bold green]{cmd_name} [{task.completed} / {task.total}]",
            refresh=True,
        )


def check_launching(line: str, cmd_name: str, progress_bar: Progress) -> None:
    task = progress_bar.tasks[0]
    if "Starting" in line:
        progress_bar.update(
            0,
            description=f" [bold]{cmd_name} [{task.completed} / {task.total+1}]",
            total=task.total + 1,
            refresh=True,
        )
    if "Started" in line:
        progress_bar.update(
            0,
            description=f" [bold]{cmd_name} [{task.completed + 1} / {task.total}]",
            completed=task.completed + 1,
            refresh=True,
        )
        if progress_bar.finished:
            progress_bar.update(
                0,
                description=f"✅ [bold green]{cmd_name} [{task.completed} / {task.total}]",
                refresh=True,
            )


DOCKER_FUNC_MAP = {
    "Pulling": check_pulling,
    "Building": check_building,
    "Launching": check_launching,
}


def read_thread_logs(
    progress_bar: Progress, process: subprocess.Popen, queue: Queue, cmd_name: str
) -> None:
    line = queue.get()
    line = str(line, encoding="utf-8").strip()

    if progress_bar:
        check_errors(line, process, cmd_name, progress_bar=progress_bar)
        DOCKER_FUNC_MAP[cmd_name](line, cmd_name, progress_bar=progress_bar)


def create_thread_logs(process: subprocess.Popen) -> Queue:
    def enqueue_output(out: Any, queue: Queue) -> None:
        for line in iter(out.readline, b""):
            queue.put(line)
        out.close()

    queue: Queue = Queue()
    thread_1 = Thread(target=enqueue_output, args=(process.stdout, queue))
    thread_2 = Thread(target=enqueue_output, args=(process.stderr, queue))

    thread_1.daemon = True  # thread dies with the program
    thread_1.start()
    thread_2.daemon = True  # thread dies with the program
    thread_2.start()
    return queue


def process_cmd(
    cmds: list[str],
    node_type: str,
    dry_run: bool,
    silent: bool,
    compose_src_path: str,
    progress_bar: Progress | None = None,
    cmd_name: str = "",
) -> None:
    process_list: list = []
    cwd = compose_src_path

    username, password = (
        extract_username_and_pass(cmds[0]) if len(cmds) > 0 else ("-", "-")
    )
    # display VM credentials
    console = rich.get_console()
    credentials = generate_user_table(username=username, password=password)
    if credentials:
        console.print(credentials)

    for cmd in cmds:
        if dry_run:
            print(f"\nRunning:\ncd {cwd}\n", hide_password(cmd=cmd))
            continue

        # use powershell if environment is Windows
        cmd_to_exec = ["powershell.exe", "-Command", cmd] if is_windows() else cmd

        try:
            if len(cmds) > 1:
                process = subprocess.Popen(  # nosec
                    cmd_to_exec,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=cwd,
                    shell=True,
                )
                ip_address = extract_host_ip_from_cmd(cmd)
                jupyter_token = extract_jupyter_token(cmd)
                process_list.append((ip_address, process, jupyter_token))
            else:
                display_jupyter_token(cmd)
                if silent:
                    ON_POSIX = "posix" in sys.builtin_module_names

                    process = subprocess.Popen(  # nosec
                        cmd_to_exec,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=cwd,
                        close_fds=ON_POSIX,
                        shell=True,
                    )

                    # Creates two threads to get docker stdout and sterr
                    logs_queue = create_thread_logs(process=process)

                    read_thread_logs(progress_bar, process, logs_queue, cmd_name)
                    while process.poll() != 0:
                        while not logs_queue.empty():
                            # Read stdout and sterr to check errors or update progress bar.
                            read_thread_logs(
                                progress_bar, process, logs_queue, cmd_name
                            )
                else:
                    if progress_bar:
                        progress_bar.stop()

                    subprocess.run(  # nosec
                        cmd_to_exec,
                        shell=True,
                        cwd=cwd,
                    )
        except Exception as e:
            print(f"Failed to run cmd: {cmd}. {e}")

    if dry_run is False and len(process_list) > 0:
        # display VM launch status
        display_vm_status(process_list)

        # save vm details as json
        save_vm_details_as_json(username, password, process_list)


def execute_commands(
    cmds: list[str] | dict[str, list[str]],
    node_type: str,
    compose_src_path: str,
    dry_run: bool = False,
    silent: bool = False,
) -> None:
    """Execute the launch commands and display their status in realtime.

    Args:
        cmds (list): list of commands to be executed
        dry_run (bool, optional): If `True` only displays cmds to be executed. Defaults to False.
    """
    console = rich.get_console()
    if isinstance(cmds, dict):
        console.print("[bold green]⠋[bold blue] Launching Containers [/bold blue]\t")
        for cmd_name, cmd in cmds.items():
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:.2f}%   "),
                console=console,
                auto_refresh=True,
            ) as progress:
                if silent:
                    progress.add_task(
                        f"[bold green]{cmd_name} Images",
                        total=0,
                    )
                process_cmd(
                    cmds=cmd,
                    node_type=node_type,
                    dry_run=dry_run,
                    silent=silent,
                    compose_src_path=compose_src_path,
                    progress_bar=progress,
                    cmd_name=cmd_name,
                )
    else:
        process_cmd(
            cmds=cmds,
            node_type=node_type,
            dry_run=dry_run,
            silent=silent,
            compose_src_path=compose_src_path,
        )


def display_vm_status(process_list: list) -> None:
    """Display the status of the processes being executed on the VM.

    Args:
        process_list (list): list of processes executed.
    """

    # Generate the table showing the status of each process being executed
    status_table, process_completed = generate_process_status_table(process_list)

    # Render the live table
    with Live(status_table, refresh_per_second=1) as live:
        # Loop till all processes have not completed executing
        while not process_completed:
            status_table, process_completed = generate_process_status_table(
                process_list
            )
            live.update(status_table)  # Update the process status table


def display_jupyter_token(cmd: str) -> None:
    token = extract_jupyter_token(cmd=cmd)
    if token is not None:
        print(f"Jupyter Token: {token}")


def extract_username_and_pass(cmd: str) -> tuple:
    # Extract username
    matcher = r"--user (.+?) "
    username = re.findall(matcher, cmd)
    username = username[0] if len(username) > 0 else None

    # Extract password
    matcher = r"ansible_ssh_pass='(.+?)'"
    password = re.findall(matcher, cmd)
    password = password[0] if len(password) > 0 else None

    return username, password


def extract_jupyter_token(cmd: str) -> str | None:
    matcher = r"jupyter_token='(.+?)'"
    token = re.findall(matcher, cmd)
    if len(token) == 1:
        return token[0]
    return None


def hide_password(cmd: str) -> str:
    try:
        matcher = r"ansible_ssh_pass='(.+?)'"
        passwords = re.findall(matcher, cmd)
        if len(passwords) > 0:
            password = passwords[0]
            stars = "*" * 4
            cmd = cmd.replace(
                f"ansible_ssh_pass='{password}'", f"ansible_ssh_pass='{stars}'"
            )
        return cmd
    except Exception as e:
        print("Failed to hide password.")
        raise e


def hide_azure_vm_password(azure_cmd: str) -> str:
    try:
        matcher = r"admin-password '(.+?)'"
        passwords = re.findall(matcher, azure_cmd)
        if len(passwords) > 0:
            password = passwords[0]
            stars = "*" * 4
            azure_cmd = azure_cmd.replace(
                f"admin-password '{password}'", f"admin-password '{stars}'"
            )
        return azure_cmd
    except Exception as e:
        print("Failed to hide password.")
        raise e


class QuestionInputError(Exception):
    pass


class QuestionInputPathError(Exception):
    pass


class Question:
    def __init__(
        self,
        var_name: str,
        question: str,
        kind: str,
        default: str | None = None,
        cache: bool = False,
        options: list[str] | None = None,
    ) -> None:
        self.var_name = var_name
        self.question = question
        self.default = default
        self.kind = kind
        self.cache = cache
        self.options = options if options is not None else []

    def validate(self, value: str) -> str:
        value = value.strip()
        if self.default is not None and value == "":
            return self.default

        if self.kind == "path":
            value = os.path.expanduser(value)
            if not os.path.exists(value):
                error = f"{value} is not a valid path."
                if self.default is not None:
                    error += f" Try {self.default}"
                raise QuestionInputPathError(f"{error}")

        if self.kind == "yesno":
            if value.lower().startswith("y"):
                return "y"
            elif value.lower().startswith("n"):
                return "n"
            else:
                raise QuestionInputError(f"{value} is not an yes or no answer")

        if self.kind == "options":
            if value in self.options:
                return value
            first_letter = value.lower()[0]
            for option in self.options:
                if option.startswith(first_letter):
                    return option

            raise QuestionInputError(
                f"{value} is not one of the options: {self.options}"
            )

        if self.kind == "password":
            try:
                return validate_password(password=value)
            except Exception as e:
                raise QuestionInputError(f"Invalid password. {e}")
        return value


def ask(question: Question, kwargs: dict[str, str]) -> str:
    if question.var_name in kwargs and kwargs[question.var_name] is not None:
        value = kwargs[question.var_name]
    else:
        if question.default is not None:
            value = click.prompt(question.question, type=str, default=question.default)
        elif question.var_name == "password":
            value = click.prompt(
                question.question, type=str, hide_input=True, confirmation_prompt=True
            )
        else:
            value = click.prompt(question.question, type=str)

    try:
        value = question.validate(value=value)
    except QuestionInputError as e:
        print(e)
        return ask(question=question, kwargs=kwargs)
    if question.cache:
        arg_cache[question.var_name] = value

    return value


def fix_key_permission(private_key_path: str) -> None:
    key_permission = oct(stat.S_IMODE(os.stat(private_key_path).st_mode))
    chmod_permission = "400"
    octal_permission = f"0o{chmod_permission}"
    if key_permission != octal_permission:
        print(
            f"Fixing key permission: {private_key_path}, setting to {chmod_permission}"
        )
        try:
            os.chmod(private_key_path, int(octal_permission, 8))
        except Exception as e:
            print("Failed to fix key permission", e)
            raise e


def private_to_public_key(private_key_path: str, temp_path: str, username: str) -> str:
    # check key permission
    fix_key_permission(private_key_path=private_key_path)
    output_path = f"{temp_path}/hagrid_{username}_key.pub"
    cmd = f"ssh-keygen -f {private_key_path} -y > {output_path}"
    try:
        subprocess.check_call(cmd, shell=True)  # nosec
    except Exception as e:
        print("failed to make ssh key", e)
        raise e
    return output_path


def check_azure_authed() -> bool:
    cmd = "az account show"
    try:
        subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)  # nosec
        return True
    except Exception:  # nosec
        pass
    return False


def login_azure() -> bool:
    cmd = "az login"
    try:
        subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)  # nosec
        return True
    except Exception:  # nosec
        pass
    return False


def check_azure_cli_installed() -> bool:
    try:
        result = subprocess.run(  # nosec
            ["az", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        if result.returncode != 0:
            raise FileNotFoundError("az not installed")
    except Exception:  # nosec
        msg = "\nYou don't appear to have the Azure CLI installed!!! \n\n\
Please install it and then retry your command.\
\n\nInstallation Instructions: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli\n"
        raise FileNotFoundError(msg)

    return True


def check_gcloud_cli_installed() -> bool:
    try:
        subprocess.call(["gcloud", "version"])  # nosec
        print("Gcloud cli installed!")
    except FileNotFoundError:
        msg = "\nYou don't appear to have the gcloud CLI tool installed! \n\n\
Please install it and then retry again.\
\n\nInstallation Instructions: https://cloud.google.com/sdk/docs/install-sdk \n"
        raise FileNotFoundError(msg)

    return True


def check_aws_cli_installed() -> bool:
    try:
        result = subprocess.run(  # nosec
            ["aws", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        if result.returncode != 0:
            raise FileNotFoundError("AWS CLI not installed")
    except Exception:  # nosec
        msg = "\nYou don't appear to have the AWS CLI installed! \n\n\
Please install it and then retry your command.\
\n\nInstallation Instructions: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html\n"
        raise FileNotFoundError(msg)

    return True


def check_gcloud_authed() -> bool:
    try:
        result = subprocess.run(  # nosec
            ["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE
        )
        if result.returncode == 0:
            return True
    except Exception:  # nosec
        pass
    return False


def login_gcloud() -> bool:
    cmd = "gcloud auth login"
    try:
        subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)  # nosec
        return True
    except Exception:  # nosec
        pass
    return False


def str_to_bool(bool_str: str | None) -> bool:
    result = False
    bool_str = str(bool_str).lower()
    if bool_str == "true" or bool_str == "1":
        result = True
    return result


ART = str_to_bool(os.environ.get("HAGRID_ART", "True"))


def generate_gcloud_key_at_path(key_path: str) -> str:
    key_path = os.path.expanduser(key_path)
    if os.path.exists(key_path):
        raise Exception(f"Can't generate key since path already exists. {key_path}")
    else:
        # triggers a key check
        cmd = "gcloud compute ssh '' --dry-run"
        try:
            subprocess.check_call(cmd, shell=True)  # nosec
        except Exception:  # nosec
            pass
        if not os.path.exists(key_path):
            raise Exception(f"gcloud failed to generate ssh-key at: {key_path}")

    return key_path


def generate_aws_key_at_path(key_path: str, key_name: str) -> str:
    key_path = os.path.expanduser(key_path)
    if os.path.exists(key_path):
        raise Exception(f"Can't generate key since path already exists. {key_path}")
    else:
        # TODO we need to do differently for powershell.
        # Ex: aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial'
        # --output text | out-file -encoding ascii -filepath MyKeyPair.pem

        print(f"Creating AWS key pair with name {key_name} at path {key_path}..")
        cmd = f"aws ec2 create-key-pair --key-name {key_name} --query 'KeyMaterial' --output text > {key_path}"
        try:
            subprocess.check_call(cmd, shell=True)  # nosec
            subprocess.check_call(f"chmod 400 {key_path}", shell=True)  # nosec
        except Exception as e:  # nosec
            print(f"Failed to create key: {e}")
        if not os.path.exists(key_path):
            raise Exception(f"AWS failed to generate key pair at: {key_path}")

    return key_path


def generate_key_at_path(key_path: str) -> str:
    key_path = os.path.expanduser(key_path)
    if os.path.exists(key_path):
        raise Exception(f"Can't generate key since path already exists. {key_path}")
    else:
        cmd = f"ssh-keygen -N '' -f {key_path}"
        try:
            subprocess.check_call(cmd, shell=True)  # nosec
            if not os.path.exists(key_path):
                raise Exception(f"Failed to generate ssh-key at: {key_path}")
        except Exception as e:
            raise e

    return key_path


def validate_password(password: str) -> str:
    """Validate if the password entered by the user is valid.

    Password length should be between 12 - 123 characters
    Passwords must also meet 3 out of the following 4 complexity requirements:
    - Have lower characters
    - Have upper characters
    - Have a digit
    - Have a special character

    Args:
        password (str): password for the vm

    Returns:
        str: password if it is valid
    """
    # Validate password length
    if len(password) < 12 or len(password) > 123:
        raise ValueError("Password length should be between 12 - 123 characters")

    # Valid character types
    character_types = {
        "upper_case": False,
        "lower_case": False,
        "digit": False,
        "special": False,
    }

    for ch in password:
        if ch.islower():
            character_types["lower_case"] = True
        elif ch.isupper():
            character_types["upper_case"] = True
        elif ch.isdigit():
            character_types["digit"] = True
        elif ch.isascii():
            character_types["special"] = True
        else:
            raise ValueError(f"{ch} is not a valid character for password")

    # Validate characters in the password
    required_character_type_count = sum(
        [int(value) for value in character_types.values()]
    )

    if required_character_type_count >= 3:
        return password

    absent_character_types = ", ".join(
        char_type for char_type, value in character_types.items() if value is False
    ).strip(", ")

    raise ValueError(
        f"At least one {absent_character_types} character types must be present"
    )


def create_launch_cmd(
    verb: GrammarVerb,
    kwargs: dict[str, Any],
    ignore_docker_version_check: bool | None = False,
) -> str | list[str] | dict[str, list[str]]:
    parsed_kwargs: dict[str, Any] = {}
    host_term = verb.get_named_term_hostgrammar(name="host")

    host = host_term.host
    auth: AuthCredentials | None = None

    tail = bool(kwargs["tail"])

    parsed_kwargs = {}

    parsed_kwargs["build"] = bool(kwargs["build"])

    parsed_kwargs["use_blob_storage"] = not bool(kwargs["no_blob_storage"])

    parsed_kwargs["in_mem_workers"] = bool(kwargs["in_mem_workers"])

    if parsed_kwargs["use_blob_storage"]:
        parsed_kwargs["set_s3_username"] = kwargs["set_s3_username"]
        parsed_kwargs["set_s3_password"] = kwargs["set_s3_password"]
        parsed_kwargs["set_volume_size_limit_mb"] = kwargs["set_volume_size_limit_mb"]

    parsed_kwargs["node_count"] = (
        int(kwargs["node_count"]) if "node_count" in kwargs else 1
    )

    if parsed_kwargs["node_count"] > 1 and host not in ["azure"]:
        print("\nArgument `node_count` is only supported with `azure`.\n")
    else:
        # Default to detached mode if running more than one nodes
        tail = False if parsed_kwargs["node_count"] > 1 else tail

    headless = bool(kwargs["headless"])
    parsed_kwargs["headless"] = headless

    parsed_kwargs["oblv"] = bool(kwargs["oblv"])

    parsed_kwargs["tls"] = bool(kwargs["tls"])
    parsed_kwargs["test"] = bool(kwargs["test"])
    parsed_kwargs["dev"] = bool(kwargs["dev"])

    parsed_kwargs["silent"] = not bool(kwargs["verbose"])

    parsed_kwargs["trace"] = False
    if ("trace" not in kwargs or kwargs["trace"] is None) and parsed_kwargs["dev"]:
        # default to trace on in dev mode
        parsed_kwargs["trace"] = False
    elif "trace" in kwargs:
        parsed_kwargs["trace"] = str_to_bool(cast(str, kwargs["trace"]))

    parsed_kwargs["release"] = "production"
    if "release" in kwargs and kwargs["release"] != "production":
        parsed_kwargs["release"] = kwargs["release"]

    # if we use --dev override it
    if parsed_kwargs["dev"] is True:
        parsed_kwargs["release"] = "development"

    # derive node type
    if kwargs["low_side"]:
        parsed_kwargs["node_side_type"] = NodeSideType.LOW_SIDE.value
    else:
        parsed_kwargs["node_side_type"] = NodeSideType.HIGH_SIDE.value

    parsed_kwargs["smtp_username"] = kwargs["smtp_username"]
    parsed_kwargs["smtp_password"] = kwargs["smtp_password"]
    parsed_kwargs["smtp_port"] = kwargs["smtp_port"]
    parsed_kwargs["smtp_host"] = kwargs["smtp_host"]
    parsed_kwargs["smtp_sender"] = kwargs["smtp_sender"]

    parsed_kwargs["enable_warnings"] = not kwargs["no_warnings"]

    # choosing deployment type
    parsed_kwargs["deployment_type"] = "container_stack"
    if "deployment_type" in kwargs and kwargs["deployment_type"] is not None:
        parsed_kwargs["deployment_type"] = kwargs["deployment_type"]

    if "cert_store_path" in kwargs:
        parsed_kwargs["cert_store_path"] = kwargs["cert_store_path"]
    if "upload_tls_cert" in kwargs:
        parsed_kwargs["upload_tls_cert"] = kwargs["upload_tls_cert"]
    if "upload_tls_key" in kwargs:
        parsed_kwargs["upload_tls_key"] = kwargs["upload_tls_key"]

    parsed_kwargs["provision"] = not bool(kwargs["no_provision"])

    if "image_name" in kwargs and kwargs["image_name"] is not None:
        parsed_kwargs["image_name"] = kwargs["image_name"]
    else:
        parsed_kwargs["image_name"] = "default"

    if parsed_kwargs["dev"] is True:
        parsed_kwargs["tag"] = "local"
    else:
        if "tag" in kwargs and kwargs["tag"] is not None and kwargs["tag"] != "":
            parsed_kwargs["tag"] = kwargs["tag"]
        else:
            parsed_kwargs["tag"] = "latest"

    if "jupyter" in kwargs and kwargs["jupyter"] is not None:
        parsed_kwargs["jupyter"] = str_to_bool(cast(str, kwargs["jupyter"]))
    else:
        parsed_kwargs["jupyter"] = False

    # allows changing docker platform to other cpu architectures like arm64
    parsed_kwargs["platform"] = kwargs["platform"] if "platform" in kwargs else None

    parsed_kwargs["tail"] = tail

    parsed_kwargs["set_root_password"] = (
        kwargs["set_root_password"] if "set_root_password" in kwargs else None
    )

    parsed_kwargs["set_root_email"] = (
        kwargs["set_root_email"] if "set_root_email" in kwargs else None
    )

    parsed_kwargs["template"] = kwargs["template"] if "template" in kwargs else None
    parsed_kwargs["template_overwrite"] = bool(kwargs["template_overwrite"])

    parsed_kwargs["compose_src_path"] = kwargs["compose_src_path"]

    parsed_kwargs["enable_signup"] = str_to_bool(cast(str, kwargs["enable_signup"]))

    # Override template tag with user input tag
    if (
        parsed_kwargs["tag"] is not None
        and parsed_kwargs["template"] is None
        and parsed_kwargs["tag"] not in ["local"]
    ):
        # third party
        from packaging import version

        pattern = r"[0-9].[0-9].[0-9]"
        input_tag = parsed_kwargs["tag"]
        if (
            not re.match(pattern, input_tag)
            and input_tag != "latest"
            and input_tag != "beta"
            and "b" not in input_tag
        ):
            raise Exception(
                f"Not a valid tag: {parsed_kwargs['tag']}"
                + "\nValid tags: latest, beta, beta version(ex: 0.8.2b35),[0-9].[0-9].[0-9]"
            )

        # TODO: we need to redo this so that pypi and docker mappings are in a single
        # file inside dev
        if parsed_kwargs["tag"] == "latest":
            parsed_kwargs["template"] = LATEST_STABLE_SYFT
            parsed_kwargs["tag"] = LATEST_STABLE_SYFT
        elif parsed_kwargs["tag"] == "beta" or "b" in parsed_kwargs["tag"]:
            tag = (
                LATEST_BETA_SYFT
                if parsed_kwargs["tag"] == "beta"
                else parsed_kwargs["tag"]
            )

            # Currently, manifest_template.yml is only supported for beta versions >= 0.8.2b34
            beta_version = version.parse(tag)
            MINIMUM_BETA_VERSION = "0.8.2b34"
            if beta_version < version.parse(MINIMUM_BETA_VERSION):
                raise Exception(
                    f"Minimum beta version tag supported is {MINIMUM_BETA_VERSION}"
                )

            # Check if the beta version is available
            template_url = f"https://github.com/OpenMined/PySyft/releases/download/v{str(beta_version)}/manifest_template.yml"
            response = requests.get(template_url)  # nosec
            if response.status_code != 200:
                raise Exception(
                    f"Tag {parsed_kwargs['tag']} is not available"
                    + " \n for download. Please check the available tags at: "
                    + "\n https://github.com/OpenMined/PySyft/releases"
                )

            parsed_kwargs["template"] = template_url
            parsed_kwargs["tag"] = tag
        else:
            MINIMUM_TAG_VERSION = version.parse("0.8.0")
            tag = version.parse(parsed_kwargs["tag"])
            if tag < MINIMUM_TAG_VERSION:
                raise Exception(
                    f"Minimum supported stable tag version is {MINIMUM_TAG_VERSION}"
                )
            parsed_kwargs["template"] = parsed_kwargs["tag"]

    if host in ["docker"] and parsed_kwargs["template"] and host is not None:
        # Setup the files from the manifest_template.yml
        kwargs = setup_from_manifest_template(
            host_type=host,
            deployment_type=parsed_kwargs["deployment_type"],
            template_location=parsed_kwargs["template"],
            overwrite=parsed_kwargs["template_overwrite"],
            verbose=kwargs["verbose"],
        )

        parsed_kwargs.update(kwargs)

    if host in ["docker"]:
        # Check docker service status
        if not ignore_docker_version_check:
            check_docker_service_status()

        # Check grid docker versions
        if not ignore_docker_version_check:
            check_grid_docker(display=True, output_in_text=True)

        if not ignore_docker_version_check:
            version = check_docker_version()
        else:
            version = "n/a"

        if version:
            # If the user is using docker desktop (OSX/Windows), check to make sure there's enough RAM.
            # If the user is using Linux this isn't an issue because Docker scales to the avaialble RAM,
            # but on Docker Desktop it defaults to 2GB which isn't enough.
            dd_memory = docker_desktop_memory()
            if dd_memory < 8192 and dd_memory != -1:
                raise Exception(
                    "You appear to be using Docker Desktop but don't have "
                    "enough memory allocated. It appears you've configured "
                    f"Memory:{dd_memory} MB when 8192MB (8GB) is required. "
                    f"Please open Docker Desktop Preferences panel and set Memory"
                    f" to 8GB or higher. \n\n"
                    f"\tOSX Help: https://docs.docker.com/desktop/mac/\n"
                    f"\tWindows Help: https://docs.docker.com/desktop/windows/\n\n"
                    f"Then re-run your hagrid command.\n\n"
                    f"If you see this warning on Linux then something isn't right. "
                    f"Please file a Github Issue on PySyft's Github.\n\n"
                    f"Alternatively in case no more memory could be allocated, "
                    f"you can run hagrid on the cloud with GitPod by visiting "
                    f"https://gitpod.io/#https://github.com/OpenMined/PySyft."
                )

            if is_windows() and not DEPENDENCIES["wsl"]:
                raise Exception(
                    "You must install wsl2 for Windows to use HAGrid.\n"
                    "In PowerShell or Command Prompt type:\n> wsl --install\n\n"
                    "Read more here: https://docs.microsoft.com/en-us/windows/wsl/install"
                )

            return create_launch_docker_cmd(
                verb=verb,
                docker_version=version,
                tail=tail,
                kwargs=parsed_kwargs,
                silent=parsed_kwargs["silent"],
            )

    elif host in ["azure"]:
        check_azure_cli_installed()

        while not check_azure_authed():
            print("You need to log into Azure")
            login_azure()

        if DEPENDENCIES["ansible-playbook"]:
            resource_group = ask(
                question=Question(
                    var_name="azure_resource_group",
                    question="What resource group name do you want to use (or create)?",
                    default=arg_cache["azure_resource_group"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            location = ask(
                question=Question(
                    var_name="azure_location",
                    question="If this is a new resource group what location?",
                    default=arg_cache["azure_location"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            size = ask(
                question=Question(
                    var_name="azure_size",
                    question="What size machine?",
                    default=arg_cache["azure_size"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            username = ask(
                question=Question(
                    var_name="azure_username",
                    question="What do you want the username for the VM to be?",
                    default=arg_cache["azure_username"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            parsed_kwargs["auth_type"] = ask(
                question=Question(
                    var_name="auth_type",
                    question="Do you want to login with a key or password",
                    default=arg_cache["auth_type"],
                    kind="option",
                    options=["key", "password"],
                    cache=True,
                ),
                kwargs=kwargs,
            )

            key_path = None
            if parsed_kwargs["auth_type"] == "key":
                key_path_question = Question(
                    var_name="azure_key_path",
                    question=f"Absolute path of the private key to access {username}@{host}?",
                    default=arg_cache["azure_key_path"],
                    kind="path",
                    cache=True,
                )
                try:
                    key_path = ask(
                        key_path_question,
                        kwargs=kwargs,
                    )
                except QuestionInputPathError as e:
                    print(e)
                    key_path = str(e).split("is not a valid path")[0].strip()

                    create_key_question = Question(
                        var_name="azure_key_path",
                        question=f"Key {key_path} does not exist. Do you want to create it? (y/n)",
                        default="y",
                        kind="yesno",
                    )
                    create_key = ask(
                        create_key_question,
                        kwargs=kwargs,
                    )
                    if create_key == "y":
                        key_path = generate_key_at_path(key_path=key_path)
                    else:
                        raise QuestionInputError(
                            "Unable to create VM without a private key"
                        )
            elif parsed_kwargs["auth_type"] == "password":
                auto_generate_password = ask(
                    question=Question(
                        var_name="auto_generate_password",
                        question="Do you want to auto-generate the password? (y/n)",
                        kind="yesno",
                    ),
                    kwargs=kwargs,
                )
                if auto_generate_password == "y":  # nosec
                    parsed_kwargs["password"] = generate_sec_random_password(length=16)
                elif auto_generate_password == "n":  # nosec
                    parsed_kwargs["password"] = ask(
                        question=Question(
                            var_name="password",
                            question=f"Password for {username}@{host}?",
                            kind="password",
                        ),
                        kwargs=kwargs,
                    )

            repo = ask(
                Question(
                    var_name="azure_repo",
                    question="Repo to fetch source from?",
                    default=arg_cache["azure_repo"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )
            branch = ask(
                Question(
                    var_name="azure_branch",
                    question="Branch to monitor for updates?",
                    default=arg_cache["azure_branch"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            use_branch(branch=branch)

            password = parsed_kwargs.get("password")

            auth = AuthCredentials(
                username=username, key_path=key_path, password=password
            )

            if not auth.valid:
                raise Exception(f"Login Credentials are not valid. {auth}")

            return create_launch_azure_cmd(
                verb=verb,
                resource_group=resource_group,
                location=location,
                size=size,
                username=username,
                password=password,
                key_path=key_path,
                repo=repo,
                branch=branch,
                auth=auth,
                ansible_extras=kwargs["ansible_extras"],
                kwargs=parsed_kwargs,
            )
        else:
            errors = []
            if not DEPENDENCIES["ansible-playbook"]:
                errors.append("ansible-playbook")
            msg = "\nERROR!!! MISSING DEPENDENCY!!!"
            msg += f"\n\nLaunching a Cloud VM requires: {' '.join(errors)}"
            msg += "\n\nPlease follow installation instructions: "
            msg += "https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#"
            msg += "\n\nNote: we've found the 'conda' based installation instructions to work best"
            msg += " (e.g. something lke 'conda install -c conda-forge ansible'). "
            msg += "The pip based instructions seem to be a bit buggy if you're using a conda environment"
            msg += "\n"
            raise MissingDependency(msg)

    elif host in ["gcp"]:
        check_gcloud_cli_installed()

        while not check_gcloud_authed():
            print("You need to log into Google Cloud")
            login_gcloud()

        if DEPENDENCIES["ansible-playbook"]:
            project_id = ask(
                question=Question(
                    var_name="gcp_project_id",
                    question="What PROJECT ID do you want to use?",
                    default=arg_cache["gcp_project_id"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            zone = ask(
                question=Question(
                    var_name="gcp_zone",
                    question="What zone do you want your VM in?",
                    default=arg_cache["gcp_zone"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            machine_type = ask(
                question=Question(
                    var_name="gcp_machine_type",
                    question="What size machine?",
                    default=arg_cache["gcp_machine_type"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            username = ask(
                question=Question(
                    var_name="gcp_username",
                    question="What is your shell username?",
                    default=arg_cache["gcp_username"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            key_path_question = Question(
                var_name="gcp_key_path",
                question=f"Private key to access user@{host}?",
                default=arg_cache["gcp_key_path"],
                kind="path",
                cache=True,
            )
            try:
                key_path = ask(
                    key_path_question,
                    kwargs=kwargs,
                )
            except QuestionInputPathError as e:
                print(e)
                key_path = str(e).split("is not a valid path")[0].strip()

                create_key_question = Question(
                    var_name="gcp_key_path",
                    question=f"Key {key_path} does not exist. Do you want gcloud to make it? (y/n)",
                    default="y",
                    kind="yesno",
                )
                create_key = ask(
                    create_key_question,
                    kwargs=kwargs,
                )
                if create_key == "y":
                    key_path = generate_gcloud_key_at_path(key_path=key_path)
                else:
                    raise QuestionInputError(
                        "Unable to create VM without a private key"
                    )

            repo = ask(
                Question(
                    var_name="gcp_repo",
                    question="Repo to fetch source from?",
                    default=arg_cache["gcp_repo"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )
            branch = ask(
                Question(
                    var_name="gcp_branch",
                    question="Branch to monitor for updates?",
                    default=arg_cache["gcp_branch"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            use_branch(branch=branch)

            auth = AuthCredentials(username=username, key_path=key_path)

            return create_launch_gcp_cmd(
                verb=verb,
                project_id=project_id,
                zone=zone,
                machine_type=machine_type,
                repo=repo,
                auth=auth,
                branch=branch,
                ansible_extras=kwargs["ansible_extras"],
                kwargs=parsed_kwargs,
            )
        else:
            errors = []
            if not DEPENDENCIES["ansible-playbook"]:
                errors.append("ansible-playbook")
            msg = "\nERROR!!! MISSING DEPENDENCY!!!"
            msg += f"\n\nLaunching a Cloud VM requires: {' '.join(errors)}"
            msg += "\n\nPlease follow installation instructions: "
            msg += "https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#"
            msg += "\n\nNote: we've found the 'conda' based installation instructions to work best"
            msg += " (e.g. something lke 'conda install -c conda-forge ansible'). "
            msg += "The pip based instructions seem to be a bit buggy if you're using a conda environment"
            msg += "\n"
            raise MissingDependency(msg)

    elif host in ["aws"]:
        check_aws_cli_installed()

        if DEPENDENCIES["ansible-playbook"]:
            aws_region = ask(
                question=Question(
                    var_name="aws_region",
                    question="In what region do you want to deploy the EC2 instance?",
                    default=arg_cache["aws_region"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )
            aws_security_group_name = ask(
                question=Question(
                    var_name="aws_security_group_name",
                    question="Name of the security group to be created?",
                    default=arg_cache["aws_security_group_name"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )
            aws_security_group_cidr = ask(
                question=Question(
                    var_name="aws_security_group_cidr",
                    question="What IP addresses to allow for incoming network traffic? Please use CIDR notation",
                    default=arg_cache["aws_security_group_cidr"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )
            ec2_instance_type = ask(
                question=Question(
                    var_name="aws_ec2_instance_type",
                    question="What EC2 instance type do you want to deploy?",
                    default=arg_cache["aws_ec2_instance_type"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            aws_key_name = ask(
                question=Question(
                    var_name="aws_key_name",
                    question="Enter the name of the key pair to use to connect to the EC2 instance",
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            key_path_qn_str = (
                "Please provide the path of the private key to connect to the instance"
            )
            key_path_qn_str += " (if it does not exist, this path corresponds to "
            key_path_qn_str += "where you want to store the key upon creation)"
            key_path_question = Question(
                var_name="aws_key_path",
                question=key_path_qn_str,
                kind="path",
                cache=True,
            )
            try:
                key_path = ask(
                    key_path_question,
                    kwargs=kwargs,
                )
            except QuestionInputPathError as e:
                print(e)
                key_path = str(e).split("is not a valid path")[0].strip()

                create_key_question = Question(
                    var_name="aws_key_path",
                    question=f"Key {key_path} does not exist. Do you want AWS to make it? (y/n)",
                    default="y",
                    kind="yesno",
                )
                create_key = ask(
                    create_key_question,
                    kwargs=kwargs,
                )
                if create_key == "y":
                    key_path = generate_aws_key_at_path(
                        key_path=key_path, key_name=aws_key_name
                    )
                else:
                    raise QuestionInputError(
                        "Unable to create EC2 instance without key"
                    )

            repo = ask(
                Question(
                    var_name="aws_repo",
                    question="Repo to fetch source from?",
                    default=arg_cache["aws_repo"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )
            branch = ask(
                Question(
                    var_name="aws_branch",
                    question="Branch to monitor for updates?",
                    default=arg_cache["aws_branch"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            use_branch(branch=branch)

            username = arg_cache["aws_ec2_instance_username"]
            auth = AuthCredentials(username=username, key_path=key_path)

            return create_launch_aws_cmd(
                verb=verb,
                region=aws_region,
                ec2_instance_type=ec2_instance_type,
                security_group_name=aws_security_group_name,
                aws_security_group_cidr=aws_security_group_cidr,
                key_path=key_path,
                key_name=aws_key_name,
                repo=repo,
                branch=branch,
                ansible_extras=kwargs["ansible_extras"],
                kwargs=parsed_kwargs,
                ami_id=arg_cache["aws_image_id"],
                username=username,
                auth=auth,
            )

        else:
            errors = []
            if not DEPENDENCIES["ansible-playbook"]:
                errors.append("ansible-playbook")
            msg = "\nERROR!!! MISSING DEPENDENCY!!!"
            msg += f"\n\nLaunching a Cloud VM requires: {' '.join(errors)}"
            msg += "\n\nPlease follow installation instructions: "
            msg += "https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#"
            msg += "\n\nNote: we've found the 'conda' based installation instructions to work best"
            msg += " (e.g. something lke 'conda install -c conda-forge ansible'). "
            msg += "The pip based instructions seem to be a bit buggy if you're using a conda environment"
            msg += "\n"
            raise MissingDependency(msg)
    else:
        if DEPENDENCIES["ansible-playbook"]:
            if host != "localhost":
                parsed_kwargs["username"] = ask(
                    question=Question(
                        var_name="username",
                        question=f"Username for {host} with sudo privledges?",
                        default=arg_cache["username"],
                        kind="string",
                        cache=True,
                    ),
                    kwargs=kwargs,
                )
                parsed_kwargs["auth_type"] = ask(
                    question=Question(
                        var_name="auth_type",
                        question="Do you want to login with a key or password",
                        default=arg_cache["auth_type"],
                        kind="option",
                        options=["key", "password"],
                        cache=True,
                    ),
                    kwargs=kwargs,
                )
                if parsed_kwargs["auth_type"] == "key":
                    parsed_kwargs["key_path"] = ask(
                        question=Question(
                            var_name="key_path",
                            question=f"Private key to access {parsed_kwargs['username']}@{host}?",
                            default=arg_cache["key_path"],
                            kind="path",
                            cache=True,
                        ),
                        kwargs=kwargs,
                    )
                elif parsed_kwargs["auth_type"] == "password":
                    parsed_kwargs["password"] = ask(
                        question=Question(
                            var_name="password",
                            question=f"Password for {parsed_kwargs['username']}@{host}?",
                            kind="password",
                        ),
                        kwargs=kwargs,
                    )

            parsed_kwargs["repo"] = ask(
                question=Question(
                    var_name="repo",
                    question="Repo to fetch source from?",
                    default=arg_cache["repo"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            parsed_kwargs["branch"] = ask(
                Question(
                    var_name="branch",
                    question="Branch to monitor for updates?",
                    default=arg_cache["branch"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

            auth = None
            if host != "localhost":
                if parsed_kwargs["auth_type"] == "key":
                    auth = AuthCredentials(
                        username=parsed_kwargs["username"],
                        key_path=parsed_kwargs["key_path"],
                    )
                else:
                    auth = AuthCredentials(
                        username=parsed_kwargs["username"],
                        key_path=parsed_kwargs["password"],
                    )
                if not auth.valid:
                    raise Exception(f"Login Credentials are not valid. {auth}")
            parsed_kwargs["ansible_extras"] = kwargs["ansible_extras"]
            return create_launch_custom_cmd(verb=verb, auth=auth, kwargs=parsed_kwargs)
        else:
            errors = []
            if not DEPENDENCIES["ansible-playbook"]:
                errors.append("ansible-playbook")
            raise MissingDependency(
                f"Launching a Custom VM requires: {' '.join(errors)}"
            )

    host_options = ", ".join(allowed_hosts)
    raise MissingDependency(
        f"Launch requires a correct host option, try: {host_options}"
    )


def pull_command(cmd: str, kwargs: dict[str, Any]) -> list[str]:
    pull_cmd = str(cmd)
    if kwargs["release"] == "production":
        pull_cmd += " --file docker-compose.yml"
    else:
        pull_cmd += " --file docker-compose.pull.yml"
    pull_cmd += " pull --ignore-pull-failures"  # ignore missing version from Dockerhub
    return [pull_cmd]


def build_command(cmd: str) -> list[str]:
    build_cmd = str(cmd)
    build_cmd += " --file docker-compose.build.yml"
    build_cmd += " build"
    return [build_cmd]


def deploy_command(cmd: str, tail: bool, dev_mode: bool) -> list[str]:
    up_cmd = str(cmd)
    up_cmd += " --file docker-compose.dev.yml" if dev_mode else ""
    up_cmd += " up"
    if not tail:
        up_cmd += " -d"
    return [up_cmd]


def create_launch_docker_cmd(
    verb: GrammarVerb,
    docker_version: str,
    kwargs: dict[str, Any],
    tail: bool = True,
    silent: bool = False,
) -> dict[str, list[str]]:
    host_term = verb.get_named_term_hostgrammar(name="host")
    node_name = verb.get_named_term_type(name="node_name")
    node_type = verb.get_named_term_type(name="node_type")

    snake_name = str(node_name.snake_input)
    tag = name_tag(name=str(node_name.input))

    if ART and not silent:
        hagrid()

    print(
        "Launching a PyGrid "
        + str(node_type.input).capitalize()
        + " node on port "
        + str(host_term.free_port)
        + "!\n"
    )

    version_string = kwargs["tag"]
    version_hash = "dockerhub"
    build = kwargs["build"]

    # if in development mode, generate a version_string which is either
    # the one you inputed concatenated with -dev or the contents of the VERSION file
    version = GRID_SRC_VERSION()
    if "release" in kwargs and kwargs["release"] == "development":
        # force version to have -dev at the end in dev mode
        # during development we can use the latest beta version
        if version_string is None:
            version_string = version[0]
        version_string += "-dev"
        version_hash = version[1]
        build = True
    else:
        # whereas if in production mode and tag == "local" use the local VERSION file
        # or if its not set somehow, which should never happen, use stable
        # otherwise use the kwargs["tag"] from above

        # during production the default would be stable
        if version_string == "local":
            # this can be used in VMs in production to auto update from src
            version_string = version[0]
            version_hash = version[1]
            build = True
        elif version_string is None:
            version_string = "latest"

    if platform.uname().machine.lower() in ["x86_64", "amd64"]:
        docker_platform = "linux/amd64"
    else:
        docker_platform = "linux/arm64"

    if "platform" in kwargs and kwargs["platform"] is not None:
        docker_platform = kwargs["platform"]

    if kwargs["template"]:
        _, template_hash = get_template_yml(kwargs["template"])
        template_dir = manifest_cache_path(template_hash)
        template_grid_dir = f"{template_dir}/packages/grid"
    else:
        template_grid_dir = GRID_SRC_PATH()

    compose_src_path = kwargs["compose_src_path"]
    if not compose_src_path:
        compose_src_path = get_compose_src_path(
            node_type=node_type,
            node_name=snake_name,
            template_location=kwargs["template"],
            **kwargs,
        )

    single_container_mode = kwargs["deployment_type"] == "single_container"
    in_mem_workers = kwargs.get("in_mem_workers")
    smtp_username = kwargs.get("smtp_username")
    smtp_sender = kwargs.get("smtp_sender")
    smtp_password = kwargs.get("smtp_password")
    smtp_port = kwargs.get("smtp_port")
    smtp_host = kwargs.get("smtp_host")

    enable_oblv = bool(kwargs["oblv"])
    print("  - NAME: " + str(snake_name))
    print("  - TEMPLATE DIR: " + template_grid_dir)
    if compose_src_path:
        print("  - COMPOSE SOURCE: " + compose_src_path)
    print("  - RELEASE: " + f'{kwargs["node_side_type"]}-{kwargs["release"]}')
    print("  - DEPLOYMENT:", kwargs["deployment_type"])
    print("  - ARCH: " + docker_platform)
    print("  - TYPE: " + str(node_type.input))
    print("  - DOCKER_TAG: " + version_string)
    if version_hash != "dockerhub":
        print("  - GIT_HASH: " + version_hash)
    print("  - HAGRID_VERSION: " + get_version_string())
    if EDITABLE_MODE:
        print("  - HAGRID_REPO_SHA: " + commit_hash())
    print("  - PORT: " + str(host_term.free_port))
    print("  - DOCKER COMPOSE: " + docker_version)
    print("  - IN-MEMORY WORKERS: " + str(in_mem_workers))
    if enable_oblv:
        print("  - OBLV: ", enable_oblv)

    print("\n")

    use_blob_storage = (
        False
        if str(node_type.input) in ["network", "gateway"]
        else bool(kwargs["use_blob_storage"])
    )

    # use a docker volume
    host_path = "credentials-data"

    # in development use a folder mount
    if kwargs.get("release", "") == "development":
        RELATIVE_PATH = ""
        # if EDITABLE_MODE:
        #     RELATIVE_PATH = "../"
        # we might need to change this for the hagrid template mode
        host_path = f"{RELATIVE_PATH}./backend/grid/storage/{snake_name}"

    envs = {
        "RELEASE": "production",
        "COMPOSE_DOCKER_CLI_BUILD": 1,
        "DOCKER_BUILDKIT": 1,
        "HTTP_PORT": int(host_term.free_port),
        "HTTPS_PORT": int(host_term.free_port_tls),
        "BACKEND_STORAGE_PATH": "credentials-data",
        "TRAEFIK_TAG": str(tag),
        "NODE_NAME": str(snake_name),
        "NODE_TYPE": str(node_type.input),
        "TRAEFIK_PUBLIC_NETWORK_IS_EXTERNAL": "False",
        "VERSION": version_string,
        "VERSION_HASH": version_hash,
        "USE_BLOB_STORAGE": str(use_blob_storage),
        "FRONTEND_TARGET": "grid-ui-production",
        "STACK_API_KEY": str(
            generate_sec_random_password(length=48, special_chars=False)
        ),
        "OBLV_ENABLED": str(enable_oblv).lower(),
        "CREDENTIALS_VOLUME": host_path,
        "NODE_SIDE_TYPE": kwargs["node_side_type"],
        "SINGLE_CONTAINER_MODE": single_container_mode,
        "INMEMORY_WORKERS": in_mem_workers,
    }

    if smtp_host and smtp_port and smtp_username and smtp_password:
        envs["SMTP_HOST"] = smtp_host
        envs["SMTP_PORT"] = smtp_port
        envs["SMTP_USERNAME"] = smtp_username
        envs["SMTP_PASSWORD"] = smtp_password
        envs["EMAIL_SENDER"] = smtp_sender

    if "trace" in kwargs and kwargs["trace"] is True:
        envs["TRACE"] = "True"
        envs["JAEGER_HOST"] = "host.docker.internal"
        envs["JAEGER_PORT"] = int(
            find_available_port(host="localhost", port=14268, search=True)
        )

    if "enable_warnings" in kwargs:
        envs["ENABLE_WARNINGS"] = kwargs["enable_warnings"]

    if "platform" in kwargs and kwargs["platform"] is not None:
        envs["DOCKER_DEFAULT_PLATFORM"] = docker_platform

    if "tls" in kwargs and kwargs["tls"] is True and len(kwargs["cert_store_path"]) > 0:
        envs["TRAEFIK_TLS_CERTS"] = kwargs["cert_store_path"]

    if (
        "tls" in kwargs
        and kwargs["tls"] is True
        and "test" in kwargs
        and kwargs["test"] is True
    ):
        envs["IGNORE_TLS_ERRORS"] = "True"

    if "test" in kwargs and kwargs["test"] is True:
        envs["S3_VOLUME_SIZE_MB"] = "100"  # GitHub CI is small

    if kwargs.get("release", "") == "development":
        envs["RABBITMQ_MANAGEMENT"] = "-management"

    # currently we only have a domain frontend for dev mode
    if kwargs.get("release", "") == "development" and (
        str(node_type.input) not in ["network", "gateway"]
    ):
        envs["FRONTEND_TARGET"] = "grid-ui-development"

    if "set_root_password" in kwargs and kwargs["set_root_password"] is not None:
        envs["DEFAULT_ROOT_PASSWORD"] = kwargs["set_root_password"]

    if "set_root_email" in kwargs and kwargs["set_root_email"] is not None:
        envs["DEFAULT_ROOT_EMAIL"] = kwargs["set_root_email"]

    if "set_s3_username" in kwargs and kwargs["set_s3_username"] is not None:
        envs["S3_ROOT_USER"] = kwargs["set_s3_username"]

    if "set_s3_password" in kwargs and kwargs["set_s3_password"] is not None:
        envs["S3_ROOT_PWD"] = kwargs["set_s3_password"]

    if (
        "set_volume_size_limit_mb" in kwargs
        and kwargs["set_volume_size_limit_mb"] is not None
    ):
        envs["S3_VOLUME_SIZE_MB"] = kwargs["set_volume_size_limit_mb"]

    if "release" in kwargs:
        envs["RELEASE"] = kwargs["release"]

    if "enable_signup" in kwargs:
        envs["ENABLE_SIGNUP"] = kwargs["enable_signup"]

    cmd = ""
    args = []
    for k, v in envs.items():
        if is_windows():
            # powershell envs
            quoted = f"'{v}'" if not isinstance(v, int) else v
            args.append(f"$env:{k}={quoted}")
        else:
            args.append(f"{k}={v}")
    if is_windows():
        cmd += "; ".join(args)
        cmd += "; "
    else:
        cmd += " ".join(args)

    cmd += " docker compose -p " + snake_name

    # new docker compose regression work around
    # default_env = os.path.expanduser("~/.hagrid/app/.env")

    default_env = f"{template_grid_dir}/default.env"
    if not os.path.exists(default_env):
        # old path
        default_env = f"{template_grid_dir}/.env"
    default_envs = {}
    with open(default_env) as f:
        for line in f.readlines():
            if "=" in line:
                parts = line.strip().split("=")
                key = parts[0]
                value = ""
                if len(parts) > 1:
                    value = parts[1]
                default_envs[key] = value
    default_envs.update(envs)

    # env file path
    env_file_path = compose_src_path + "/.env"

    # Render templates if creating stack from the manifest_template.yml
    if kwargs["template"] and host_term.host is not None:
        # If release is development, update relative path
        # if EDITABLE_MODE:
        #     default_envs["RELATIVE_PATH"] = "../"

        render_templates(
            node_name=snake_name,
            deployment_type=kwargs["deployment_type"],
            template_location=kwargs["template"],
            env_vars=default_envs,
            host_type=host_term.host,
        )

    try:
        env_file = ""
        for k, v in default_envs.items():
            env_file += f"{k}={v}\n"

        with open(env_file_path, "w") as f:
            f.write(env_file)

        # cmd += f" --env-file {env_file_path}"
    except Exception:  # nosec
        pass

    if single_container_mode:
        cmd += " --profile worker"
    else:
        cmd += " --profile backend"
        cmd += " --profile proxy"
        cmd += " --profile mongo"

        if str(node_type.input) in ["network", "gateway"]:
            cmd += " --profile network"

        if use_blob_storage:
            cmd += " --profile blob-storage"

        # no frontend container so expect bad gateway on the / route
        if not bool(kwargs["headless"]):
            cmd += " --profile frontend"

        if "trace" in kwargs and kwargs["trace"]:
            cmd += " --profile telemetry"

    final_commands = {}
    final_commands["Pulling"] = pull_command(cmd, kwargs)

    cmd += " --file docker-compose.yml"
    if "tls" in kwargs and kwargs["tls"] is True:
        cmd += " --file docker-compose.tls.yml"
    if "test" in kwargs and kwargs["test"] is True:
        cmd += " --file docker-compose.test.yml"

    if build:
        my_build_command = build_command(cmd)
        final_commands["Building"] = my_build_command

    dev_mode = kwargs.get("dev", False)
    final_commands["Launching"] = deploy_command(cmd, tail, dev_mode)
    return final_commands


def create_launch_vagrant_cmd(verb: GrammarVerb) -> str:
    host_term = verb.get_named_term_hostgrammar(name="host")
    node_name = verb.get_named_term_type(name="node_name")
    node_type = verb.get_named_term_type(name="node_type")

    snake_name = str(node_name.snake_input)

    if ART:
        hagrid()

    print(
        "Launching a "
        + str(node_type.input)
        + " PyGrid node on port "
        + str(host_term.port)
        + "!\n"
    )

    print("  - TYPE: " + str(node_type.input))
    print("  - NAME: " + str(snake_name))
    print("  - PORT: " + str(host_term.port))
    # print("  - VAGRANT: " + "1")
    # print("  - VIRTUALBOX: " + "1")
    print("\n")

    cmd = ""
    cmd += 'ANSIBLE_ARGS="'
    cmd += f"-e 'node_name={snake_name}'"
    cmd += f"-e 'node_type={node_type.input}'"
    cmd += '" '
    cmd += "vagrant up --provision"
    cmd = "cd " + GRID_SRC_PATH() + ";" + cmd
    return cmd


def get_or_make_resource_group(resource_group: str, location: str = "westus") -> None:
    cmd = f"az group show --resource-group {resource_group}"
    exists = True
    try:
        subprocess.check_call(cmd, shell=True)  # nosec
    except Exception:  # nosec
        # group doesn't exist so lets create it
        exists = False

    if not exists:
        cmd = f"az group create -l {location} -n {resource_group}"
        try:
            print(f"Creating resource group.\nRunning: {cmd}")
            subprocess.check_call(cmd, shell=True)  # nosec
        except Exception as e:
            raise Exception(
                f"Unable to create resource group {resource_group} @ {location}. {e}"
            )


def extract_host_ip(stdout: bytes) -> str | None:
    output = stdout.decode("utf-8")

    try:
        j = json.loads(output)
        if "publicIpAddress" in j:
            return str(j["publicIpAddress"])
    except Exception:  # nosec
        matcher = r'publicIpAddress":\s+"(.+)"'
        ips = re.findall(matcher, output)
        if len(ips) > 0:
            return ips[0]

    return None


def get_vm_host_ips(node_name: str, resource_group: str) -> list | None:
    cmd = f"az vm list-ip-addresses -g {resource_group} --query "
    cmd += f""""[?starts_with(virtualMachine.name, '{node_name}')]"""
    cmd += '''.virtualMachine.network.publicIpAddresses[0].ipAddress"'''
    output = subprocess.check_output(cmd, shell=True)  # nosec
    try:
        host_ips = json.loads(output)
        return host_ips
    except Exception as e:
        print(f"Failed to extract ips: {e}")

    return None


def is_valid_ip(host_or_ip: str) -> bool:
    matcher = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
    ips = re.findall(matcher, host_or_ip.strip())
    if len(ips) == 1:
        return True
    return False


def extract_host_ip_gcp(stdout: bytes) -> str | None:
    output = stdout.decode("utf-8")

    try:
        matcher = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        ips = re.findall(matcher, output)
        if len(ips) == 2:
            return ips[1]
    except Exception:  # nosec
        pass

    return None


def extract_host_ip_from_cmd(cmd: str) -> str | None:
    try:
        matcher = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        ips = re.findall(matcher, cmd)
        if ips:
            return ips[0]
    except Exception:  # nosec
        pass

    return None


def check_ip_for_ssh(
    host_ip: str, timeout: int = 600, wait_time: int = 5, silent: bool = False
) -> bool:
    if not silent:
        print(f"Checking VM at {host_ip} is up")
    checks = int(timeout / wait_time)  # 10 minutes in 5 second chunks
    first_run = True
    while checks > 0:
        checks -= 1
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(wait_time)
            result = sock.connect_ex((host_ip, 22))
            sock.close()
            if result == 0:
                if not silent:
                    print(f"VM at {host_ip} is up!")
                return True
            else:
                if first_run:
                    if not silent:
                        print("Waiting for VM to start", end="", flush=True)
                    first_run = False
                else:
                    if not silent:
                        print(".", end="", flush=True)
        except Exception:  # nosec
            pass
    return False


def create_aws_security_group(
    security_group_name: str, region: str, snake_name: str
) -> str:
    sg_description = f"{snake_name} security group"
    create_cmd = f"aws ec2 create-security-group --group-name {security_group_name} "
    create_cmd += f'--region {region} --description "{sg_description}" '
    sg_output = subprocess.check_output(  # nosec
        create_cmd,
        shell=True,
    )
    sg_output_dict = json.loads(sg_output)
    if "GroupId" in sg_output_dict:
        return sg_output_dict["GroupId"]

    return ""


def open_port_aws(
    security_group_name: str, port_no: int, cidr: str, region: str
) -> None:
    cmd = f"aws ec2 authorize-security-group-ingress --group-name {security_group_name} --protocol tcp "
    cmd += f"--port {port_no} --cidr {cidr} --region {region}"
    subprocess.check_call(  # nosec
        cmd,
        shell=True,
    )


def extract_instance_ids_aws(stdout: bytes) -> list:
    output = stdout.decode("utf-8")
    output_dict = json.loads(output)
    instance_ids: list = []
    if "Instances" in output_dict:
        for ec2_instance_metadata in output_dict["Instances"]:
            if "InstanceId" in ec2_instance_metadata:
                instance_ids.append(ec2_instance_metadata["InstanceId"])

    return instance_ids


def get_host_ips_given_instance_ids(
    instance_ids: list, timeout: int = 600, wait_time: int = 10
) -> list:
    checks = int(timeout / wait_time)  # 10 minutes in 10 second chunks
    instance_ids_str = " ".join(instance_ids)
    cmd = f"aws ec2 describe-instances --instance-ids {instance_ids_str}"
    cmd += " --query 'Reservations[*].Instances[*].{StateName:State.Name,PublicIpAddress:PublicIpAddress}'"
    cmd += " --output json"
    while checks > 0:
        checks -= 1
        time.sleep(wait_time)
        desc_ec2_output = subprocess.check_output(cmd, shell=True)  # nosec
        instances_output_json = json.loads(desc_ec2_output.decode("utf-8"))
        host_ips: list = []
        all_instances_running = True
        for reservation in instances_output_json:
            for instance_metadata in reservation:
                if instance_metadata["StateName"] != "running":
                    all_instances_running = False
                    break
                else:
                    host_ips.append(instance_metadata["PublicIpAddress"])
        if all_instances_running:
            return host_ips
        # else, wait another wait_time seconds and try again

    return []


def make_aws_ec2_instance(
    ami_id: str, ec2_instance_type: str, key_name: str, security_group_name: str
) -> list:
    # From the docs: "For security groups in a nondefault VPC, you must specify the security group ID".
    # Right now, since we're using default VPC, we can use security group name instead of ID.

    ebs_size = 200  # gb
    cmd = f"aws ec2 run-instances --image-id {ami_id} --count 1 --instance-type {ec2_instance_type} "
    cmd += f"--key-name {key_name} --security-groups {security_group_name} "
    tmp_cmd = rf"[{{\"DeviceName\":\"/dev/sdf\",\"Ebs\":{{\"VolumeSize\":{ebs_size},\"DeleteOnTermination\":false}}}}]"
    cmd += f'--block-device-mappings "{tmp_cmd}"'

    host_ips: list = []
    try:
        print(f"Creating EC2 instance.\nRunning: {cmd}")
        create_ec2_output = subprocess.check_output(cmd, shell=True)  # nosec
        instance_ids = extract_instance_ids_aws(create_ec2_output)
        host_ips = get_host_ips_given_instance_ids(instance_ids=instance_ids)
    except Exception as e:
        print("failed", e)

    if not (host_ips):
        raise Exception("Failed to create EC2 instance(s) or get public ip(s)")

    return host_ips


def create_launch_aws_cmd(
    verb: GrammarVerb,
    region: str,
    ec2_instance_type: str,
    security_group_name: str,
    aws_security_group_cidr: str,
    key_name: str,
    key_path: str,
    ansible_extras: str,
    kwargs: dict[str, Any],
    repo: str,
    branch: str,
    ami_id: str,
    username: str,
    auth: AuthCredentials,
) -> list[str]:
    node_name = verb.get_named_term_type(name="node_name")
    snake_name = str(node_name.snake_input)
    create_aws_security_group(security_group_name, region, snake_name)
    open_port_aws(
        security_group_name=security_group_name,
        port_no=80,
        cidr=aws_security_group_cidr,
        region=region,
    )  # HTTP
    open_port_aws(
        security_group_name=security_group_name,
        port_no=443,
        cidr=aws_security_group_cidr,
        region=region,
    )  # HTTPS
    open_port_aws(
        security_group_name=security_group_name,
        port_no=22,
        cidr=aws_security_group_cidr,
        region=region,
    )  # SSH
    if kwargs["jupyter"]:
        open_port_aws(
            security_group_name=security_group_name,
            port_no=8888,
            cidr=aws_security_group_cidr,
            region=region,
        )  # Jupyter

    host_ips = make_aws_ec2_instance(
        ami_id=ami_id,
        ec2_instance_type=ec2_instance_type,
        key_name=key_name,
        security_group_name=security_group_name,
    )

    launch_cmds: list[str] = []

    for host_ip in host_ips:
        # get old host
        host_term = verb.get_named_term_hostgrammar(name="host")

        # replace
        host_term.parse_input(host_ip)
        verb.set_named_term_type(name="host", new_term=host_term)

        if not bool(kwargs["provision"]):
            print("Skipping automatic provisioning.")
            print("VM created with:")
            print(f"IP: {host_ip}")
            print(f"Key: {key_path}")
            print("\nConnect with:")
            print(f"ssh -i {key_path} {username}@{host_ip}")

        else:
            extra_kwargs = {
                "repo": repo,
                "branch": branch,
                "ansible_extras": ansible_extras,
            }
            kwargs.update(extra_kwargs)

            # provision
            host_up = check_ip_for_ssh(host_ip=host_ip)
            if not host_up:
                print(f"Warning: {host_ip} ssh not available yet")
            launch_cmd = create_launch_custom_cmd(verb=verb, auth=auth, kwargs=kwargs)
            launch_cmds.append(launch_cmd)

    return launch_cmds


def make_vm_azure(
    node_name: str,
    resource_group: str,
    username: str,
    password: str | None,
    key_path: str | None,
    size: str,
    image_name: str,
    node_count: int,
) -> list:
    disk_size_gb = "200"
    try:
        temp_dir = tempfile.TemporaryDirectory()
        public_key_path = (
            private_to_public_key(
                private_key_path=key_path, temp_path=temp_dir.name, username=username
            )
            if key_path
            else None
        )
    except Exception:  # nosec
        temp_dir.cleanup()

    authentication_type = "ssh" if key_path else "password"
    cmd = f"az vm create -n {node_name} -g {resource_group} --size {size} "
    cmd += f"--image {image_name} --os-disk-size-gb {disk_size_gb} "
    cmd += f"--public-ip-sku Standard --authentication-type {authentication_type} --admin-username {username} "
    cmd += f"--ssh-key-values {public_key_path} " if public_key_path else ""
    cmd += f"--admin-password '{password}' " if password else ""
    cmd += f"--count {node_count} " if node_count > 1 else ""

    host_ips: list | None = []
    try:
        print(f"Creating vm.\nRunning: {hide_azure_vm_password(cmd)}")
        subprocess.check_output(cmd, shell=True)  # nosec
        host_ips = get_vm_host_ips(node_name=node_name, resource_group=resource_group)
    except Exception as e:
        print("failed", e)
    finally:
        temp_dir.cleanup()

    if not host_ips:
        raise Exception("Failed to create vm or get VM public ip")

    try:
        # clean up temp public key
        if public_key_path:
            os.unlink(public_key_path)
    except Exception:  # nosec
        pass

    return host_ips


def open_port_vm_azure(
    resource_group: str, node_name: str, port_name: str, port: int, priority: int
) -> None:
    cmd = f"az network nsg rule create --resource-group {resource_group} "
    cmd += f"--nsg-name {node_name}NSG --name {port_name} --destination-port-ranges {port} --priority {priority}"
    try:
        print(f"Creating {port_name} {port} ngs rule.\nRunning: {cmd}")
        output = subprocess.check_call(cmd, shell=True)  # nosec
        print("output", output)
        pass
    except Exception as e:
        print("failed", e)


def create_project(project_id: str) -> None:
    cmd = f"gcloud projects create {project_id} --set-as-default"
    try:
        print(f"Creating project.\nRunning: {cmd}")
        subprocess.check_call(cmd, shell=True)  # nosec
    except Exception as e:
        print("failed", e)

    print("create project complete")


def create_launch_gcp_cmd(
    verb: GrammarVerb,
    project_id: str,
    zone: str,
    machine_type: str,
    ansible_extras: str,
    kwargs: dict[str, Any],
    repo: str,
    branch: str,
    auth: AuthCredentials,
) -> str:
    # create project if it doesn't exist
    create_project(project_id)
    # vm
    node_name = verb.get_named_term_type(name="node_name")
    kebab_name = str(node_name.kebab_input)
    disk_size_gb = "200"
    host_ip = make_gcp_vm(
        vm_name=kebab_name,
        project_id=project_id,
        zone=zone,
        machine_type=machine_type,
        disk_size_gb=disk_size_gb,
    )

    # get old host
    host_term = verb.get_named_term_hostgrammar(name="host")

    host_up = check_ip_for_ssh(host_ip=host_ip)
    if not host_up:
        raise Exception(f"Something went wrong launching the VM at IP: {host_ip}.")

    if not bool(kwargs["provision"]):
        print("Skipping automatic provisioning.")
        print("VM created with:")
        print(f"IP: {host_ip}")
        print(f"User: {auth.username}")
        print(f"Key: {auth.key_path}")
        print("\nConnect with:")
        print(f"ssh -i {auth.key_path} {auth.username}@{host_ip}")
        sys.exit(0)

    # replace
    host_term.parse_input(host_ip)
    verb.set_named_term_type(name="host", new_term=host_term)

    extra_kwargs = {
        "repo": repo,
        "branch": branch,
        "auth_type": "key",
        "ansible_extras": ansible_extras,
    }
    kwargs.update(extra_kwargs)

    # provision
    return create_launch_custom_cmd(verb=verb, auth=auth, kwargs=kwargs)


def make_gcp_vm(
    vm_name: str, project_id: str, zone: str, machine_type: str, disk_size_gb: str
) -> str:
    create_cmd = "gcloud compute instances create"
    network_settings = "network=default,network-tier=PREMIUM"
    maintenance_policy = "MIGRATE"
    scopes = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring.write",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/trace.append",
    ]
    tags = "http-server,https-server"
    disk_image = "projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20230429"
    disk = (
        f"auto-delete=yes,boot=yes,device-name={vm_name},image={disk_image},"
        + f"mode=rw,size={disk_size_gb},type=pd-ssd"
    )
    security_flags = (
        "--no-shielded-secure-boot --shielded-vtpm "
        + "--shielded-integrity-monitoring --reservation-affinity=any"
    )

    cmd = (
        f"{create_cmd} {vm_name} "
        + f"--project={project_id} "
        + f"--zone={zone} "
        + f"--machine-type={machine_type} "
        + f"--create-disk={disk} "
        + f"--network-interface={network_settings} "
        + f"--maintenance-policy={maintenance_policy} "
        + f"--scopes={','.join(scopes)} --tags={tags} "
        + f"{security_flags}"
    )

    host_ip = None
    try:
        print(f"Creating vm.\nRunning: {cmd}")
        output = subprocess.check_output(cmd, shell=True)  # nosec
        host_ip = extract_host_ip_gcp(stdout=output)
    except Exception as e:
        print("failed", e)

    if host_ip is None:
        raise Exception("Failed to create vm or get VM public ip")

    return host_ip


def create_launch_azure_cmd(
    verb: GrammarVerb,
    resource_group: str,
    location: str,
    size: str,
    username: str,
    password: str | None,
    key_path: str | None,
    repo: str,
    branch: str,
    auth: AuthCredentials,
    ansible_extras: str,
    kwargs: dict[str, Any],
) -> list[str]:
    get_or_make_resource_group(resource_group=resource_group, location=location)

    node_count = kwargs.get("node_count", 1)
    print("Total VMs to create: ", node_count)

    # vm
    node_name = verb.get_named_term_type(name="node_name")
    snake_name = str(node_name.snake_input)
    image_name = get_azure_image(kwargs["image_name"])
    host_ips = make_vm_azure(
        snake_name,
        resource_group,
        username,
        password,
        key_path,
        size,
        image_name,
        node_count,
    )

    # open port 80
    open_port_vm_azure(
        resource_group=resource_group,
        node_name=snake_name,
        port_name="HTTP",
        port=80,
        priority=500,
    )

    # open port 443
    open_port_vm_azure(
        resource_group=resource_group,
        node_name=snake_name,
        port_name="HTTPS",
        port=443,
        priority=501,
    )

    if kwargs["jupyter"]:
        # open port 8888
        open_port_vm_azure(
            resource_group=resource_group,
            node_name=snake_name,
            port_name="Jupyter",
            port=8888,
            priority=502,
        )

    launch_cmds: list[str] = []

    for host_ip in host_ips:
        # get old host
        host_term = verb.get_named_term_hostgrammar(name="host")

        # replace
        host_term.parse_input(host_ip)
        verb.set_named_term_type(name="host", new_term=host_term)

        if not bool(kwargs["provision"]):
            print("Skipping automatic provisioning.")
            print("VM created with:")
            print(f"Name: {snake_name}")
            print(f"IP: {host_ip}")
            print(f"User: {username}")
            print(f"Password: {password}")
            print(f"Key: {key_path}")
            print("\nConnect with:")
            if kwargs["auth_type"] == "key":
                print(f"ssh -i {key_path} {username}@{host_ip}")
            else:
                print(f"ssh {username}@{host_ip}")
        else:
            extra_kwargs = {
                "repo": repo,
                "branch": branch,
                "ansible_extras": ansible_extras,
            }
            kwargs.update(extra_kwargs)

            # provision
            host_up = check_ip_for_ssh(host_ip=host_ip)
            if not host_up:
                print(f"Warning: {host_ip} ssh not available yet")
            launch_cmd = create_launch_custom_cmd(verb=verb, auth=auth, kwargs=kwargs)
            launch_cmds.append(launch_cmd)

    return launch_cmds


def create_ansible_land_cmd(
    verb: GrammarVerb, auth: AuthCredentials | None, kwargs: dict[str, Any]
) -> str:
    try:
        host_term = verb.get_named_term_hostgrammar(name="host")
        print("Landing PyGrid node on port " + str(host_term.port) + "!\n")

        print("  - PORT: " + str(host_term.port))
        print("\n")

        grid_path = GRID_SRC_PATH()
        playbook_path = grid_path + "/ansible/site.yml"
        ansible_cfg_path = grid_path + "/ansible.cfg"
        auth = cast(AuthCredentials, auth)

        if not os.path.exists(playbook_path):
            print(f"Can't find playbook site.yml at: {playbook_path}")
        cmd = f"ANSIBLE_CONFIG={ansible_cfg_path} ansible-playbook "
        if host_term.host == "localhost":
            cmd += "--connection=local "
        cmd += f"-i {host_term.host}, {playbook_path}"
        if host_term.host != "localhost" and kwargs["auth_type"] == "key":
            cmd += f" --private-key {auth.key_path} --user {auth.username}"
        elif host_term.host != "localhost" and kwargs["auth_type"] == "password":
            cmd += f" -c paramiko --user {auth.username}"

        ANSIBLE_ARGS = {"install": "false"}

        if host_term.host != "localhost" and kwargs["auth_type"] == "password":
            ANSIBLE_ARGS["ansible_ssh_pass"] = kwargs["password"]

        if host_term.host == "localhost":
            ANSIBLE_ARGS["local"] = "true"

        if "ansible_extras" in kwargs and kwargs["ansible_extras"] != "":
            options = kwargs["ansible_extras"].split(",")
            for option in options:
                parts = option.strip().split("=")
                if len(parts) == 2:
                    ANSIBLE_ARGS[parts[0]] = parts[1]

        for k, v in ANSIBLE_ARGS.items():
            cmd += f" -e \"{k}='{v}'\""

        cmd = "cd " + grid_path + ";" + cmd
        return cmd
    except Exception as e:
        print(f"Failed to construct custom deployment cmd: {cmd}. {e}")
        raise e


def create_launch_custom_cmd(
    verb: GrammarVerb, auth: AuthCredentials | None, kwargs: dict[str, Any]
) -> str:
    try:
        host_term = verb.get_named_term_hostgrammar(name="host")
        node_name = verb.get_named_term_type(name="node_name")
        node_type = verb.get_named_term_type(name="node_type")
        # source_term = verb.get_named_term_type(name="source")

        snake_name = str(node_name.snake_input)

        if ART:
            hagrid()

        print(
            "Launching a "
            + str(node_type.input)
            + " PyGrid node on port "
            + str(host_term.port)
            + "!\n"
        )

        print("  - TYPE: " + str(node_type.input))
        print("  - NAME: " + str(snake_name))
        print("  - PORT: " + str(host_term.port))
        print("\n")

        grid_path = GRID_SRC_PATH()
        playbook_path = grid_path + "/ansible/site.yml"
        ansible_cfg_path = grid_path + "/ansible.cfg"
        auth = cast(AuthCredentials, auth)

        if not os.path.exists(playbook_path):
            print(f"Can't find playbook site.yml at: {playbook_path}")
        cmd = f"ANSIBLE_CONFIG={ansible_cfg_path} ansible-playbook "
        if host_term.host == "localhost":
            cmd += "--connection=local "
        cmd += f"-i {host_term.host}, {playbook_path}"
        if host_term.host != "localhost" and kwargs["auth_type"] == "key":
            cmd += f" --private-key {auth.key_path} --user {auth.username}"
        elif host_term.host != "localhost" and kwargs["auth_type"] == "password":
            cmd += f" -c paramiko --user {auth.username}"

        version_string = kwargs["tag"]
        if version_string is None:
            version_string = "local"

        ANSIBLE_ARGS = {
            "node_type": node_type.input,
            "node_name": snake_name,
            "github_repo": kwargs["repo"],
            "repo_branch": kwargs["branch"],
            "docker_tag": version_string,
        }

        if host_term.host != "localhost" and kwargs["auth_type"] == "password":
            ANSIBLE_ARGS["ansible_ssh_pass"] = kwargs["password"]

        if host_term.host == "localhost":
            ANSIBLE_ARGS["local"] = "true"

        if "node_side_type" in kwargs:
            ANSIBLE_ARGS["node_side_type"] = kwargs["node_side_type"]

        if kwargs["tls"] is True:
            ANSIBLE_ARGS["tls"] = "true"

        if "release" in kwargs:
            ANSIBLE_ARGS["release"] = kwargs["release"]

        if "set_root_email" in kwargs and kwargs["set_root_email"] is not None:
            ANSIBLE_ARGS["root_user_email"] = kwargs["set_root_email"]

        if "set_root_password" in kwargs and kwargs["set_root_password"] is not None:
            ANSIBLE_ARGS["root_user_password"] = kwargs["set_root_password"]

        if (
            kwargs["tls"] is True
            and "cert_store_path" in kwargs
            and len(kwargs["cert_store_path"]) > 0
        ):
            ANSIBLE_ARGS["cert_store_path"] = kwargs["cert_store_path"]

        if (
            kwargs["tls"] is True
            and "upload_tls_key" in kwargs
            and len(kwargs["upload_tls_key"]) > 0
        ):
            ANSIBLE_ARGS["upload_tls_key"] = kwargs["upload_tls_key"]

        if (
            kwargs["tls"] is True
            and "upload_tls_cert" in kwargs
            and len(kwargs["upload_tls_cert"]) > 0
        ):
            ANSIBLE_ARGS["upload_tls_cert"] = kwargs["upload_tls_cert"]

        if kwargs["jupyter"] is True:
            ANSIBLE_ARGS["jupyter"] = "true"
            ANSIBLE_ARGS["jupyter_token"] = generate_sec_random_password(
                length=48, upper_case=False, special_chars=False
            )

        if "ansible_extras" in kwargs and kwargs["ansible_extras"] != "":
            options = kwargs["ansible_extras"].split(",")
            for option in options:
                parts = option.strip().split("=")
                if len(parts) == 2:
                    ANSIBLE_ARGS[parts[0]] = parts[1]

        # if mode == "deploy":
        #     ANSIBLE_ARGS["deploy"] = "true"

        for k, v in ANSIBLE_ARGS.items():
            cmd += f" -e \"{k}='{v}'\""

        cmd = "cd " + grid_path + ";" + cmd
        return cmd
    except Exception as e:
        print(f"Failed to construct custom deployment cmd: {cmd}. {e}")
        raise e


def create_land_cmd(verb: GrammarVerb, kwargs: dict[str, Any]) -> str:
    host_term = verb.get_named_term_hostgrammar(name="host")
    host = host_term.host if host_term.host is not None else ""

    if host in ["docker"]:
        target = verb.get_named_term_grammar("node_name").input
        prune_volumes: bool = kwargs.get("prune_vol", False)

        if target == "all":
            # land all syft nodes
            if prune_volumes:
                land_cmd = "docker rm `docker ps --filter label=orgs.openmined.syft -q` --force "
                land_cmd += "&& docker volume rm "
                land_cmd += "$(docker volume ls --filter label=orgs.openmined.syft -q)"
                return land_cmd
            else:
                return "docker rm `docker ps --filter label=orgs.openmined.syft -q` --force"

        version = check_docker_version()
        if version:
            return create_land_docker_cmd(verb=verb, prune_volumes=prune_volumes)

    elif host == "localhost" or is_valid_ip(host):
        parsed_kwargs = {}
        if DEPENDENCIES["ansible-playbook"]:
            if host != "localhost":
                parsed_kwargs["username"] = ask(
                    question=Question(
                        var_name="username",
                        question=f"Username for {host} with sudo privledges?",
                        default=arg_cache["username"],
                        kind="string",
                        cache=True,
                    ),
                    kwargs=kwargs,
                )
                parsed_kwargs["auth_type"] = ask(
                    question=Question(
                        var_name="auth_type",
                        question="Do you want to login with a key or password",
                        default=arg_cache["auth_type"],
                        kind="option",
                        options=["key", "password"],
                        cache=True,
                    ),
                    kwargs=kwargs,
                )
                if parsed_kwargs["auth_type"] == "key":
                    parsed_kwargs["key_path"] = ask(
                        question=Question(
                            var_name="key_path",
                            question=f"Private key to access {parsed_kwargs['username']}@{host}?",
                            default=arg_cache["key_path"],
                            kind="path",
                            cache=True,
                        ),
                        kwargs=kwargs,
                    )
                elif parsed_kwargs["auth_type"] == "password":
                    parsed_kwargs["password"] = ask(
                        question=Question(
                            var_name="password",
                            question=f"Password for {parsed_kwargs['username']}@{host}?",
                            kind="password",
                        ),
                        kwargs=kwargs,
                    )

            auth = None
            if host != "localhost":
                if parsed_kwargs["auth_type"] == "key":
                    auth = AuthCredentials(
                        username=parsed_kwargs["username"],
                        key_path=parsed_kwargs["key_path"],
                    )
                else:
                    auth = AuthCredentials(
                        username=parsed_kwargs["username"],
                        key_path=parsed_kwargs["password"],
                    )
                if not auth.valid:
                    raise Exception(f"Login Credentials are not valid. {auth}")
            parsed_kwargs["ansible_extras"] = kwargs["ansible_extras"]
            return create_ansible_land_cmd(verb=verb, auth=auth, kwargs=parsed_kwargs)
        else:
            errors = []
            if not DEPENDENCIES["ansible-playbook"]:
                errors.append("ansible-playbook")
            raise MissingDependency(
                f"Launching a Custom VM requires: {' '.join(errors)}"
            )

    host_options = ", ".join(allowed_hosts)
    raise MissingDependency(
        f"Launch requires a correct host option, try: {host_options}"
    )


def create_land_docker_cmd(verb: GrammarVerb, prune_volumes: bool = False) -> str:
    """
    Create docker `land` command to remove containers when a node's name is specified
    """
    node_name = verb.get_named_term_type(name="node_name")
    snake_name = str(node_name.snake_input)

    path = GRID_SRC_PATH()
    env_var = ";export $(cat .env | sed 's/#.*//g' | xargs);"

    cmd = ""
    cmd += "docker compose"
    cmd += ' --file "docker-compose.yml"'
    cmd += ' --project-name "' + snake_name + '"'
    cmd += " down --remove-orphans"

    if prune_volumes:
        cmd += (
            f' && docker volume rm $(docker volume ls --filter name="{snake_name}" -q)'
        )

    cmd += f" && docker rm $(docker ps --filter name={snake_name} -q) --force"

    cmd = "cd " + path + env_var + cmd
    return cmd


@click.command(
    help="Stop a running PyGrid domain/network node.",
    context_settings={"show_default": True},
)
@click.argument("args", type=str, nargs=-1)
@click.option(
    "--cmd",
    is_flag=True,
    help="Print the cmd without running it",
)
@click.option(
    "--ansible-extras",
    default="",
    type=str,
)
@click.option(
    "--build-src",
    default=DEFAULT_BRANCH,
    required=False,
    type=str,
    help="Git branch to use for launch / build operations",
)
@click.option(
    "--silent",
    is_flag=True,
    help="Suppress extra outputs",
)
@click.option(
    "--force",
    is_flag=True,
    help="Bypass the prompt during hagrid land",
)
@click.option(
    "--prune-vol",
    is_flag=True,
    help="Prune docker volumes after land.",
)
def land(args: tuple[str], **kwargs: Any) -> None:
    verb = get_land_verb()
    silent = bool(kwargs["silent"])
    force = bool(kwargs["force"])
    try:
        grammar = parse_grammar(args=args, verb=verb)
        verb.load_grammar(grammar=grammar)
    except BadGrammar as e:
        print(e)
        return

    try:
        update_repo(repo=GIT_REPO(), branch=str(kwargs["build_src"]))
    except Exception as e:
        print(f"Failed to update repo. {e}")

    try:
        cmd = create_land_cmd(verb=verb, kwargs=kwargs)
    except Exception as e:
        print(f"{e}")
        return

    target = verb.get_named_term_grammar("node_name").input

    if not force:
        _land_domain = ask(
            Question(
                var_name="_land_domain",
                question=f"Are you sure you want to land {target} (y/n)",
                kind="yesno",
            ),
            kwargs={},
        )

    grid_path = GRID_SRC_PATH()

    if force or _land_domain == "y":
        if not bool(kwargs["cmd"]):
            if not silent:
                print("Running: \n", cmd)
            try:
                if silent:
                    process = subprocess.Popen(  # nosec
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=grid_path,
                        shell=True,
                    )
                    process.communicate()

                    print(f"HAGrid land {target} complete!")
                else:
                    subprocess.call(cmd, shell=True, cwd=grid_path)  # nosec
            except Exception as e:
                print(f"Failed to run cmd: {cmd}. {e}")
    else:
        print("Hagrid land aborted.")


cli.add_command(launch)
cli.add_command(land)
cli.add_command(clean)


@click.command(
    help="Show HAGrid debug information", context_settings={"show_default": True}
)
@click.argument("args", type=str, nargs=-1)
def debug(args: tuple[str], **kwargs: Any) -> None:
    debug_info = gather_debug()
    print("\n\nWhen reporting bugs, please copy everything between the lines.")
    print("==================================================================\n")
    print(json.dumps(debug_info))
    print("\n=================================================================\n\n")


cli.add_command(debug)


DEFAULT_HEALTH_CHECKS = ["host", "UI (βeta)", "api", "ssh", "jupyter"]
HEALTH_CHECK_FUNCTIONS = {
    "host": check_host,
    "UI (βeta)": check_login_page,
    "api": check_api_metadata,
    "ssh": check_ip_for_ssh,
    "jupyter": check_jupyter_server,
}

HEALTH_CHECK_ICONS = {
    "host": "🔌",
    "UI (βeta)": "🖱",
    "api": "⚙️",
    "ssh": "🔐",
    "jupyter": "📗",
}

HEALTH_CHECK_URLS = {
    "host": "{ip_address}",
    "UI (βeta)": "http://{ip_address}/login",
    "api": "http://{ip_address}/api/v2/openapi.json",
    "ssh": "hagrid ssh {ip_address}",
    "jupyter": "http://{ip_address}:8888",
}


def check_host_health(ip_address: str, keys: list[str]) -> dict[str, bool]:
    status = {}
    for key in keys:
        func: Callable = HEALTH_CHECK_FUNCTIONS[key]  # type: ignore
        status[key] = func(ip_address, silent=True)
    return status


def icon_status(status: bool) -> str:
    return "✅" if status else "❌"


def get_health_checks(ip_address: str) -> tuple[bool, list[list[str]]]:
    keys = list(DEFAULT_HEALTH_CHECKS)
    if "localhost" in ip_address:
        new_keys = []
        for key in keys:
            if key not in ["host", "jupyter", "ssh"]:
                new_keys.append(key)
        keys = new_keys

    health_status = check_host_health(ip_address=ip_address, keys=keys)
    complete_status = all(health_status.values())

    # find port from ip_address
    try:
        port = int(ip_address.split(":")[1])
    except Exception:
        # default to 80
        port = 80

    # url to display based on running environment
    display_url = gitpod_url(port).split("//")[1] if is_gitpod() else ip_address

    # figure out how to add this back?
    # console.print("[bold magenta]Checking host:[/bold magenta]", ip_address, ":mage:")
    table_contents = []
    for key, value in health_status.items():
        table_contents.append(
            [
                HEALTH_CHECK_ICONS[key],
                key,
                HEALTH_CHECK_URLS[key].replace("{ip_address}", display_url),
                icon_status(value),
            ]
        )

    return complete_status, table_contents


def create_check_table(
    table_contents: list[list[str]], time_left: int = 0
) -> rich.table.Table:
    table = rich.table.Table()
    table.add_column("PyGrid", style="magenta")
    table.add_column("Info", justify="left", overflow="fold")
    time_left_str = "" if time_left == 0 else str(time_left)
    table.add_column(time_left_str, justify="left")
    for row in table_contents:
        table.add_row(row[1], row[2], row[3])
    return table


def get_host_name(container_name: str, by_suffix: str) -> str:
    # Assumption we always get proxy containers first.
    # if users have old docker compose versios.
    # the container names are _ instead of -
    # canada_proxy_1 instead of canada-proxy-1
    try:
        host_name = container_name[0 : container_name.find(by_suffix) - 1]  # noqa: E203
    except Exception:
        host_name = ""
    return host_name


def get_docker_status(
    ip_address: str, node_name: str | None
) -> tuple[bool, tuple[str, str]]:
    url = from_url(ip_address)
    port = url[2]
    network_container = (
        shell(
            "docker ps --format '{{.Names}} {{.Ports}}' | " + f"grep '0.0.0.0:{port}'"
        )
        .strip()
        .split(" ")[0]
    )

    # Second conditional handle the case when internal port of worker container
    # matches with host port of launched Domain/Network Container
    if not network_container or (node_name and node_name not in network_container):
        # check if it is a worker container and an internal port was passed
        worker_containers_output: str = shell(
            "docker ps --format '{{.Names}} {{.Ports}}' | " + f"grep '{port}/tcp'"
        ).strip()
        if not worker_containers_output or not node_name:
            return False, ("", "")

        # If there are worker containers with an internal port
        # fetch the worker container with the launched worker name
        worker_containers = worker_containers_output.split("\n")
        for worker_container in worker_containers:
            container_name = worker_container.split(" ")[0]
            if node_name in container_name:
                network_container = container_name
                break
        else:
            # If the worker container is not created yet
            return False, ("", "")

    if "proxy" in network_container:
        host_name = get_host_name(network_container, by_suffix="proxy")

        backend_containers = shell(
            "docker ps --format '{{.Names}}' | grep 'backend' "
        ).split()

        _backend_exists = False
        for container in backend_containers:
            if host_name in container and "stream" not in container:
                _backend_exists = True
                break
        if not _backend_exists:
            return False, ("", "")

        node_type = "Domain"

        # TODO: Identify if node_type is Gateway
        # for container in headscale_containers:
        #     if host_name in container:
        #         node_type = "Gateway"
        #         break

        return True, (host_name, node_type)
    else:
        # health check for worker node
        host_name = get_host_name(network_container, by_suffix="worker")
        return True, (host_name, "Worker")


def get_syft_install_status(host_name: str, node_type: str) -> bool:
    container_search = "backend" if node_type != "Worker" else "worker"
    search_containers = shell(
        "docker ps --format '{{.Names}}' | " + f"grep '{container_search}' "
    ).split()

    context_container = None
    for container in search_containers:
        # stream keyword is for our old container stack
        if host_name in container and "stream" not in container:
            context_container = container
            break

    if not context_container:
        print(f"❌ {container_search} Docker Stack for: {host_name} not found")
        exit(0)
    else:
        container_log = shell(f"docker logs {context_container}")
        if "Application startup complete" not in container_log:
            return False
        return True


@click.command(
    help="Check health of an IP address/addresses or a resource group",
    context_settings={"show_default": True},
)
@click.argument("ip_addresses", type=str, nargs=-1)
@click.option(
    "--timeout",
    default=300,
    help="Timeout for hagrid check command",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Refresh output",
)
def check(
    ip_addresses: list[str], verbose: bool = False, timeout: int | str = 300
) -> None:
    check_status(ip_addresses=ip_addresses, silent=not verbose, timeout=timeout)


def _check_status(
    ip_addresses: str | list[str],
    silent: bool = True,
    signal: Event | None = None,
    node_name: str | None = None,
) -> None:
    OK_EMOJI = RichEmoji("white_heavy_check_mark").to_str()
    # Check if ip_addresses is str, then convert to list
    if ip_addresses and isinstance(ip_addresses, str):
        ip_addresses = [ip_addresses]
    console = Console()
    node_info = None
    if len(ip_addresses) == 0:
        headers = {"User-Agent": "curl/7.79.1"}
        print("Detecting External IP...")
        ip_res = requests.get("https://ifconfig.co", headers=headers)  # nosec
        ip_address = ip_res.text.strip()
        ip_addresses = [ip_address]

    if len(ip_addresses) == 1:
        ip_address = ip_addresses[0]
        status, table_contents = get_health_checks(ip_address=ip_address)
        table = create_check_table(table_contents=table_contents)
        max_timeout = 600
        if not status:
            table = create_check_table(
                table_contents=table_contents, time_left=max_timeout
            )
            if silent:
                with console.status("Gathering Node information") as console_status:
                    console_status.update(
                        "[bold orange_red1]Waiting for Container Creation"
                    )
                    docker_status, node_info = get_docker_status(ip_address, node_name)
                    while not docker_status:
                        docker_status, node_info = get_docker_status(
                            ip_address, node_name
                        )
                        time.sleep(1)
                        if (
                            signal and signal.is_set()
                        ):  # Stop execution if timeout is triggered
                            return
                    console.print(
                        f"{OK_EMOJI} {node_info[0]} {node_info[1]} Containers Created"
                    )

                    console_status.update("[bold orange_red1]Starting Backend")
                    syft_install_status = get_syft_install_status(
                        node_info[0], node_info[1]
                    )
                    while not syft_install_status:
                        syft_install_status = get_syft_install_status(
                            node_info[0], node_info[1]
                        )
                        time.sleep(1)
                        # Stop execution if timeout is triggered
                        if signal and signal.is_set():
                            return
                    console.print(f"{OK_EMOJI} Backend")
                    console.print(f"{OK_EMOJI} Startup Complete")

                status, table_contents = get_health_checks(ip_address)
                table = create_check_table(
                    table_contents=table_contents, time_left=max_timeout
                )
            else:
                while not status:
                    # Stop execution if timeout is triggered
                    if signal is not None and signal.is_set():
                        return
                    with Live(
                        table, refresh_per_second=2, screen=True, auto_refresh=False
                    ) as live:
                        max_timeout -= 1
                        if max_timeout % 5 == 0:
                            status, table_contents = get_health_checks(ip_address)
                        table = create_check_table(
                            table_contents=table_contents, time_left=max_timeout
                        )
                        live.update(table)
                        if status:
                            break
                        time.sleep(1)

        # TODO: Create new health checks table for Worker Container
        if (node_info and node_info[1] != "Worker") or not node_info:
            console.print(table)
    else:
        for ip_address in ip_addresses:
            _, table_contents = get_health_checks(ip_address)
            table = create_check_table(table_contents=table_contents)
            console.print(table)


def check_status(
    ip_addresses: str | list[str],
    silent: bool = True,
    timeout: int | str = 300,
    node_name: str | None = None,
) -> None:
    timeout = int(timeout)
    # third party
    from rich import print

    signal = Event()

    t = Thread(
        target=_check_status,
        kwargs={
            "ip_addresses": ip_addresses,
            "silent": silent,
            "signal": signal,
            "node_name": node_name,
        },
    )
    t.start()
    t.join(timeout=timeout)

    if t.is_alive():
        signal.set()
        t.join()

        print(f"Hagrid check command timed out after: {timeout} seconds 🕛")
        print(
            "Please try increasing the timeout or kindly check the docker containers for error logs."
        )
        print("You can view your container logs using the following tool:")
        print("Tool: [link=https://ctop.sh]Ctop[/link]")
        print("Video Explanation: https://youtu.be/BJhlCxerQP4 \n")


cli.add_command(check)


# add Hagrid info to the cli
@click.command(help="Show HAGrid info", context_settings={"show_default": True})
def version() -> None:
    print(f"HAGRID_VERSION: {get_version_string()}")
    if EDITABLE_MODE:
        print(f"HAGRID_REPO_SHA: {commit_hash()}")


cli.add_command(version)


def run_quickstart(
    url: str | None = None,
    syft: str = "latest",
    reset: bool = False,
    quiet: bool = False,
    pre: bool = False,
    test: bool = False,
    repo: str = DEFAULT_REPO,
    branch: str = DEFAULT_BRANCH,
    commit: str | None = None,
    python: str | None = None,
    zip_file: str | None = None,
) -> None:
    try:
        quickstart_art()
        directory = os.path.expanduser("~/.hagrid/quickstart/")
        confirm_reset = None
        if reset:
            if not quiet:
                confirm_reset = click.confirm(
                    "This will create a new quickstart virtualenv and reinstall Syft and "
                    "Jupyter. Are you sure you want to continue?"
                )
            else:
                confirm_reset = True
        if confirm_reset is False:
            return

        if reset and confirm_reset or not os.path.isdir(directory):
            quickstart_setup(
                directory=directory,
                syft_version=syft,
                reset=reset,
                pre=pre,
                python=python,
            )
        downloaded_files = []
        if zip_file:
            downloaded_files = fetch_notebooks_from_zipfile(
                zip_file,
                directory=directory,
                reset=reset,
            )
        elif url:
            downloaded_files = fetch_notebooks_for_url(
                url=url,
                directory=directory,
                reset=reset,
                repo=repo,
                branch=branch,
                commit=commit,
            )
        else:
            file_path = add_intro_notebook(directory=directory, reset=reset)
            downloaded_files.append(file_path)

        if len(downloaded_files) == 0:
            raise Exception(f"Unable to find files at: {url}")
        file_path = sorted(downloaded_files)[0]

        # add virtualenv path
        environ = os.environ.copy()
        os_bin_path = "Scripts" if is_windows() else "bin"
        venv_dir = directory + ".venv"
        environ["PATH"] = venv_dir + os.sep + os_bin_path + os.pathsep + environ["PATH"]
        jupyter_binary = "jupyter.exe" if is_windows() else "jupyter"

        if is_windows():
            env_activate_cmd = (
                "(Powershell): "
                + "cd "
                + venv_dir
                + "; "
                + os_bin_path
                + os.sep
                + "activate"
            )
        else:
            env_activate_cmd = (
                "(Linux): source " + venv_dir + os.sep + os_bin_path + "/activate"
            )

        print(f"To activate your virtualenv {env_activate_cmd}")

        try:
            allow_browser = " --no-browser" if is_gitpod() else ""
            cmd = (
                venv_dir
                + os.sep
                + os_bin_path
                + os.sep
                + f"{jupyter_binary} lab{allow_browser} --ip 0.0.0.0 --notebook-dir={directory} {file_path}"
            )
            if test:
                jupyter_path = venv_dir + os.sep + os_bin_path + os.sep + jupyter_binary
                if not os.path.exists(jupyter_path):
                    print(f"Failed to install Jupyter in path: {jupyter_path}")
                    sys.exit(1)
                print(f"Jupyter exists at: {jupyter_path}. CI Test mode exiting.")
                sys.exit(0)

            disable_toolbar_extension = (
                venv_dir
                + os.sep
                + os_bin_path
                + os.sep
                + f"{jupyter_binary} labextension disable @jupyterlab/cell-toolbar-extension"
            )

            subprocess.run(  # nosec
                disable_toolbar_extension.split(" "), cwd=directory, env=environ
            )

            ON_POSIX = "posix" in sys.builtin_module_names

            def enqueue_output(out: Any, queue: Queue) -> None:
                for line in iter(out.readline, b""):
                    queue.put(line)
                out.close()

            proc = subprocess.Popen(  # nosec
                cmd.split(" "),
                cwd=directory,
                env=environ,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=ON_POSIX,
            )
            queue: Queue = Queue()
            thread_1 = Thread(target=enqueue_output, args=(proc.stdout, queue))
            thread_2 = Thread(target=enqueue_output, args=(proc.stderr, queue))
            thread_1.daemon = True  # thread dies with the program
            thread_1.start()
            thread_2.daemon = True  # thread dies with the program
            thread_2.start()

            display_url = None
            console = rich.get_console()

            # keepn reading the queue of stdout + stderr
            while True:
                try:
                    if not display_url:
                        # try to read the line and extract a jupyter url:
                        with console.status(
                            "Starting Jupyter service"
                        ) as console_status:
                            line = queue.get()
                            display_url = extract_jupyter_url(line.decode("utf-8"))
                            if display_url:
                                display_jupyter_url(url_parts=display_url)
                                console_status.stop()
                except KeyboardInterrupt:
                    proc.kill()  # make sure jupyter gets killed
                    sys.exit(1)
                except Exception:  # nosec
                    pass  # nosec
        except KeyboardInterrupt:
            proc.kill()  # make sure jupyter gets killed
            sys.exit(1)
    except Exception as e:
        print(f"Error running quickstart: {e}")
        raise e


@click.command(
    help="Launch a Syft + Jupyter Session with a Notebook URL / Path",
    context_settings={"show_default": True},
)
@click.argument("url", type=str, required=False)
@click.option(
    "--reset",
    is_flag=True,
    default=False,
    help="Force hagrid quickstart to setup a fresh virtualenv",
)
@click.option(
    "--syft",
    default="latest",
    help="Choose a syft version or just use latest",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Silence confirmation prompts",
)
@click.option(
    "--pre",
    is_flag=True,
    help="Install pre-release versions of syft",
)
@click.option(
    "--python",
    default=None,
    help="Specify the path to which python to use",
)
@click.option(
    "--test",
    is_flag=True,
    help="CI Test Mode, don't hang on Jupyter",
)
@click.option(
    "--repo",
    default=DEFAULT_REPO,
    help="Choose a repo to fetch the notebook from or just use OpenMined/PySyft",
)
@click.option(
    "--branch",
    default=DEFAULT_BRANCH,
    help="Choose a branch to fetch from or just use dev",
)
@click.option(
    "--commit",
    help="Choose a specific commit to fetch the notebook from",
)
def quickstart_cli(
    url: str | None = None,
    syft: str = "latest",
    reset: bool = False,
    quiet: bool = False,
    pre: bool = False,
    test: bool = False,
    repo: str = DEFAULT_REPO,
    branch: str = DEFAULT_BRANCH,
    commit: str | None = None,
    python: str | None = None,
) -> None:
    return run_quickstart(
        url=url,
        syft=syft,
        reset=reset,
        quiet=quiet,
        pre=pre,
        test=test,
        repo=repo,
        branch=branch,
        commit=commit,
        python=python,
    )


cli.add_command(quickstart_cli, "quickstart")


def display_jupyter_url(url_parts: tuple[str, str, int]) -> None:
    url = url_parts[0]
    if is_gitpod():
        parts = urlparse(url)
        query = getattr(parts, "query", "")
        url = gitpod_url(port=url_parts[2]) + "?" + query

    console = rich.get_console()

    tick_emoji = RichEmoji("white_heavy_check_mark").to_str()
    link_emoji = RichEmoji("link").to_str()

    console.print(
        f"[bold white]{tick_emoji} Jupyter Server is running at:\n{link_emoji} [bold blue]{url}\n"
        + "[bold white]Use Control-C to stop this server and shut down all kernels.",
        new_line_start=True,
    )

    # if is_gitpod():
    #     open_browser_with_url(url=url)


def open_browser_with_url(url: str) -> None:
    webbrowser.open(url)


def extract_jupyter_url(line: str) -> tuple[str, str, int] | None:
    jupyter_regex = r"^.*(http.*127.*)"
    try:
        matches = re.match(jupyter_regex, line)
        if matches is not None:
            url = matches.group(1).strip()
            parts = urlparse(url)
            host_or_ip_parts = parts.netloc.split(":")
            # netloc is host:port
            port = 8888
            if len(host_or_ip_parts) > 1:
                port = int(host_or_ip_parts[1])
            host_or_ip = host_or_ip_parts[0]
            return (url, host_or_ip, port)
    except Exception as e:
        print("failed to parse jupyter url", e)
    return None


def quickstart_setup(
    directory: str,
    syft_version: str,
    reset: bool = False,
    pre: bool = False,
    python: str | None = None,
) -> None:
    console = rich.get_console()
    OK_EMOJI = RichEmoji("white_heavy_check_mark").to_str()

    try:
        with console.status(
            "[bold blue]Setting up Quickstart Environment"
        ) as console_status:
            os.makedirs(directory, exist_ok=True)
            virtual_env_dir = os.path.abspath(directory + ".venv/")
            if reset and os.path.exists(virtual_env_dir):
                shutil.rmtree(virtual_env_dir)
            env = VirtualEnvironment(virtual_env_dir, python=python)
            console.print(
                f"{OK_EMOJI} Created Virtual Environment {RichEmoji('evergreen_tree').to_str()}"
            )

            # upgrade pip
            console_status.update("[bold blue]Installing pip")
            env.install("pip", options=["-U"])
            console.print(f"{OK_EMOJI} pip")

            # upgrade packaging
            console_status.update("[bold blue]Installing packaging")
            env.install("packaging", options=["-U"])
            console.print(f"{OK_EMOJI} packaging")

            # Install jupyter lab
            console_status.update("[bold blue]Installing Jupyter Lab")
            env.install("jupyterlab")
            env.install("ipywidgets")
            console.print(f"{OK_EMOJI} Jupyter Lab")

            # Install hagrid
            if EDITABLE_MODE:
                local_hagrid_dir = Path(
                    os.path.abspath(Path(hagrid_root()) / "../hagrid")
                )
                console_status.update(
                    f"[bold blue]Installing HAGrid in Editable Mode: {str(local_hagrid_dir)}"
                )
                env.install("-e " + str(local_hagrid_dir))
                console.print(
                    f"{OK_EMOJI} HAGrid in Editable Mode: {str(local_hagrid_dir)}"
                )
            else:
                console_status.update("[bold blue]Installing hagrid")
                env.install("hagrid", options=["-U"])
                console.print(f"{OK_EMOJI} HAGrid")
    except Exception as e:
        print(e)
        raise e


def add_intro_notebook(directory: str, reset: bool = False) -> str:
    filenames = ["00-quickstart.ipynb", "01-install-wizard.ipynb"]

    files = os.listdir(directory)
    try:
        files.remove(".venv")
    except Exception:  # nosec
        pass

    existing = 0
    for file in files:
        if file in filenames:
            existing += 1

    if existing != len(filenames) or reset:
        if EDITABLE_MODE:
            local_src_dir = Path(os.path.abspath(Path(hagrid_root()) / "../../"))
            for filename in filenames:
                file_path = os.path.abspath(f"{directory}/{filename}")
                shutil.copyfile(
                    local_src_dir / f"notebooks/quickstart/{filename}",
                    file_path,
                )
        else:
            for filename in filenames:
                url = (
                    "https://raw.githubusercontent.com/OpenMined/PySyft/dev/"
                    + f"notebooks/quickstart/{filename}"
                )
                file_path, _, _ = quickstart_download_notebook(
                    url=url, directory=directory, reset=reset
                )
    if arg_cache["install_wizard_complete"]:
        filename = filenames[0]
    else:
        filename = filenames[1]
    return os.path.abspath(f"{directory}/{filename}")


@click.command(help="Walk the Path", context_settings={"show_default": True})
@click.argument("zip_file", type=str, default="padawan.zip", metavar="ZIPFILE")
def dagobah(zip_file: str) -> None:
    if not os.path.exists(zip_file):
        for text in (
            f"{zip_file} does not exists.",
            "Please specify the path to the zip file containing the notebooks.",
            "hagrid dagobah [ZIPFILE]",
        ):
            print(text, file=sys.stderr)
        sys.exit(1)

    return run_quickstart(zip_file=zip_file)


cli.add_command(dagobah)


def ssh_into_remote_machine(
    host_ip: str,
    username: str,
    auth_type: str,
    private_key_path: str | None,
    cmd: str = "",
) -> None:
    """Access or execute command on the remote machine.

    Args:
        host_ip (str): ip address of the VM
        private_key_path (str): private key of the VM
        username (str): username on the VM
        cmd (str, optional): Command to execute on the remote machine. Defaults to "".
    """
    try:
        if auth_type == "key":
            subprocess.call(  # nosec
                ["ssh", "-i", f"{private_key_path}", f"{username}@{host_ip}", cmd]
            )
        elif auth_type == "password":
            subprocess.call(["ssh", f"{username}@{host_ip}", cmd])  # nosec
    except Exception as e:
        raise e


@click.command(
    help="SSH into the IP address or a resource group",
    context_settings={"show_default": True},
)
@click.argument("ip_address", type=str)
@click.option(
    "--cmd",
    type=str,
    required=False,
    default="",
    help="Optional: command to execute on the remote machine.",
)
def ssh(ip_address: str, cmd: str) -> None:
    kwargs: dict = {}
    key_path: str | None = None

    if check_ip_for_ssh(ip_address, timeout=10, silent=False):
        username = ask(
            question=Question(
                var_name="azure_username",
                question="What is the username for the VM?",
                default=arg_cache["azure_username"],
                kind="string",
                cache=True,
            ),
            kwargs=kwargs,
        )
        auth_type = ask(
            question=Question(
                var_name="auth_type",
                question="Do you want to login with a key or password",
                default=arg_cache["auth_type"],
                kind="option",
                options=["key", "password"],
                cache=True,
            ),
            kwargs=kwargs,
        )

        if auth_type == "key":
            key_path = ask(
                question=Question(
                    var_name="azure_key_path",
                    question="Absolute path to the private key of the VM?",
                    default=arg_cache["azure_key_path"],
                    kind="string",
                    cache=True,
                ),
                kwargs=kwargs,
            )

        # SSH into the remote and execute the command
        ssh_into_remote_machine(
            host_ip=ip_address,
            username=username,
            auth_type=auth_type,
            private_key_path=key_path,
            cmd=cmd,
        )


cli.add_command(ssh)


# Add hagrid logs command to the CLI
@click.command(
    help="Get the logs of the HAGrid node", context_settings={"show_default": True}
)
@click.argument("domain_name", type=str)
def logs(domain_name: str) -> None:  # nosec
    container_ids = (
        subprocess.check_output(  # nosec
            f"docker ps -qf name=^{domain_name}-*", shell=True
        )
        .decode("utf-8")
        .split()
    )
    Container = namedtuple("Container", "id name logs")
    container_names = []
    for container in container_ids:
        container_name = (
            subprocess.check_output(  # nosec
                "docker inspect --format '{{.Name}}' " + container, shell=True
            )
            .decode("utf-8")
            .strip()
            .replace("/", "")
        )
        log_command = "docker logs -f " + container_name
        container_names.append(
            Container(id=container, name=container_name, logs=log_command)
        )
    # Generate a table of the containers and their logs with Rich
    table = rich.table.Table(title="Container Logs")
    table.add_column("Container ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Container Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Log Command", justify="right", style="cyan", no_wrap=True)
    for container in container_names:  # type: ignore
        table.add_row(container.id, container.name, container.logs)  # type: ignore
    console = rich.console.Console()
    console.print(table)
    # Print instructions on how to view the logs
    console.print(
        rich.panel.Panel(
            long_string,
            title="How to view logs",
            border_style="white",
            expand=False,
            padding=1,
            highlight=True,
        )
    )


long_string = (
    "ℹ [bold green]To view the live logs of a container,copy the log command and paste it into your terminal.[/bold green]\n"  # noqa: E501
    + "\n"
    + "ℹ [bold green]The logs will be streamed to your terminal until you exit the command.[/bold green]\n"
    + "\n"
    + "ℹ [bold green]To exit the logs, press CTRL+C.[/bold green]\n"
    + "\n"
    + "🚨 The [bold white]backend,backend_stream & celery[/bold white] [bold green]containers are the most important to monitor for debugging.[/bold green]\n"  # noqa: E501
    + "\n"
    + "               [bold white]--------------- Ctop 🦾 -------------------------[/bold white]\n"
    + "\n"
    + "🧠 To learn about using [bold white]ctop[/bold white] to monitor your containers,visit https://www.youtube.com/watch?v=BJhlCxerQP4n \n"  # noqa: E501
    + "\n"
    + "               [bold white]----------------- How to view this. 🙂 ---------------[/bold white]\n"
    + "\n"
    + """ℹ [bold green]To view this panel again, run the command [bold white]hagrid logs {{NODE_NAME}}[/bold white] [/bold green]\n"""  # noqa: E501
    + "\n"
    + """🚨 NODE_NAME above is the name of your Hagrid deployment,without the curly braces. E.g hagrid logs canada [bold green]\n"""  # noqa: E501
    + "\n"
    + "               [bold green]HAPPY DEBUGGING! 🐛🐞🦗🦟🦠🦠🦠[/bold green]\n                      "
)

cli.add_command(logs)
