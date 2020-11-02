import io
import os
import re
import sys
from shutil import rmtree

from setuptools import setup, Command

# distro-info version + distro-info-data version
VERSION = '0.24.0.45a5'


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
            rmtree(os.path.join(os.path.dirname(__file__), "dist"))
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
    name="debian-distro-info",
    version=VERSION,
    packages=['distro_info'],
    entry_points={
        'console_scripts': [
            'debian-distro-info = distro_info.debian_distro_info:main',
            'ubuntu-distro-info = distro_info.ubuntu_distro_info:main',
        ],
    },
    package_data={"distro_info": ["distro_info/debian.csv",
                                  "distro_info/ubuntu.csv"]},
    include_package_data=True,
    cmdclass={
        'upload': UploadCommand,
    },
    zip_safe=False,
)
