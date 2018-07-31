import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')



inpath = '~/Documents/file_simulations/tbl_20180627_01_trg/heppy/set_all/sel_030/020_counts/tbl_n.process.htbin.metbin.minArccotF.txt'
tbl = pd.read_table(inpath, delim_whitespace=True)

keys = ['process', 'htbin', 'metbin', 'minArccotF']
tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
tbl_mesh.columns = keys
tbl = pd.merge(tbl_mesh, tbl, how='left')
tbl.fillna(0, inplace=True)

dbg = tbl
dbg['cumn'] = dbg['n']
dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', 'metbin'])['cumn'].cumsum()[::-1]
dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', 'minArccotF'])['cumn'].cumsum()[::-1]
dbg['cumn'] = dbg[::-1].groupby(['process', 'metbin', 'minArccotF'])['cumn'].cumsum()[::-1]
dbg['cumn'] = dbg[::-1].groupby(['htbin', 'metbin', 'minArccotF'])['cumn'].cumsum()[::-1]
        
dbg['log10cumn'] = np.log10(dbg['cumn'])

dbg = dbg.groupby(['htbin', 'metbin']).sum()
print(dbg)

#dbg = dbg.pivot('htbin', 'metbin', 'log10cumn')
#
#g = sns.FacetGrid(dbg, col='minArccotF', hue="process", margin_titles=True, legend_out = True, sharey=True)
#g.map(sns.heatmap)
#        g.add_legend()
#        plt.savefig('{}{}_cumn_rate.htbin.{}.{}.png'.format(month, date, 'metbin', 'minArccotF'))











