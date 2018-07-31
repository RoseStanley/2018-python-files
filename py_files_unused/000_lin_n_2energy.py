import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

inpath = '~/Documents/tbl_20180621_01_trg/heppy/set_EWK_QCD/sel_030/020_counts/tbl_n.process.htbin.mhtbin.min4Dphi.txt'
outpath = 'log_n.process.htbin.mhtbin.min4Dphi.png'

d = pd.read_table(inpath, delim_whitespace=True)

d['log10n'] = np.log10(d['n'])

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

g = sns.FacetGrid(d, col="mhtbin", row="htbin", hue='process', margin_titles=True, legend_out = False, sharey=False)
g.map(plt.step, 'min4Dphi', 'log10n')
g.add_legend()
plt.savefig(outpath)

