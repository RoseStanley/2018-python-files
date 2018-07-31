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


    inpath = '~/Documents/file_nanoAOD/tbl_20180710_01_trg/nanoaod/set_EWK_QCD/sel_030/020_counts/tbl_n.process.htbin.metbin.{}.txt'.format(angle)        
    tbl1 = pd.read_table(inpath, delim_whitespace=True)    
    
    tbl1['err'] = np.sqrt(tbl1['nvar'])    
    tbl1['ratio'] = tbl1['err'] / tbl1['n']
    
    #tbl2 = tbl1.dropna()
    #g = sns.FacetGrid(tbl2, col='metbin', row="htbin", margin_titles=True, legend_out = True, sharey=True)
    #g.map(plt.hist, 'ratio', bins=25)
    #g.add_legend()
    #plt.show()
    
    tbl1 = tbl1[tbl1['ratio'] < ratio] 
    
    keys = ['process', 'htbin', 'metbin', angle]
    tbl1_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl1[c].unique()) for c in keys])))
    tbl1_mesh.columns = keys
    tbl1 = pd.merge(tbl1_mesh, tbl1, how='left')
    tbl1.fillna(0, inplace=True)       
            
    tbl1['cumn'] = tbl1['n']
    tbl1['cumn'] = tbl1[::-1].groupby(['process', 'htbin', 'metbin'])['cumn'].cumsum()[::-1]
    tbl1['cumn'] = tbl1[::-1].groupby(['process', 'htbin', angle])['cumn'].cumsum()[::-1]
    tbl1['cumn'] = tbl1[::-1].groupby(['process', 'metbin', angle])['cumn'].cumsum()[::-1]
    #tbl1['cumn'] = tbl1[::-1].groupby(['htbin', 'metbin', angle])['cumn'].cumsum()[::-1]
    
    tbl1['nn'] = tbl1['n']
    #tbl1['nn'] = tbl1[::-1].groupby(['htbin', 'metbin', angle])['nn'].cumsum()[::-1]
    
    tbl1['log10cumn'] = np.log10(tbl1['cumn'])
    tbl1['log10n'] = np.log10(tbl1['nn'])
    
#    tbl1 = tbl1[ tbl1['metbin'] > 100]
    
    g = sns.FacetGrid(tbl1, col='metbin', row="htbin", hue='process', margin_titles=True, legend_out = True, sharey=True)
    g.map(plt.step, angle, 'log10cumn', where='post')
    g.add_legend()
    plt.show()
#    plt.savefig('20180710_cumn_{}_ratio{}.png'.format(angle, ratio))
    
    g = sns.FacetGrid(tbl1, col='metbin', row="htbin", hue='process', margin_titles=True, legend_out = True, sharey=True)
    g.map(plt.step, angle, 'log10n', where='post')
    g.add_legend()
    plt.show()
#    plt.savefig('20180710_n_{}_ratio{}.png'.format(angle, ratio))
    
    
            