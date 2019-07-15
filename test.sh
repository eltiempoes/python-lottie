#!/bin/bash
HERE="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

if [ "$#" -gt 0 ]
then
    python3 -m unittest "$@"
elif which coverage &>/dev/null
then
    coverage erase
    coverage run --branch --source="$HERE/lib" -m unittest discover -t "$HERE" -s test && \
    coverage html && \
    coverage report --skip-covered && \
    echo "file://$HERE/htmlcov/index.html"
else
    python3 -m unittest discover -t "$HERE" -s test
fi
