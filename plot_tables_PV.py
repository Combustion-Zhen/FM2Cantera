"""
Zhen Lu 2017/07/19 <albert.lz07@gmail.com>

plot flamelet solutions, progress variable C against mixture fraction Z
"""

import numpy as np
import matplotlib.pyplot as plt
import glob

SMALL = 1.e-20

folder_name = 'tables_H2/'
table_pre   = 'Table_'
file_end    = '.csv'

# figure and axes parameters
plot_width      =18.0 / 2.54
plot_height     =18.0 / 2.54
margin_left     =2.0 / 2.54
margin_right    =0.3 / 2.54
margin_bottom   =1.5 / 2.54
margin_top      =0.3 / 2.54
space_width     =0.0 / 2.54
space_height    =0.0 / 2.54
ftsize          =12

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# generate the figure
fig, axes = plt.subplots(1,1,figsize=(plot_width, plot_height))

for table in glob.glob('{0}{1}*{2}'.format(folder_name,table_pre,file_end)): 
    data = np.genfromtxt(table,delimiter=',',names=True)
    chist = table[len(folder_name)+len(table_pre):table.find(file_end)]
    label = r'$\chi_{st}=$'+chist

    # calculate the equivalence ratio
    phi = (data['H']+data['OH']/17.+2.*data['H2']/2.+2.*data['H2O']/18.
            +data['HO2']/33.+2.*data['H2O2']/34.) \
         / (2.*data['O2']/32.+data['OH']/17.+data['O']/16.+data['H2O']/18.
            +2.*data['HO2']/33.+2.*data['H2O2']/34.) *0.5

    PV = np.zeros(len(phi))

    for i, p in enumerate(phi):
        if phi[i] < 1.0:
            PV[i] = data['H2O'][i]/18./(data['H2O'][i]/18.+data['H2'][i]/2.)
        else:
            PV[i] = data['H2O'][i]/18./(data['H2O'][i]/18.+data['O2'][i]/16.)

    #plt.plot(phi/(phi+1),PV,label=label,linewidth=1.5)
    plt.plot(data['Z'],PV,label=label,linewidth=1.5)

axes.set_xlabel(r'$Z$',fontsize=ftsize)
axes.set_xlim(0.0,1.0)

# too many lines
#axes.legend(fontsize=ftsize,frameon=False)

plt.subplots_adjust(left   = margin_left   / plot_width,
                    bottom = margin_bottom / plot_height,
                    right  = 1.0 - margin_right / plot_width,
                    top    = 1.0 - margin_top   / plot_height,
                    wspace = space_width   / plot_width,
                    hspace = space_height  / plot_height)

plt.show()
