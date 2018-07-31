import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

month = '07'
date = '19'
sel = '3'
folder = 'set_all' 
angles = ['minArccotF', 'minChi', 'minOmegaHat']
anglevals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]#, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

for i in range (len(angles)):
    angle = angles[i]
    inpath = '~/Documents/file_simulations/tbl_2018{}{}_01_trg/heppy/{}/sel_0{}0/020_counts/tbl_n.process.htbin.metbin.mhtbin.{}.txt'.format(month, date, folder, sel, angle)
    
    tbl = pd.read_table(inpath, delim_whitespace=True)
    keys = ['process', 'htbin', 'metbin', 'mhtbin', angle]
    tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
    tbl_mesh.columns = keys
    tbl = pd.merge(tbl_mesh, tbl, how='left')
    tbl.fillna(0, inplace=True)
       
    tbl['mhtovermet'] =  tbl['metbin'] / tbl['mhtbin']
    tbl['mhtovermet'] = tbl['mhtovermet'].round(2)
   
    tbl_1 = tbl
    tbl_1['cumn'] = tbl_1['n']
    tbl_1['cumn'] = tbl_1[::-1].groupby(['process', 'htbin', 'metbin', 'mhtbin' ])['cumn'].cumsum()[::-1]
    tbl_1['cumn'] = tbl_1[::-1].groupby(['process', 'htbin', 'metbin', angle ])['cumn'].cumsum()[::-1]   
    tbl_1['cumn'] = tbl_1[::-1].groupby(['process', 'htbin', 'mhtbin', angle ])['cumn'].cumsum()[::-1]
    tbl_1['cumn'] = tbl_1[::-1].groupby(['process', 'metbin', 'mhtbin', angle ])['cumn'].cumsum()[::-1]
    tbl_1['cumn'] = tbl_1[::-1].groupby(['htbin', 'metbin', 'mhtbin', angle ])['cumn'].cumsum()[::-1]
#       
    tbl_1['nn'] = tbl_1['n']
    tbl_1['nn'] = tbl_1[::-1].groupby(['htbin', 'metbin', 'mhtbin', angle])['nn'].cumsum()[::-1]

    tbl_1['log10cumn'] = np.log10(tbl_1['cumn'])
    tbl_1['log10n'] = np.log10(tbl_1['nn'])
    
    tbl_1 = tbl_1[tbl_1.process == 'QCD']
    
    
    fig1, axes = plt.subplots(nrows=2, ncols=5, sharey=True, sharex=True, figsize=(24,8))   
    
    n = 0
    
    for ax in axes.flat:
        angleval = anglevals[n]
        tbl_2 = tbl_1
        tbl_2 = tbl_2[tbl_2[angle] == angleval]
        tbl_2 = tbl_2.pivot_table('log10cumn', ['mhtovermet'], 'metbin', aggfunc='sum')   
        g = sns.heatmap(tbl_2, cbar=False, ax=ax)
        g.invert_yaxis()
        
        if n <= 4:
            g.set_xlabel('')
            if n != 0:
                g.set_ylabel('')
        elif n > 4:
            if n != 5:
                g.set_ylabel('')
                
        n+= 1     
    
    cbar = fig1.colorbar(g, ax=axes.ravel().tolist())
    plt.show()
    
    
    
    
    
    
    
