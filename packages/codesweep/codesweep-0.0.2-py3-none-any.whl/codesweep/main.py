import typer

from ._core import lint_and_format, type_check
from ._utils import _display_config_summary

app = typer.Typer()


@app.command()
def config():
    """Displays the current configuration."""
    _display_config_summary()


@app.command()
def tidy(
    path: str = ".",
    fix: bool = typer.Option(False, "--fix", help="Automatically fix fixable errors."),
):
    """
    Lints the given directory or file using Ruff.
    """
    lint_and_format(path, fix)


@app.command()
def typecheck(path: str = "."):
    """
    Performs type checking using mypy.
    """
    type_check(path)


@app.command()
def sweep(
    path: str = typer.Option(".", help="The path to the directory or file to sweep."),
):
    """
    Runs linting and type checking as the default action.
    """
    lint_and_format(path, fix=True, verbose=False)
    type_check(path)


if __name__ == "__main__":
    app()
