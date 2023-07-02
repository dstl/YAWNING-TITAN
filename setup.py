from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel  # noqa


class bdist_wheel(_bdist_wheel):  # noqa
    def finalize_options(self):  # noqa
        super().finalize_options()
        # Set to False if you need to build OS and Python specific wheels
        self.root_is_pure = True  # noqa


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
        "torch==2.0.0",
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
