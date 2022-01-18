#!/bin/env bash

set -e

read -r -p "This script requires root permissions, please acknowledge that it is being run as root. [y|N]: "
if ! [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Aborting"
    exit 1
fi

echo "Updating script permissions."
chmod u+x scripts/dbrun.py

echo "Linking to bin."
sudo ln scripts/dbrun.py /usr/local/bin/dbrun

echo "Done, Enjoy :)"