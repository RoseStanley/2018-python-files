import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

run = '2'
inpath = '~/Documents/file_simulations/tbl_20180706_0{}_trg/heppy/set_all/sel_010/020_counts/tbl_n.process.nVert.txt'.format(run)

tbl = pd.read_table(inpath, delim_whitespace=True)        
keys = ['process', 'nVert']
tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
tbl_mesh.columns = keys
tbl = pd.merge(tbl_mesh, tbl, how='left')
tbl.fillna(0, inplace=True)

tbl['nn'] = tbl.groupby('nVert')['n'].sum()

tbl = tbl[tbl.process == 'QCD']

g = sns.FacetGrid(tbl, hue="process", margin_titles=True, legend_out = True, sharey=True)
g.map(plt.step, 'nVert', 'nn', where='post')
g.add_legend()

plt.show()
#plt.savefig('20180706_0{}_cumnrate.htbin.{}.{}_0{}0.png'.format(run, me, angle, sel))


idx = tbl['nn'].idxmax()
peak = tbl.loc[idx, 'nVert']
print(peak)        