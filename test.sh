#!/bin/bash
HERE="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

if [ "$#" -gt 0 ]
then
    python3 -m unittest "$@"
else
    python3 -m unittest discover -t "$HERE" -s test
fi
