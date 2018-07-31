import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')


inpath = '~/Documents/tbl_20180619_01_trg/heppy/set_EWK_QCD/sel_020/020_counts/tbl_n.process.htbin.metbin.txt'

outpath = 'n.process.htbin.metbin.png'

d = pd.read_table(inpath, delim_whitespace=True)

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

d['log10n'] = np.log10(d['n'])

g = sns.FacetGrid(d, col='htbin', hue='process', margin_titles=True, legend_out = True, sharey=False)
g.map(plt.step, 'metbin', 'log10n')
g.add_legend()
plt.savefig(outpath)

