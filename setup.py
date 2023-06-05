from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel  # noqa


class bdist_wheel(_bdist_wheel):  # noqa
    def finalize_options(self):  # noqa
        super().finalize_options()
        # Set to False if you need to build OS and Python specific wheels
        self.root_is_pure = True  # noqa


setup(
    cmdclass={
        "bdist_wheel": bdist_wheel,
    }
)
