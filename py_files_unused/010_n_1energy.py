#Cumulative count graph htbin angle change

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

inpath = '~/Documents/tbl_20180619_01_trg/heppy/set_EWK_QCD/sel_020/020_counts/tbl_n.process.htbin.min4Dphi.txt'

outpath = 'n.process.htbin.min4Dphi.png'

d = pd.read_table(inpath, delim_whitespace=True)


d = d[d.htbin != 50]
d = d[d.htbin != 100]
d = d[d.htbin != 150]
d = d[d.htbin != 850]
d = d[d.htbin != 900]

d['log10n'] = np.log10(d['n'])

g = sns.FacetGrid(d, col="htbin", hue='process', margin_titles=True, legend_out = False, sharey=False)
g.map(plt.step, 'min4Dphi', 'log10n')
g.add_legend()
plt.savefig(outpath)

