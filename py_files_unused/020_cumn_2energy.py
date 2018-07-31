import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

inpath = '~/Documents/tbl_20180621_01_trg/heppy/set_EWK_QCD/sel_030/020_counts/tbl_n.process.htbin.mhtbin.minArccotF.txt'

outpath = 'slogx_cumn.process.htbin.mhtbin.minArccotF.png'

d = pd.read_table(inpath, delim_whitespace=True)

keys = ['process', 'htbin', 'mhtbin', 'minArccotF']
d_mesh = pd.DataFrame(list(itertools.product(*[np.sort(d[c].unique()) for c in keys])))
d_mesh.columns = keys
d = pd.merge(d_mesh, d, how='left')
d.fillna(0, inplace=True)

d['cumn'] = d['n']
d['cumn'] = d[::-1].groupby(['process', 'htbin', 'mhtbin'])['cumn'].cumsum()[::-1]
d['cumn'] = d[::-1].groupby(['process', 'htbin', 'minArccotF'])['cumn'].cumsum()[::-1]
d['cumn'] = d[::-1].groupby(['process', 'mhtbin', 'minArccotF'])['cumn'].cumsum()[::-1]
d['cumn'] = d[::-1].groupby(['htbin', 'mhtbin', 'minArccotF'])['cumn'].cumsum()[::-1]

d['log10cumn'] = np.log10(d['cumn'])

d = d[d.mhtbin != 0]

d = d[d.mhtbin != 260]
d = d[d.mhtbin != 270]
d = d[d.mhtbin != 280]
d = d[d.mhtbin != 290]
d = d[d.mhtbin != 300]

d = d[d.htbin != 50]
d = d[d.htbin != 100]
d = d[d.htbin != 150]

d = d[d.htbin != 850]
d = d[d.htbin != 900]

g = sns.FacetGrid(d, col="minArccotF", row="htbin", hue="process", margin_titles=True, legend_out = False, sharey=True)
g.map(plt.step, 'mhtbin', 'log10cumn')
g.add_legend()
plt.show()
#plt.savefig(outpath)

