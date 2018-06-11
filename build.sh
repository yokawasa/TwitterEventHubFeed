#!/bin/sh

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
#python ${cwd}/setup.py sdist
python ${cwd}/setup.py sdist bdist_wheel
# sudo python ${cwd}/setup.py install
