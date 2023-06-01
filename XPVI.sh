#!/bin/bash
pushd $(dirname "$BASH_SOURCE") > /dev/null
if command -v python3 &> /dev/null
then
    python3 XPVI.py "${@:1}"
else
    python XPVI.py "${@:1}"
fi
popd > /dev/null
