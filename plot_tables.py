# Zhen Lu, 2017 <albert.lz07@gmail.com>
# plot flamelet tables
# load csv tables to be used for flameletFoam integration
import csv
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

# load the chi_param.include file to get information on table files
f=open('tables/chi_param.include','r')
f.readline()
table_num=int(f.readline())
f.readline()
# read chi, load file, suppot 12 maximun digits
full_tables={}
for i in range(table_num):
    chi = float(f.readline())
    filename = 'tables/Table_{0:.12g}.csv'.format(chi)
    print('Reading table: {0}'.format(filename))
    with open(filename, 'rb') as tablefile:
        tablereader = csv.reader(tablefile,delimiter=',')
        table_data = {}
        var_names = next(tablereader)
        for var in var_names:
            table_data.update({var:[]})
        for row in tablereader:
            for i in range(len(row)):
                table_data[var_names[i]].append(row[i])
    full_tables.update({chi:table_data})
# print(full_tables.keys())

# plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
plot_width      =9.0
plot_height     =9.0
margin_left     =2.0
margin_right    =0.3
margin_bottom   =1.5
margin_top      =0.3
ftsize          =12
# min and max of axis
xmin = 0.0
xmax = 1.0
ymin = 300.0
ymax = 2300.0

# generate the figure
plt.figure(1,figsize=cm2inch(plot_width, plot_height))
# generate the axis
plt.subplot(111)
# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height)

#table_name=full_tables.keys()[0]
#plt.plot(full_tables[table_name]['Z'],full_tables[table_name]['T'])
for chi_st in full_tables.keys():
    plt.plot(full_tables[chi_st]['Z'],full_tables[chi_st]['T'])

# labels
plt.xlabel("$f$",fontsize=ftsize)
plt.ylabel("$T\;(\mathrm{K})$",fontsize=ftsize)

# axis limits, ticks, and labels
plt.axis([xmin, xmax, ymin, ymax])
plt.xticks((0.0,0.2,0.4,0.6,0.8,1.0))
plt.yticks(range(300,2301,500))
plt.savefig('tmp.eps')
