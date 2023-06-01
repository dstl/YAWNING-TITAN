from logging import getLogger

from yawning_titan import (
    _YT_USER_DIRS,
    PPO_TENSORBOARD_LOGS_DIR,
    AGENTS_DIR,
    AGENTS_LOGS_DIR,
    VIDEOS_DIR,
    IMAGES_DIR,
    GAME_MODES_DIR,
    NOTEBOOKS_DIR,
    DB_DIR,
    LOG_DIR,
    APP_IMAGES_DIR
)

_LOGGER = getLogger(__name__)


def run():
    """
    Handles creation of application directories and user directories.

    Uses `platformdirs.PlatformDirs` and `pathlib.Path` to create the required
    app directories in the correct locations based on the users OS.
    """
    app_dirs = [
        _YT_USER_DIRS,
        PPO_TENSORBOARD_LOGS_DIR,
        AGENTS_DIR,
        AGENTS_LOGS_DIR,
        VIDEOS_DIR,
        IMAGES_DIR,
        GAME_MODES_DIR,
        NOTEBOOKS_DIR,
        DB_DIR,
        LOG_DIR,
        APP_IMAGES_DIR
    ]

    for app_dir in app_dirs:
        if not app_dir.is_dir():
            app_dir.mkdir(parents=True, exist_ok=True)
            _LOGGER.info(f"Created directory: {app_dir}")


if __name__ == "__main__":
    run()
