import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def _create_app_dirs():
    """
    Handles creation of application directories and user directories.

    Uses `platformdirs.PlatformDirs` and `pathlib.Path` to create the required app directories in the correct
    locations based on the users OS.
    """
    import sys
    from pathlib import Path, PosixPath
    from typing import Final, Union

    try:
        from platformdirs import PlatformDirs

        _YT_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs(appname="yawning_titan")
        """An instance of `PlatformDirs` set with appname='yawning_titan'."""

        app_dirs = [_YT_PLATFORM_DIRS.user_data_path]
        if sys.platform == "win32":
            app_dirs.append(_YT_PLATFORM_DIRS.user_data_path / "config")
            app_dirs.append(_YT_PLATFORM_DIRS.user_data_path / "logs")
            _YT_USER_DIRS: Final[Union[Path, PosixPath]] = Path.home() / "yawning_titan"
        else:
            app_dirs.append(_YT_PLATFORM_DIRS.user_config_path)
            app_dirs.append(_YT_PLATFORM_DIRS.user_log_path)
            _YT_USER_DIRS: Final[Union[Path, PosixPath]] = Path.home() / "yawning_titan"

        app_dirs.append(_YT_PLATFORM_DIRS.user_data_path / "docs")
        app_dirs.append(_YT_PLATFORM_DIRS.user_data_path / "db")
        app_dirs.append(_YT_PLATFORM_DIRS.user_data_path / "app_images")
        app_dirs.append(_YT_USER_DIRS / "notebooks")
        app_dirs.append(_YT_USER_DIRS / "game_modes")
        app_dirs.append(_YT_USER_DIRS / "images")
        app_dirs.append(_YT_USER_DIRS / "agents")
        app_dirs.append(_YT_USER_DIRS / "agents" / "logs" / "tensorboard")

        for app_dir in app_dirs:
            app_dir.mkdir(parents=True, exist_ok=True)
    except ImportError:
        pass


def _copy_package_data_notebooks_to_notebooks_dir():
    """
    Call the reset_default_jupyter_notebooks without overwriting if notebooks are already there.

    As this is a post install script, it should be possible to import Yawning-Titan, but it may not. This
    `ImportError` is handled so that setup doesn't fail.
    """
    try:
        from yawning_titan.notebooks.jupyter import reset_default_jupyter_notebooks

        reset_default_jupyter_notebooks(overwrite_existing=False)
    except ImportError:
        # Failed as, although this is a post-install script, YT can't be imported
        pass


class PostDevelopCommand(develop):
    """Post-installation command class for development mode."""

    def run(self):
        """Run the installation command then create the app dirs."""
        develop.run(self)
        _create_app_dirs()
        _copy_package_data_notebooks_to_notebooks_dir()


class PostInstallCommand(install):
    """Post-installation command class for installation mode."""

    def run(self):
        """Run the installation command then create the app dirs."""
        install.run(self)
        _create_app_dirs()
        _copy_package_data_notebooks_to_notebooks_dir()


def _ray_3_beta_rllib_py_platform_pip_install() -> str:
    """
    Python version and OS version map to ray 3.0.0.dev0 .whel.

    Maps the operating system and the Python version to the relevant .whl
    file for Ray 3.0.0.dev0 beta version. Uses it to build a pip install
    string for installing Ray 3.0.0.dev0 with the [rllib] extra.

    whl source: https://docs.ray.io/en/master/ray-overview/installation.html

    * A temporary measure to allow for use on Linux, Windows, and MacOS
    while we wait for ray 3.0.0 release with full Windows support. *

    Returns: A pip install string to install Ray 3.0.0.dev0 with the [rllib]
        extra for the given OS and Python version.
    Raises EnvironmentError: When either the operating system is not
        supported or the Python version is not supported.
    """
    ray_wheels_root = "https://s3-us-west-2.amazonaws.com/ray-wheels/latest"
    ray_3_py_platform_map = {
        "linux": {  # Linux
            (3, 8): "/ray-3.0.0.dev0-cp38-cp38-manylinux2014_x86_64.whl",
            (3, 9): "/ray-3.0.0.dev0-cp39-cp39-manylinux2014_x86_64.whl",
            (3, 10): "/ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl",
        },
        "darwin": {  # MacOSX
            (3, 8): "/ray-3.0.0.dev0-cp38-cp38-macosx_10_15_x86_64.whl",
            (3, 9): "/ray-3.0.0.dev0-cp39-cp39-macosx_10_15_x86_64.whl",
            (3, 10): "/ray-3.0.0.dev0-cp310-cp310-macosx_10_15_universal2.whl",
        },
        "win32": {  # Windows
            (3, 8): "/ray-3.0.0.dev0-cp38-cp38-win_amd64.whl",
            (3, 9): "/ray-3.0.0.dev0-cp39-cp39-win_amd64.whl",
            (3, 10): "/ray-3.0.0.dev0-cp310-cp310-win_amd64.whl",
        },
    }
    py_v = sys.version_info
    py_v_major_minor = py_v[:2]
    if sys.platform in ray_3_py_platform_map.keys():
        if py_v_major_minor in ray_3_py_platform_map[sys.platform].keys():
            ray_whl = ray_3_py_platform_map[sys.platform][py_v_major_minor]
            whl_url = f"{ray_wheels_root}{ray_whl}"
            return f"ray[rllib] @ {whl_url}"
        else:
            #  Python version not supported
            raise EnvironmentError(
                f"yawningtitan with ray on {sys.platform} is only supported "
                f"by Python versions 3.8.*, 3.9.*, and 3.10.*, currently using "
                f"python version {py_v.major}.{py_v.minor}.{py_v.micro}"
            )
    else:
        #  OS not supported
        raise EnvironmentError(
            f"yawningtitan with ray is only supported by Linux (linux), Windows (win32),"
            f" and MacOS (darwin), currently using {sys.platform}"
        )


setup(
    name="yawningtitan",
    maintainer="Defence Science and Technology Laboratory UK",
    maintainer_email="oss@dstl.gov.uk",
    url="https://github.com/dstl/YAWNING-TITAN",
    description="An abstract, flexible and configurable cyber security " "simulation",
    python_requires=">=3.8, <3.11",
    version="1.0.1",
    license="MIT License",
    packages=find_packages(),
    install_requires=[
        "dm-tree==0.1.7",
        "gym==0.21.0",
        "imageio==2.9.0",
        "jupyter==1.0.0",
        "karateclub==1.3.0",
        "matplotlib==3.6.2",
        "networkx==2.5.1",
        "numpy==1.23.4",
        "pandas==1.3.5",
        "platformdirs==2.5.2",
        "pyyaml==5.4.1",
        _ray_3_beta_rllib_py_platform_pip_install(),
        "scipy==1.9.2",
        "seaborn==0.12.1",
        "stable_baselines3==1.6.2",
        "tabulate==0.8.9",
        "tensorboard==2.11.0",
        "torch==1.12.1",
        "typing-extensions==4.4.0",
    ],
    extras_require={
        "dev": [
            "nbmake==1.3.5",
            "pip-licenses==4.0.2",
            "pre-commit==2.20.0",
            "pytest==7.2.0",
            "pytest-cov==4.0.0",
            "pytest-flake8==1.1.1",
            "sphinx==5.3.0",
            "sphinx_rtd_theme==1.1.1",
        ],
        "tensorflow": ["tensorflow==2.11.0"],
    },
    package_data={
        "yawning_titan": [
            "config/_package_data/logging_config.yaml",
            "config/_package_data/game_modes/default_game_mode.yaml",
            "config/_package_data/game_modes/dcbo_config.yaml",
            "config/_package_data/game_modes/low_skill_red_with_random_infection_perfect_detection.yaml",
            "notebooks/_package_data/sb3/End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering.ipynb",
            "notebooks/_package_data/sb3/Using an Evaluation Callback to monitor progress during training.ipynb",
            "notebooks/_package_data/Creating and playing as a Keyboard Agent.ipynb",
        ]
    },
    include_package_data=True,
    cmdclass={"install": PostInstallCommand, "develop": PostDevelopCommand},
)
