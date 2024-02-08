#!/usr/bin/env bash

directory=$(dirname "${BASH_SOURCE}")
python3 "${directory}/yank.py" "$@"
