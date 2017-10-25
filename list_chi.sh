#!/bin/sh

# make input file for the FM2Cantera, list all the flamelet resutls of FlameMaster
# example: ./list_chi.sh OutMethane/CH4_p01_0chi tf0298to0298
echo $1 > input;
echo $2 >> input;
ls $1*$2 | \
    sed -e "s@$1@@g" -e "s@$2@@g" | \
    sort -g >> input;
