#!/bin/bash

STAT=$1
OPT=""

if [ $# -eq 3 ]
then
    echo "also arguments"
    OPT=$2
fi
set -x
CMD="python -m timeit -c \"$STAT\""
echo $CMD
$CMD