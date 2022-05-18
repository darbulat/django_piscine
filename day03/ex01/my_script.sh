#!/bin/bash

SMALL_PROGRAM="my_program.py"

python3 -m pip --version

python3 -m pip install --target local_lib --log log.log  git+https://github.com/jaraco/path.git &> /dev/null

# execute the small program
python3 $SMALL_PROGRAM
