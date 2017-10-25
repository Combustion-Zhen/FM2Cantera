"""
Zhen Lu 2017/10/25
A python script to transfer FlameMaster output to csv tables
"""

import numpy as np
import os
import sys
import glob
import csv

column_num = 5

fm_dir = 'OutSteady'
ct_dir = 'tables'

if not os.path.exists(fm_dir):
    sys.exit('FlameMaster output not found')

os.makedirs(ct_dir,exist_ok=True)

# read the species names into dictionary
# key: species names in FlameMaster
# value: species names in Chemkin mechanism
spe_name_dict = {}
with open('speciestranslated','r') as f:
    for line in f:
        spe_names = line.split()
        spe_name_dict[spe_names[1]] = spe_names[0] 

chi_list = []

for flame in glob.glob('{}/CH4_p01*'.format(fm_dir)):

    # skip not converged solution
    if flame[-3:] == 'noC':
        continue

    data = {}
    chi_st = float(flame[flame.find('chi')+3:flame.find('tf')])
    chi_list.append(chi_st)
    table_name = 'Table_{:g}.csv'.format(chi_st)

    with open(flame,'r') as f:

        # read the header part
        for line in f:
            if line.strip() == '':
                continue
            elif line[:-1] == 'body':
                break
            elif line.split()[0] == 'gridPoints':
                pts = int(line.split()[-1])
                row_num = np.ceil(pts/column_num)

        for line in f:
            if line.strip() == '':
                continue
            elif line[:-1] == 'trailer':
                break
            var_name = line.split()[0]
            # map names
            if var_name == 'temperature':
                var_name = 'T'
            elif var_name[:12] == 'massfraction':
                var_name = spe_name_dict[var_name[13:]]
            # read data
            var = []
            for i in np.arange(row_num):
                data_line = f.readline().split()
                var.extend([float(x) for x in data_line])
            data[var_name] = np.array(var)

    # write to csv file
    with open('{0}/{1}'.format(ct_dir,table_name),'w') as f:
        writer = csv.DictWriter(f,fieldnames=data.keys())
        writer.writeheader()
        for i in range(pts):
            data_row = {}
            for k, v in data.items():
                data_row[k] = v[i]
            writer.writerow(data_row)

    # write a Z list
    if chi_st == 10:
        with open('{}/Z_param.include'.format(ct_dir),'w') as f:
            f.write('Z_param\n{:g}\n(\n'.format(len(data['Z'])))
            f.write('\n'.join(format(x, '12.6e') for x in data['Z']))
            f.write('\n);')

chi_list = sorted(chi_list)
with open('{}/chi_param.include'.format(ct_dir),'w') as f:
    f.write('chi_param\n{:g}\n(\n'.format(len(chi_list)))
    f.write('\n'.join(format(x, '12.6e') for x in chi_list))
    f.write('\n);')

