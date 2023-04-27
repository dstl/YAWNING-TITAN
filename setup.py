import sys

from setuptools import find_packages, setup

from package_data import get_package_data

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):  # noqa
        def finalize_options(self):  # noqa
            super().finalize_options()
            # forces whee to be platform and Python version specific
            # Source: https://stackoverflow.com/a/45150383
            self.root_is_pure = False

except ImportError:
    bdist_wheel = None


def version() -> str:
    """
    Gets the version from the `VERSION` file.

    :return: The version string.
    """
    with open("yawning_titan/VERSION", "r") as file:
        return file.readline().strip()


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
    description="An abstract, flexible and configurable cyber security simulation",
    python_requires=">=3.8, <3.11",
    version=version(),
    license="MIT License",
    packages=find_packages(exclude=["network_editor"]),
    install_requires=[
        "dm-tree==0.1.7",
        "gym==0.21.0",
        "imageio==2.9.0",
        "jupyterlab==3.6.1",
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
        "tinydb==4.7.0",
        "tensorboard==2.11.0",
        "tinydb==4.7.0",
        "torch==1.13.1",
        "typer[all]==0.7.0",
        "typing-extensions==4.4.0",
        "Django==4.2",
        "flaskwebgui==1.0.1",
        "django-cors-headers==3.14.0"
    ],
    extras_require={
        "dev": [
            "furo==2023.3.27",
            "nbmake==1.3.5",
            "pip-licenses==4.0.2",
            "pre-commit==2.20.0",
            "pytest==7.2.0",
            "pytest-django==4.5.2",
            "pytest-cov==4.0.0",
            "pytest-flake8==1.1.1",
            "setuptools==66",
            "sphinx==5.3.0",
            "sphinx-code-tabs==0.5.3",
            "sphinx-copybutton==0.5.2",
            "wheel",
        ],
        "tensorflow": ["tensorflow==2.11.0"],
    },
    package_data=get_package_data(),
    data_files=[("./yawning_titan", ["package_data.py", "yawning_titan/VERSION"])],
    include_package_data=True,
    cmdclass={
        "bdist_wheel": bdist_wheel,
    },
    entry_points={
        "console_scripts": [
            "yawning-titan = yawning_titan.main:app",
        ],
    },
)
