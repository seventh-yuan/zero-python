#!/bin/sh

if [ "$#" -ge 1 ]; then
    if [ "$1" = "clean" ]; then
        rm -rf build
        exit 1
    else
        echo "------------------------------
Usage:
    build.sh [clean]
--------------------------------"
    exit 1
    fi
fi

mkdir -p build
cd build
cmake -DTOOLCHAIN_PREFIX=arm-fsl-linux-gnueabi- ..
make