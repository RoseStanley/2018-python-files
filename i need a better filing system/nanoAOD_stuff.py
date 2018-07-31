import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

month = '07'
date = '10'
sel = '3'
folder = 'MET' #'MET' for MET replace dataset with dataset and 020_counts with 010_dataset_counts
mes = ['metbin']#, 'mhtbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
#htvals = [0, 400, 600, 800, 1000 ]

for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath = '~/Documents/file_nanoAOD/tbl_2018{}{}_01_trg/nanoaod/{}/sel_0{}0/010_dataset_counts/tbl_n.dataset.htbin.{}.{}.txt'.format(month, date, folder, sel, me, angle)
        
        tbl = pd.read_table(inpath, delim_whitespace=True)
        keys = ['dataset', 'htbin', me, angle]
        tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
        tbl_mesh.columns = keys
        tbl = pd.merge(tbl_mesh, tbl, how='left')
        tbl.fillna(0, inplace=True)
        
        tbl['n'] = tbl['n'] / 3600000         
        
        dbg = tbl
        dbg['cumn'] = dbg['n']
        dbg['cumn'] = dbg[::-1].groupby(['dataset', 'htbin', me])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['dataset', 'htbin', angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['dataset', me, angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['htbin', me, angle])['cumn'].cumsum()[::-1]
        
        dbg['nn'] = dbg['n']
        dbg['nn'] = dbg[::-1].groupby(['htbin', me, angle])['nn'].cumsum()[::-1]

        dbg['log10cumn'] = np.log10(dbg['cumn'])
        dbg['log10n'] = np.log10(dbg['nn'])
        
        dbg = dbg[dbg[me] != 0]
        dbg = dbg[dbg[me] != 100]
    
        
        g = sns.FacetGrid(dbg, col=me, row="htbin", hue="dataset", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10cumn', where='post')
        g.add_legend()
        plt.savefig('MET2018{}{}_cumn_rate.htbin.{}.{}_0{}0.png'.format(month, date, me, angle, sel))
        
        g = sns.FacetGrid(dbg, col=me, row="htbin", hue="dataset", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10n', where='post')
        g.add_legend()
        plt.savefig('MET2018{}{}_n.htbin.{}.{}_0{}0.png'.format(month, date, me, angle, sel))
    
