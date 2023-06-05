def run(overwrite_existing: bool = True):
    """
    Resets the default jupyter notebooks in the app notebooks directory.

    :param overwrite_existing: A bool to toggle replacing existing edited
        notebooks on or off.
    :return:
    """
    import filecmp
    import os
    import shutil
    from logging import getLogger
    from pathlib import Path

    from yawning_titan import NOTEBOOKS_DIR

    try:
        # Attempt to import Yawning-Titan to leverage its logging config
        import yawning_titan  # noqa
    except ImportError:
        pass

    logger = getLogger("scripts.reset_default_notebooks")

    # The users Yawning-Titan notebook directory

    # The root dir of notebook package data in the library
    lib_notebooks = Path(__file__).parent.parent / "notebooks"
    default_notebooks_root = os.path.join(lib_notebooks, "_package_data")

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
                    logger.info(f"Created subdirectory: {target_subdir}")
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
                logger.info(f"Reset default notebook: {target_fp}")


if __name__ == "__main__":
    run(True)
