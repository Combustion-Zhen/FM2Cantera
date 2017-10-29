"""
Zhen Lu 2017/07/20 <albert.lz07@gmail.com>
"""

import glob
import numpy as np
import matplotlib.pyplot as plt

SMALL  = 1.e-20
idx_I  = 2
models = ['IEM','MC','EMST']
Z_mean = [0.304,]
Z_var  = np.arange(0.2,1.0,0.2);

# plot
# use TeX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
plot_width    = 9.0 / 2.54
plot_height   = 9.0 / 2.54
margin_left   = 1.8 / 2.54
margin_right  = 0.3 / 2.54
margin_bottom = 1.2 / 2.54
margin_top    = 1.0 / 2.54
space_width   = 2.4 / 2.54
space_height  = 1.5 / 2.54
ftsize        = 12

str_legend = r'$\tilde{Z^{\prime\prime 2}}/($'+r'$\tilde{Z}(1-$'+r'$\tilde{Z}))=$'

for i, model in enumerate(models):

    fig = plt.figure(i,figsize=(plot_width,plot_height))
    ax  = fig.add_subplot(1,1,1)

    for mean in Z_mean:
        for var in Z_var:
            file_pre = 'samples_ave{0:.3f}_var{1:.3f}_chi'.format(mean,var)
            files = '{0}*.{1}'.format(file_pre,model)
            data = np.zeros((len(glob.glob(files)),2))
            for j, file_name in enumerate(glob.glob(files)):
                chist = float(file_name[len(file_pre):file_name.find('.{}'.format(model))])

                particles = np.genfromtxt(file_name)

                I = []
                for p in particles:
                    if abs(p[-1])>SMALL or abs(p[-2])>SMALL:
                        I.append(p[idx_I])
                I_ave = np.average(np.array(I))

                data[j,0] = chist
                data[j,1] = I_ave

            # sort the data
            data = data[np.argsort(data[:,0])]

            # plot for each mean and var
            label = str_legend+'{0:.2g}'.format(var)
            ax.plot(data[:,0],data[:,1],label=label,linewidth=1.5)

    ax.set_ylabel(r'$\langle\mathrm{FI}\rangle$',fontsize=ftsize)
    ax.set_ylim(0.0,1.0)
    ax.set_xlabel(r'$\chi_{st}\;\mathrm{(1/s)}$',fontsize=ftsize)
    ax.set_xscale('log')
    ax.set_title(model,fontsize=ftsize)
    ax.legend(fontsize=ftsize,frameon=False)

    fig.subplots_adjust(left   = margin_left   / plot_width,
                        bottom = margin_bottom / plot_height,
                        right  = 1.0 - margin_right / plot_width,
                        top    = 1.0 - margin_top   / plot_height,
                        wspace = space_width   / plot_width,
                        hspace = space_height  / plot_height)

    fig.savefig('chi_{0}.png'.format(model),dpi=400)
    fig.savefig('chi_{0}.eps'.format(model))
    fig.savefig('chi_{0}.pdf'.format(model))
