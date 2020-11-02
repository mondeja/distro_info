import io
import os
import re
import sys
from shutil import rmtree

from setuptools import setup, Command

# distro-info version + distro-info-data version
VERSION = '0.24.0.45'
PACKAGES = []
PY_MODULES = ["distro_info"]
SCRIPTS = ["debian-distro-info", "ubuntu-distro-info"]


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = [
        ("test", None, "Upload the package to PyPI test mirror."),
        ("username=", None, "Specify the username used uploading to PyPI."),
        ("password=", None, "Specify the password used uploading to PyPI."),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        self.username = None
        self.password = None
        self.test = None

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        except OSError:
            pass
        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(
            sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        cmd = "twine upload%s%s%s dist/*" % (
            " --repository-url https://test.pypi.org/legacy/"
            if self.test else "",
            " --password %s" % self.password if self.password else "",
            " --username %s" % self.username if self.username else "",
        )
        os.system(cmd)
        sys.exit()


setup(
    name="distro_info",
    version=VERSION,
    py_modules=PY_MODULES,
    packages=PACKAGES,
    test_suite="distro_info_test",
    entry_points={
        'console_scripts': [
            'debian-distro-info = debian_distro_info:main',
            'ubuntu-distro-info = ubuntu_distro_info:main',
        ],
    },
    package_data={"distro-info": ["debian.csv", "ubuntu.csv"]},
)
