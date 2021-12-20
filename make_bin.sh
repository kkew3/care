#!/bin/bash
set -e

if [ -n "$VIRTUAL_ENV" ] && python3 -c "import libarchive.public" 2> /dev/null; then
    mkdir -p bin
    { printf "#!%s\n" "$(command -v python3)"; cat care.py } > bin/care
    chmod u+x bin/care
else
	echo "Must be in virtualenv containing libarchive" >&2
	exit 1
fi
