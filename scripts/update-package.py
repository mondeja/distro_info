#!/usr/bin/env python3

"""Updates the package 'distro-info-data', if needed, because the version of
'distro-info-data' package has been updated."""

import hashlib
import os
import re
import shutil
import sys
import tarfile
from pkg_resources import parse_version
from urllib.request import Request, urlopen, urlretrieve

DISTRO_INFO_DATA_URLBASE = "http://ftp.debian.org/debian/pool/main/d/distro-info-data/"


def get_distro_info_data_latest_version():
    req = Request(DISTRO_INFO_DATA_URLBASE)
    res = urlopen(req)
    
    latest_version = None
    for line in res.read().decode("utf-8").splitlines():
        if "tar.xz" not in line:
            continue
        match = re.search('((\d+)\.(\d+)\.?(\d+)?)', line)
        if not match:
            continue
        version = parse_version(match.group(1).strip("."))
        if latest_version is None:
            latest_version = version
        else:
            if version > latest_version:
                latest_version = version
    return latest_version


def download_distro_info_data(version):
    filepath = f"distro-info-data_{version}.tar.xz"
    url = f"{DISTRO_INFO_DATA_URLBASE}{filepath}"
    req = Request(url)
    res = urlopen(req)
    urlretrieve(url, filepath)
    return filepath


def unzip_distro_info_data(filepath, version):
    with tarfile.open(filepath, "r") as f:
        f.extractall()
    return f"distro-info-data-{version}"


def hashfile(filepath): 
    BUF_SIZE = 65536 
    sha256 = hashlib.sha256() 
    with open(filepath, 'rb') as f: 
        while True:
            data = f.read(BUF_SIZE)
            if not data: 
                break
            sha256.update(data)
    return sha256.hexdigest()


def update_csvs(downloaded_directory_name):
    file_updated = False
    
    filenames = ["debian.csv", "ubuntu.csv"]
    for filename in filenames:
        source_filepath = os.path.join(downloaded_directory_name, filename)
        target_filepath = os.path.join("distro-info", filename)
        
        source_hash = hashfile(source_filepath)
        target_hash = hashfile(target_filepath)
        
        if source_hash != target_hash:
            os.remove(target_filepath)
            shutil.copyfile(source_filepath, target_filepath)
            sys.stdout.write(f"'{target_filepath}' file updated.\n")
            file_updated = True
    return file_updated


def cleanup(version, downloaded_directory_name):
    if os.path.exists(downloaded_directory_name):
        shutil.rmtree(downloaded_directory_name)
    filename = f"distro-info-data_{version}.tar.xz"
    if os.path.exists(filename):
        os.remove(filename)


def update_setup_version(distro_info_data_version):
    new_setup_content = ''
    with open("setup.py", "r") as f:
        lines = f.read()
    
    for line in lines.split("\n"):
        if line.startswith("VERSION ="):
            previous_version = line.split("= ")[1].strip("'")
            new_version = '.'.join(
                previous_version.split(".")[0:2] +
                [str(distro_info_data_version)])
            line = f"VERSION = '{new_version}'"
        new_setup_content += f"{line}\n"
    os.remove("setup.py")
    with open("setup.py", "w") as f:
        f.write(new_setup_content)
    

def main():
    err, version, downloaded_directory_name, file_updated = (
        None, "", "", False)
    try:
        # distro-info-data update
        version = get_distro_info_data_latest_version()
        filepath = download_distro_info_data(version)
        downloaded_directory_name = unzip_distro_info_data(filepath, version)
        file_updated = update_csvs(downloaded_directory_name)
        if file_updated:
            update_setup_version(version)
    except Exception as exception:
        err = exception
    finally:
        cleanup(version, downloaded_directory_name)
        if err:
            raise err
    if file_updated:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())