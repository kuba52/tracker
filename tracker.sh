#!/bin/bash
g++ -std=c++20 main.cc -o p
if [ $# -le 0 ]
then
    echo "usage $0 [distance to plane]"
else
    echo $#
    python3 detect.py
    ./p 1280 720 $1
    python3 IO_wykresy.py
fi