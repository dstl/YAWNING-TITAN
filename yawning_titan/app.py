"""The app module handles configuration at the application level."""
import os.path
from pathlib import Path


def create_app_dirs():
    """
    Uses platformdirs to create the required app directories in the correct
    locations based on the users OS.
    """
    from platformdirs import PlatformDirs

    dirs = PlatformDirs(appname="yawning_titan", appauthor="DSTL")

    # Creates the app config directory
    dirs.user_config_path.mkdir(parents=True, exist_ok=True)

    # Creates the app log directory
    dirs.user_log_path.mkdir(parents=True, exist_ok=True)

    # Creates the app data directory
    dirs.user_data_path.mkdir(parents=True, exist_ok=True)

    # Sets and creates the app game modes directory
    game_modes_dir = os.path.join(dirs.user_config_path, "game_modes")
    Path(game_modes_dir).mkdir(parents=True, exist_ok=True)

    # Sets and creates the app notebooks directory
    notebooks_dir = os.path.join(dirs.user_data_path, "notebooks")
    Path(notebooks_dir).mkdir(parents=True, exist_ok=True)

    # Sets and creates the app docs directory
    docs_dir = os.path.join(dirs.user_data_path, "docs")
    Path(docs_dir).mkdir(parents=True, exist_ok=True)

    # Sets and creates the app images directory
    docs_dir = os.path.join(dirs.user_data_path, "images")
    Path(docs_dir).mkdir(parents=True, exist_ok=True)
