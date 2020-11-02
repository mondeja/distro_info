#!/bin/bash

setup_git() {
  git config --global user.email "travis@travis-ci.com"
  git config --global user.name "Travis CI"
}

commit_files() {
  git add -f distro-info
  git add -f setup.py
  git commit -m "Update 'distro-info-data' version"
}

push() {
  git remote set-url origin \
    "https://mondeja:$GITHUB_PASSWORD@github.com/mondeja/distro_info.git" \
    > /dev/null 2>&1
  git push --quiet origin HEAD:master
}

setup_git
commit_files
push