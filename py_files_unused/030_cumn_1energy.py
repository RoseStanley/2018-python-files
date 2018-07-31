import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

inpath = '~/Documents/tbl_20180621_01_trg/heppy/set_EWK_QCD/sel_020/020_counts/tbl_n.process.htbin.mhtbin.minOmegaHat.txt'

outpath = 'cumn.process.htbin.mhtbin.minOmegaHat.png'

d = pd.read_table(inpath, delim_whitespace=True)

keys = ['process', 'htbin', 'minOmegaHat', 'mhtbin']
d_mesh = pd.DataFrame(list(itertools.product(*[np.sort(d[c].unique()) for c in keys])))
d_mesh.columns = keys
d = pd.merge(d_mesh, d, how='left')
d.fillna(0, inplace=True)

d['cumn'] = d['n']
d['cumn'] = d[::-1].groupby(['process', 'htbin', 'minOmegaHat'])['cumn'].cumsum()[::-1]
d['cumn'] = d[::-1].groupby(['process', 'htbin', 'mhtbin'])['cumn'].cumsum()[::-1]
d['cumn'] = d[::-1].groupby(['process', 'mhtbin', 'minOmegaHat'])['cumn'].cumsum()[::-1]


d['log10cumn'] = np.log10(d['cumn'])

print(d)
#
#g = sns.FacetGrid(d, row='mhtbin', col="htbin", hue='process', margin_titles=True, legend_out = False,sharey=False)
#g.map(plt.step, 'minOmegaHat', 'log10cumn')
#g.add_legend()
#plt.savefig(outpath)

