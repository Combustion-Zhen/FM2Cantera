"""
Zhen Lu 2017/07/20 <albert.lz07@gmail.com>

Do mixing for the samled flamelet solution
cycle in three mixing models
"""

import glob
import numpy as np
from subprocess import call

models = ['IEM','MC','EMST']

Z_mean = [0.304,]
Z_var  = np.arange(0.1,1.0,0.1);
N_p    = 100

for mean in Z_mean:
    for var in Z_var:
        file_pre = 'samples_ave{0:.3f}_var{1:.3f}_chi'.format(mean,var)
        for file_name in glob.glob('{0}*.dat'.format(file_pre)):
            chist = float(file_name[len(file_pre):-4])

            # edit input
            with open('input','w') as f:
                f.write('{0}\n'.format(file_name))
                f.write('{0:12.5f}{1:12.5f}{2:12.5f}\n'
                        .format(mean,var,chist))

            for i, model in enumerate( models ):
                # edit the pasr.nml
                with open('pasr.nml','r') as f:
                    nml = f.read()
                nml_n = '{0}{1}{2}'.format(nml[:nml.find('mxmode')+7],
                                           i+1,
                                           nml[nml.find('mxmode')+8:])
                with open('pasr.nml','w') as f:
                    f.write(nml_n)

                # run the mixing
                call(["Mixing"])
