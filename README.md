# distro_info

Python implementation mirror of [Debian distro-info utility][distro-info-link].

[distro-info-link]: https://salsa.debian.org/debian/distro-info/-/tree/master/python

## Installation

```bash
pip install debian-distro-info
```

## Usage

```bash
from distro_info import DebianDistroInfo, UbuntuDistroInfo

di = UbuntuDistroInfo()
print(di._releases)
```