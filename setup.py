import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """
     Post-installation command class for development mode.
     """

    def run(self):
        develop.run(self)
        from yawning_titan.config.app import create_app_dirs
        create_app_dirs()


class PostInstallCommand(install):
    """
    Post-installation command class for installation mode.
    """

    def run(self):
        install.run(self)
        from yawning_titan.config.app import create_app_dirs
        create_app_dirs()


def _ray_3_beta_rllib_py_platform_pip_install() -> str:
    """
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
        }
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
    description="An abstract, flexible and configurable cyber security "
                "simulation",
    python_requires=">=3.8",
    version="0.1.0",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "gym==0.21.0",
        "imageio==2.9.0",
        "matplotlib==3.6.1",
        "networkx==2.5.1",
        "numpy==1.23.4",
        _ray_3_beta_rllib_py_platform_pip_install(),
        "scipy==1.9.2",
        "stable_baselines3==1.6.2",
        "tabulate==0.8.9",
        "karateclub==1.3.0",
        "pandas==1.3.5",
        "platformdirs==2.5.2",
        "pyyaml==5.4.1",
        "typing-extensions==4.0.1",
        "torch==1.12.1 ",
        "tensorboard==2.10.1 ",
        "dm-tree==0.1.7",
        "ruamel.yaml>=0.17.21"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-flake8",
            "pytest-cov",
            "pip-licenses",
            "sphinx_rtd_theme",
            "sphinx",
            "pre-commit",
        ],
        "tensorflow": ["tensorflow"],  # TODO: Determine version and lock it in
        "jupyter": ["jupyter"]
    },
    package_data={
        "yawning_titan": [
            "config/_package_data/logging_config.yaml"
            "config/_package_data/game_modes/default_game_mode.yaml",
            "config/_package_data/game_modes/low_skill_red_with_random_infection_perfect_detection.yaml",
            "notebooks/_package_data/sb3/End to End Generic Env Example - Env Creation, Agent Train and Agent Rendering.ipynb",
            "notebooks/_package_data/sb3/Using an Evaluation Callback to monitor progress during training.ipynb",
            "notebooks/_package_data/Creating and playing as a Keyboard Agent.ipynb",
        ]
        # TODO: Determine whether tests config needs to be included in
        #  package_data to be able to run tests from installed YT rather
        #  than from cloned repo directory.
    },
    include_package_data=True,
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand
    }
)
