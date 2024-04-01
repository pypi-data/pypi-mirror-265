import shutil
from pathlib import Path

import toml
from rich import print
from rich.table import Table

CONFIG_DIR = Path(__file__).parent / "_config"


def _load_config(file_path):
    """
    Load and parse the ruff TOML configuration file.
    """
    with open(file_path, "r") as toml_file:
        config = toml.load(toml_file)
    return config


def _display_table(title, settings):
    """
    Create and print a table given a title and settings.
    """
    table = Table(title=title)
    table.add_column("Setting", style="bold magenta")
    table.add_column("Value", style="green")
    for setting, value in settings.items():
        table.add_row(setting, str(value))
    print(table)


def _display_config_summary():
    """
    Display the configuration summary by loading the config and creating tables.
    """
    config = _load_config(CONFIG_DIR / "ruff.toml")
    format_settings = config.pop("format", {})
    lint_settings = config.pop("lint", {})
    general_settings = config

    _display_table("General Configuration", general_settings)
    if lint_settings:
        _display_table("Linting Configuration", lint_settings)
    if format_settings:
        _display_table("Formatting Configuration", format_settings)


def update_mypy_ini(library_name: str) -> None:
    ini_path = CONFIG_DIR / "mypy.ini"
    config_section = f"\n[mypy-{library_name}.*]\nignore_missing_imports = True"
    with open(ini_path, "a") as file:
        file.write(f"\n{config_section}")
    print(f"Updated mypy.ini to ignore missing imports for {library_name}.")


def copy_config_file(destination_dir: Path, config_filename: str) -> None:
    """
    Copies a configuration file from the internal 'config' directory to the specified destination directory.

    Parameters:
    - destination_dir (Path): The directory to copy the files to.
    - config_filename (str): The filename (or relative path within the 'config' directory) of the configuration file to copy.
    """
    try:
        file_location = CONFIG_DIR / config_filename
        destination_dir.mkdir(parents=True, exist_ok=True)
        dest_file_path = destination_dir / config_filename
        shutil.copy2(file_location, dest_file_path)
    except shutil.Error as e:
        print(f"An error occurred while copying: {e}")
