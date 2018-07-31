import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

pd.set_option('display.width', None)
matplotlib.style.use('ggplot')


inpath = '~/Documents/tbl_20180619_01_trg/heppy/set_EWK_QCD/sel_020/020_counts/tbl_n.process.htbin.txt'

outpath = 'n.process.htbin.png'

d = pd.read_table(inpath, delim_whitespace=True)

sumall = d.groupby('htbin')
df = pd.DataFrame(sumall.size().reset_index())
df['n'] = d.groupby(['htbin'])['n'].transform('sum')

d = d[d.htbin != 50]
d = d[d.htbin != 100]
d = d[d.htbin != 150]
d = d[d.htbin != 850]
d = d[d.htbin != 900]

df['log10n'] = np.log10(df['n'])

g = sns.FacetGrid(df, margin_titles=True, legend_out = False, sharey=False)
g.map(plt.step, 'htbin', 'log10n')
plt.savefig(outpath)

