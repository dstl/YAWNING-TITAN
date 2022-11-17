"""
The Jupyter module.

The jupyter module handles 'resetting' the default Jupyter notebooks in the app jupyter directory, and for starting a
new jupyter notebook environment.
"""
import filecmp
import importlib.util
import os
import shutil
import subprocess
import sys
from logging import getLogger

from yawning_titan import NOTEBOOKS_DIR

_LOGGER = getLogger(__name__)


def reset_default_jupyter_notebooks(overwrite_existing: bool = True):
    """
    Resets the default jupyter notebooks in the app notebooks directory.

    This is done by copying the templates over from the library notebooks package data if they do not already exist.
    If a notebook does already exist, but it has been edited, passing overwrite_existing=True as a parameter will
    replace the edited notebook with the original.

    Default notebooks:
    ------------------
    - Creating and playing as a Keyboard Agent.ipynb
    - sb3/End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering.ipynb
    - sb3/Using an Evaluation Callback to monitor progress during training.ipynb

    Args:
        overwrite_existing: A bool to toggle replacing existing edited
            notebooks on or off.
    """
    from yawning_titan import NOTEBOOKS_DIR
    from yawning_titan.notebooks import _LIB_NOTEBOOKS_ROOT_PATH

    default_notebooks_root = os.path.join(_LIB_NOTEBOOKS_ROOT_PATH, "_package_data")
    for subdir, dirs, files in os.walk(default_notebooks_root):
        if subdir != default_notebooks_root:
            lib_subdir = str(subdir).split(os.sep)[-1]
            if lib_subdir == ".ipynb_checkpoints":
                continue
            if lib_subdir:
                target_subdir = os.path.join(NOTEBOOKS_DIR, lib_subdir)
                if not os.path.isdir(target_subdir):
                    # Create new subdirectory in the app notebooks
                    # directory
                    os.mkdir(target_subdir)
                    _LOGGER.info(f"Created subdirectory: {target_subdir}")
        for file in files:
            fp = os.path.join(subdir, file)
            path_split = fp.replace(default_notebooks_root, "").split(os.sep)
            target_fp = os.path.join(NOTEBOOKS_DIR, *path_split)
            copy_file = not os.path.isfile(target_fp)
            if overwrite_existing:
                if not copy_file:
                    # Exists, but check if files match
                    copy_file = not filecmp.cmp(fp, target_fp)
            if copy_file:
                shutil.copy2(fp, target_fp)
                _LOGGER.info(f"Reset default notebook: {target_fp}")


# Ensures default notebooks exist in the directory without overwriting
reset_default_jupyter_notebooks(overwrite_existing=False)


def start_jupyter_session():
    """Starts a new Jupyter notebook session. in the app notebooks directory. Currently only works on Windows OS."""
    reset_default_jupyter_notebooks(overwrite_existing=False)
    # TODO: Figure out how to get this working for Linux and MacOS too.
    if sys.platform == "win32":
        if importlib.util.find_spec("jupyter") is not None:
            # Jupyter is installed
            working_dir = os.getcwd()
            os.chdir(NOTEBOOKS_DIR)
            subprocess.Popen("jupyter notebook")
            os.chdir(working_dir)
        else:
            # Jupyter is not installed
            _LOGGER.error("Cannot start jupyter notebook as it is not installed")
    else:
        _LOGGER.error("Feature currently supported on Windows OS.")
