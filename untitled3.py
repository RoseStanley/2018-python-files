import pandas as pd
import numpy as np
import itertools
from matplotlib import pyplot as plt
import seaborn as sns

pd.set_option('display.width', 3000000)
pd.set_option('display.max_columns', 50)

angles = ['minChi']#'minArccotF', 'minChi', 'minOmegaHat']
ratio = 0.5

for i in range (len(angles)):
    angle = angles[i]


    inpath = '~/Documents/file_nanoAOD/tbl_20180710_01_trg/nanoaod/QCD/sel_030/010_dataset_counts/tbl_n.dataset.htbin.metbin.{}.txt'.format(angle)        
    tbl1 = pd.read_table(inpath, delim_whitespace=True)    
    
    tbl1['err'] = np.sqrt(tbl1['nvar'])    
    tbl1['ratio'] = tbl1['err'] / tbl1['n']
    
    tbl1 = tbl1.dropna()
    
#    tbl2 = tbl1.dropna()
#    g = sns.FacetGrid(tbl2, col='metbin', row="htbin", margin_titles=True, legend_out = True, sharey=True)
#    g.map(plt.hist, 'ratio', bins=25)
#    g.add_legend()
#    plt.show()  
    
    tbl1 = tbl1[tbl1['dataset'] != 'QCD_HT100to200']
    tbl1 = tbl1[tbl1['nvar'] != tbl1['err']]
    
    tbl2 = tbl1.groupby(['htbin', 'metbin', angle]).sum().reset_index()
    tbl2['log10n'] = np.log10(tbl2['n'])


    g = sns.FacetGrid(tbl2, col='metbin', row="htbin", margin_titles=True, legend_out = True, sharey=True)
    g.map(plt.step, angle, 'log10n', where='post')
    g.add_legend()
    plt.show()
    
