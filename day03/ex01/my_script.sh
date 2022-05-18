#!/bin/bash

SMALL_PROGRAM="my_program.py"

python3 -m pip --version

python3 -m pip install --target local_lib --log log.log --upgrade --force-reinstall git+https://github.com/jaraco/path.git &> /dev/null && python3 $SMALL_PROGRAM || echo "NOK"

