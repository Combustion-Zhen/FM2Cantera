#!/bin/sh

# make input file for the FM2Cantera, list all the flamelet resutls of FlameMaster
echo OutMethane/CH4_p01_0chi > input;
echo tf0291to0294 >> input;
ls OutMethane/CH4_p01_0chi*tf0291to0294 | \
    sed -e 's@OutMethane/CH4_p01_0chi@@g' -e 's@tf0291to0294@@g' | \
    sort -g >> input;
