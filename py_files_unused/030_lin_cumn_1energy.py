import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

inpath = '~/Documents/tbl_20180619_01_trg/heppy/set_EWK_QCD/sel_020/020_counts/tbl_n.process.htbin.minChi.txt'

outpath = 'lin_cumn.process.htbin.minChi.png'

d = pd.read_table(inpath, delim_whitespace=True)

keys = ['process', 'htbin', 'minChi']
d_mesh = pd.DataFrame(list(itertools.product(*[np.sort(d[c].unique()) for c in keys])))
d_mesh.columns = keys
d = pd.merge(d_mesh, d, how='left')
d.fillna(0, inplace=True)

d['cumn'] = d['n']
d['cumn'] = d[::-1].groupby(['process', 'htbin', 'minChi'])['cumn'].cumsum()[::-1]

d = d[d.htbin != 50]
d = d[d.htbin != 100]
d = d[d.htbin != 150]
d = d[d.htbin != 850]
d = d[d.htbin != 900]

g = sns.FacetGrid(d, col="htbin", hue='process', margin_titles=True, legend_out = False, sharey=False)
g.map(plt.step, 'minChi', 'cumn')
g.add_legend()
plt.savefig(outpath)

