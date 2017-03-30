#!/bin/sh

# make input file for the FM2Cantera, list all the flamelet resutls of FlameMaster
echo $1 > input;
echo $2 >> input;
ls $1*$2 | \
    sed -e "s@$1@@g" -e "s@$2@@g" | \
    sort -g >> input;
