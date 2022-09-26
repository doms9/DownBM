#!/bin/bash

if [ -f ./DownBM.exe ] || [ -f ./DownBM ]; then
    printf "Executable exists..."
    exit
else
    [ -d ./Build/ ] || mkdir Build

    [ -x "$(command -v pyinstaller)" ] && printf "Building...\n" || python3 -m pip install pyinstaller

    pyinstaller -Fy --console ./source.pyw --distpath="./" --workpath="./Build/" --specpath="./Build/" -i="../icon.ico" -n="DownBM"

    rm -rf ./Build/

    printf "\nSuccessfully built DownBM!"
fi
