import pandas as pd
import numpy as np
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

inpath = '~/Documents/tbl_20180619_01_trg/heppy/set_EWK_QCD/sel_030/020_counts/tbl_n.process.htbin.mhtbin.min4Dphi.txt'

outpath = 'red_angle.process.mhtbin.min4Dphi.png'

d = pd.read_table(inpath, delim_whitespace=True)

keys = ['process', 'htbin', 'min4Dphi', 'mhtbin']
d_mesh = pd.DataFrame(list(itertools.product(*[np.sort(d[c].unique()) for c in keys])))
d_mesh.columns = keys
d = pd.merge(d_mesh, d, how='left')
d.fillna(0, inplace=True)
df = pd.DataFrame()
df = d[d.index % 4 == 0] 
df['n'] = d['n'].groupby(d['n'].index // 4 * 4).sum()

d = d[d.mhtbin != 0]
d = d[d.mhtbin != 10]
d = d[d.mhtbin != 20]
d = d[d.mhtbin != 30]
d = d[d.mhtbin != 40]
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

with np.errstate(divide='ignore'):
    df['log10n'] = np.log10(df['n'])

g = sns.FacetGrid(df, row="htbin", col="min4Dphi", hue='process', margin_titles=True, legend_out = False, sharey=False)
g.map(plt.step, 'mhtbin', 'log10n')
g.add_legend()
plt.savefig(outpath)



