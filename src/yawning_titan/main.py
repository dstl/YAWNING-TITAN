"""Provides a CLI using Typer as an entry point."""
import os
import sys

import typer

app = typer.Typer()


@app.command()
def gui():
    """Start the Yawning-Titan GUI."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "yawning_titan_server.settings.prod")
    from django.core.management import execute_from_command_line

    """Method that is fired on execution of the command in the terminal."""
    execute_from_command_line(["runserver", "run_gui"])

@app.command()
def build_dirs():
    """Build the Yawning-Titan app directories."""
    from yawning_titan.utils import setup_app_dirs

    setup_app_dirs.run()


@app.command()
def reset_db(rebuild: bool = False):
    """
    Force a reset of the default entries in the NetworkDB and GameModeDB.

    :param rebuild: If True, completely rebuild the DB, removing all custom
        Networks and GameModes. Default value is False.
    """
    from yawning_titan.utils import reset_network_and_game_mode_db_defaults

    reset_network_and_game_mode_db_defaults.run(rebuild)


@app.command()
def reset_notebooks(overwrite: bool = True):
    """
    Force a reset of the default notebooks in the users notebooks directory.

    :param overwrite: If True, will overwrite existing default notebooks.
    """
    from yawning_titan.utils import reset_default_notebooks

    reset_default_notebooks.run(overwrite)


@app.command()
def logs(last_n: int = 10):
    """
    Print the Yawning-Titan log file.

    :param last_n: The number of lines to print. Default value is 10.
    """
    import re

    from platformdirs import PlatformDirs

    yt_platform_dirs = PlatformDirs(appname="yawning_titan")

    if sys.platform == "win32":
        log_dir = yt_platform_dirs.user_data_path / "logs"
    else:
        log_dir = yt_platform_dirs.user_log_path
    log_path = os.path.join(log_dir, "yawning_titan.log")

    if os.path.isfile(log_path):
        with open(log_path) as file:
            lines = file.readlines()
        for line in lines[-last_n:]:
            print(re.sub(r"\n*", "", line))


@app.command()
def notebooks():
    """Start Jupyter Lab in the users Yawning-Titan notebooks directory."""
    from yawning_titan.notebooks.jupyter import start_jupyter_session

    start_jupyter_session()


@app.command()
def docs():
    """View the Yawning-Titan docs."""
    import webbrowser

    webbrowser.open("https://dstl.github.io/YAWNING-TITAN/", new=2)


@app.command()
def version():
    """Get the installed Yawning-Titan version number."""
    import yawning_titan

    print(yawning_titan.__version__)


@app.command()
def release_notes():
    """View the GitHub release notes of the installed Yawning-Titan version."""
    import webbrowser

    import yawning_titan

    v = yawning_titan.__version__
    url = f"https://github.com/dstl/YAWNING-TITAN/releases/tag/v{v}"

    webbrowser.open(url, new=2)


@app.command()
def setup():
    """
    Perform the Yawning-Titan first-time setup.

    WARNING: All user-data will be lost.
    """
    from yawning_titan.utils import setup_app_dirs
    from yawning_titan.utils import reset_network_and_game_mode_db_defaults
    from yawning_titan.utils import reset_default_notebooks
    print("Performing the Yawning-Titan first-time setup...")
    print()

    print("Building the Yawning-Titan app directories...")
    setup_app_dirs.run()
    print()

    print("Rebuilding the NetworkDB and GameModeDB...")
    reset_network_and_game_mode_db_defaults.run(rebuild=True)
    print()

    print("Rebuilding the default notebooks...")
    reset_default_notebooks.run(overwrite_existing=True)
    print()

    print("Setup complete!")


if __name__ == "__main__":
    app()
