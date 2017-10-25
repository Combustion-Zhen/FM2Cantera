"""
Zhen Lu 2017/10/25
A python script to transfer FlameMaster output to csv tables
"""

import numpy as np
import os
import sys
import glob

fuel_name = 'CH4'

fm_dir = 'Out{}'.format(fuel_name)
ct_dir = 'tables_{}'.format(fuel_name)

if not os.path.exists(fm_dir):
    sys.exit('FlameMaster output not found')

os.makedirs(cantera_name,exist_ok=True)

for flame in glob.glob('{}/{}_p*'.format(fm_dir,fuel_name)):
    print(flame)
