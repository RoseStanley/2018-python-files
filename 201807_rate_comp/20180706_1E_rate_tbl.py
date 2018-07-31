import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

run = '3'
sel = '3'
mes = ['metbin', 'mhtbin', 'htbin'] 
angles = ['minArccotF', 'minChi', 'minOmegaHat']
for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath = '~/Documents/file_simulations/tbl_20180706_0{}_trg/heppy/set_all/sel_0{}0/020_counts/tbl_n.process.{}.{}.txt'.format(run, sel, me, angle)
    
        tbl = pd.read_table(inpath, delim_whitespace=True)
        keys = ['process', me, angle]
        tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
        tbl_mesh.columns = keys
        tbl = pd.merge(tbl_mesh,tbl, how='left')
        tbl.fillna(0, inplace=True)
 
    
        """Background Stacked"""
        dbg = tbl
       
        dbg['cumn'] = dbg['n']
        dbg['cumn'] = dbg[::-1].groupby(['process', me])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['process', angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby([me, angle])['cumn'].cumsum()[::-1]
        
        """RateTables"""    
        
        df = dbg
        df = df[df.process == 'QCD']
        df2 = df.pivot_table('cumn', [angle], me)
        df2.to_csv(r'20180706_0{}_rate.{}.{}_0{}0.csv'.format(run, me, angle, sel), sep='\t', mode='w') #, float_format='%6f')
    
#  
