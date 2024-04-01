import re
import subprocess
from pathlib import Path
from typing import List, Tuple, Union

import typer
from rich import print

from ._utils import copy_config_file, update_mypy_ini


def run_subprocess(command: List[str], verbose: bool = True) -> Tuple[int, str, str]:
    """
    Runs a subprocess command and returns its exit status, stdout, and stderr.

    Parameters:
    - command: List[str]: The subprocess command to run.
    - verbose: bool: If True (default), prints the command's output and errors. If False, suppresses them.

    Returns:
    - Tuple[int, str, str]: A tuple containing the exit status, stdout, and stderr of the subprocess command.
    """
    result: Union[subprocess.CompletedProcess, subprocess.CalledProcessError]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        exit_status = result.returncode
    except subprocess.CalledProcessError as e:
        exit_status = e.returncode
        result = e
    finally:
        stdout = result.stdout if result.stdout else ""
        stderr = result.stderr if result.stderr else ""

        if verbose:
            if stdout:
                print(
                    f"[bold green]{stdout}"
                ) if "success" in stdout.lower() else print(stdout)
            if stderr:
                print(f"[bold red]{stderr}")

    return exit_status, stdout, stderr


def lint_and_format(path: str, fix: bool, verbose: bool = True) -> None:
    """
    Performs the linting process, including initial checks, formatting, and final checks.

    Parameters:
    - path: str: The path to the file or directory to lint.
    - fix: bool: If True, fixes fixable errors.
    - verbose: bool: If True (default), prints the command's output and errors. If False, suppresses them.

    Returns:
    - None
    """
    copy_config_file(Path("."), "ruff.toml")
    run_subprocess(["ruff", "check", "--select", "I", "--fix", path], verbose=False)
    run_subprocess(["ruff", "format", path])

    final_check_command = ["ruff", "check", path]
    if fix:
        final_check_command.append("--fix")
    _, stdout, _ = run_subprocess(final_check_command, verbose=verbose)

    if "passed" in stdout.strip():
        return

    if (
        not fix
        and stdout.strip()
        and typer.confirm("Would you like to run fixes for fixable errors?")
    ):
        lint_and_format(path, fix=True)


def type_check(path: str) -> None:
    """
    Performs type checking using mypy.

    Parameters:
    - path: str: The path to the file or directory to type check.

    Returns:
    - None
    """
    copy_config_file(Path("."), "mypy.ini")
    _, stdout, _ = run_subprocess(["mypy", path])

    if "stubs not installed" in stdout:
        match = re.search(r"Library stubs not installed for \"([^\"]+)\"", stdout)
        if match:
            library_name = match.group(1)
            if typer.confirm(
                f"Would you like to ignore {library_name} for type checking?"
            ):
                update_mypy_ini(library_name)
