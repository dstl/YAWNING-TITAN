from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class bdist_wheel(_bdist_wheel):  # noqa
    def finalize_options(self):  # noqa
        super().finalize_options()
        # forces whee to be platform and Python version specific
        # Source: https://stackoverflow.com/a/45150383
        self.root_is_pure = False

setup(
    cmdclass={
        "bdist_wheel": bdist_wheel,
    }
)
