#!/usr/bin/env sh
set -e

cd /source
make install
tox
