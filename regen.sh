#!/bin/bash

set -eux

for d in data/*.json; do 
    destfile=results/$(basename ${d%.json}).txt; 
    ./championship_plus_minus.py -f $d > $destfile
done
