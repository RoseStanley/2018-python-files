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
anglevals = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]#, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

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
    
    
    for j in range (len(anglevals)):
        angleval = anglevals[j]
        
        tbl_2 = tbl_1
        tbl_2 = tbl_2[tbl_2[angle] == angleval]
        tbl_2 = tbl_2[tbl_2.process == 'QCD']        
        tbl_2 = tbl_2.pivot_table('log10cumn', ['mhtbin'], 'metbin', aggfunc='sum')   
        
        tbl_3 = tbl_1
        tbl_3 = tbl_3[tbl_3[angle] == angleval]
        tbl_3 = tbl_3[tbl_3.process == 'QCD'] 
        tbl_3 = tbl_3.pivot_table('log10cumn', ['mhtovermet'], 'metbin', aggfunc='sum')
#        tbl_3 = tbl_3.fillna(value=0)
    
        pl_2 = sns.heatmap(tbl_2)
        pl_2.invert_yaxis()
        plt.savefig('2018{}{}_MHTMET_{}{}_sel_0{}0.png'.format(month, date, angle, angleval, sel))
        plt.show()
        
        pl_3 = sns.heatmap(tbl_3)
        pl_3.invert_yaxis()
        plt.savefig('2018{}{}_MHTOVERMET_{}{}_sel_0{}0.png'.format(month, date, angle, angleval, sel))
        plt.show()
 