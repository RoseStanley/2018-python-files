import pandas as pd
import numpy as np
import itertools
pd.set_option('display.width', None)
pd.set_option('display.max_columns', 50)

spike = 1.2          

run1 = '01'
sel1 = '020'

run2 = '01'
sel2 = '030'

Emiss = ['mhtbin', 'metbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
htvals = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
metvals = [0, 70, 80, 90, 100, 110, 120, 130, 140, 150]

df = pd.DataFrame(columns = ['run', 'sel', 'htbin', 'Emiss', 'EmissVal', 'Angle', 'AngleVal', 'Difference'])


for i in range (len(angles)):
    angle = angles[i]
    for j in range (len(Emiss)):
        Emis = Emiss[j]
        
        inpath1 = '~/Documents/file_simulations/tbl_20180706_{}_trg/heppy/set_all/sel_{}/020_counts/tbl_n.process.htbin.{}.{}.txt'.format(run1, sel1, Emis, angle)
        inpath2 = '~/Documents/file_simulations/tbl_20180706_{}_trg/heppy/set_all/sel_{}/020_counts/tbl_n.process.htbin.{}.{}.txt'.format(run2, sel2, Emis, angle)
        
        tbl1 = pd.read_table(inpath1, delim_whitespace=True) 
        tbl2 = pd.read_table(inpath2, delim_whitespace=True)
                  
        keys = ['process', 'htbin', Emis, angle]
        tbl1_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl1[c].unique()) for c in keys])))
        tbl1_mesh.columns = keys
        tbl1 = pd.merge(tbl1_mesh, tbl1, how='left')
        tbl1.fillna(0, inplace=True)                
        
        tbl1['nn'] = tbl1['n']
        tbl1['nn'] = tbl1[::-1].groupby(['htbin', Emis, angle])['nn'].cumsum()[::-1]
        
        tbl1 = tbl1[tbl1.process == 'QCD']

        tbl2_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl2[c].unique()) for c in keys])))
        tbl2_mesh.columns = keys
        tbl2 = pd.merge(tbl2_mesh, tbl2, how='left')
        tbl2.fillna(0, inplace=True)                
        
        tbl2['nn'] = tbl2['n']
        tbl2['nn'] = tbl2[::-1].groupby(['htbin', Emis, angle])['nn'].cumsum()[::-1]
        
        tbl2 = tbl2[tbl2.process == 'QCD']
        
        for k in range (len(htvals)):
            htval = htvals[k]
            for l in range(len(metvals)):
                metval = metvals[l]
                
                tbl_1 = tbl1
                tbl_1 = tbl_1[tbl_1.htbin == htval]
                tbl_1 = tbl_1[tbl_1[Emis] == metval]
                tbl_1 = tbl_1.reset_index(drop=True)                

                tbl_2 = tbl2
                tbl_2 = tbl_2[tbl_2.htbin == htval]
                tbl_2 = tbl_2[tbl_2[Emis] == metval]
                tbl_2 = tbl_2.reset_index(drop=True)
            
                for m in range (len(tbl_1.index)-2):
                    m1 = m+1
                    m2 = m+2
                    
                    


