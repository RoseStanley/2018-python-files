import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

inpath = '~/Documents/tbl_20180619_01_trg/heppy/set_EWK_QCD/sel_020/020_counts/tbl_n.process.htbin.metbin.minChi.txt'

outpath = 'lin_cumn.process.htbin.metbin.minChi.png'

d = pd.read_table(inpath, delim_whitespace=True)

keys = ['process', 'htbin', 'minChi']
d_mesh = pd.DataFrame(list(itertools.product(*[np.sort(d[c].unique()) for c in keys])))
d_mesh.columns = keys
d = pd.merge(d_mesh, d, how='left')
d.fillna(0, inplace=True)

d['cumn'] = d['n']
d['cumn'] = d[::-1].groupby(['process', 'htbin', 'metbin'])['cumn'].cumsum()[::-1]
d['cumn'] = d[::-1].groupby(['process', 'htbin', 'minChi'])['cumn'].cumsum()[::-1]
d['cumn'] = d[::-1].groupby(['process', 'metbin', 'minChi'])['cumn'].cumsum()[::-1]

d = d[d.metbin != 0]
d = d[d.metbin != 10]
d = d[d.metbin != 20]
d = d[d.metbin != 30]
d = d[d.metbin != 40]
d = d[d.metbin != 260]
d = d[d.metbin != 270]
d = d[d.metbin != 280]
d = d[d.metbin != 290]
d = d[d.metbin != 300]
d = d[d.htbin != 50]
d = d[d.htbin != 100]
d = d[d.htbin != 150]
d = d[d.htbin != 850]
d = d[d.htbin != 900]

g = sns.FacetGrid(d, col="metbin", row="htbin", hue="process", margin_titles=True, legend_out = False, sharey=False)
g.map(plt.step, 'minChi', 'cumn')
g.add_legend()
plt.savefig(outpath)

