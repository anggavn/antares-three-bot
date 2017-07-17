#!/bin/bash

cd "$(dirname "$BASH_SOURCE")" || {
	echo "Python 3.5 doesn't seem to be installed" >&2
exit 1
}

#alwasys run with python3.5 bcs python3.6 fucks discord.py
python3.5 antares_three.py
