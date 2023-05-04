import os
from pathlib import Path
from typing import Dict, List, Optional


def _get_all_files_and_sub_dirs(
    root_dir: str,
    split_by_parent: bool = True,
    ignore_files: Optional[List[str]] = None,
    ignore_file_types: Optional[List[str]] = None,
) -> List[str]:
    if not ignore_files:
        ignore_files = []
    if not ignore_file_types:
        ignore_file_types = []

    filepaths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            add = True
            file_type = file.split(".")[-1]

            if file_type in ignore_file_types:
                add = False
            if add and f".{file_type}" in ignore_file_types:
                add = False
            if add and file in ignore_files:
                add = False

            if add:
                file_path = Path(os.path.join(root, file)).as_posix()
                split_by = Path(root_dir)

                if split_by_parent:
                    split_by = split_by.parent
                split_by = split_by.as_posix()

                filepaths.append(file_path.split(split_by)[-1][1:])
    return filepaths


def _yawning_titan_gui_package_data() -> List[str]:
    static_files = _get_all_files_and_sub_dirs(root_dir="yawning_titan_gui/static")
    template_files = _get_all_files_and_sub_dirs(root_dir="yawning_titan_gui/templates")
    return static_files + template_files


def _yawning_titan_package_data() -> List[str]:
    """
    Get the list of package data files in the yawning_titan directory.

    :return: A list of string paths.
    """
    filepaths = ["VERSION"]
    for root, dirs, files in os.walk("yawning_titan"):
        if root.split(os.sep)[-1] == "_package_data":
            for file in files:
                file_path = Path(os.path.join(root, file)).as_posix()
                filepaths.append(file_path.split("yawning_titan")[-1][1:])
    return filepaths


def get_package_data() -> Dict[str, List[str]]:
    """
    Dynamically generate the package data.

    :return: A dict containing package data for yawning_titan and
        yawning_titan_gui.
    """
    return {
        "yawning_titan": _yawning_titan_package_data(),
        "yawning_titan_gui": _yawning_titan_gui_package_data(),
    }
