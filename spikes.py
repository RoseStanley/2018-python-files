import pandas as pd
import numpy as np
import itertools
pd.set_option('display.width', None)
pd.set_option('display.max_columns', 50)

spike = 0.9


Emiss = ['mhtbin', 'metbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
runs = ['02']#, '02', '03']
sels = ['020']#, '030']
htvals = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
metvals = [50, 70, 80, 90, 100, 110, 120, 130, 140, 150]

df1 = pd.DataFrame(columns = ['run', 'sel', 'htbin', 'Emiss', 'EmissVal', 'Angle', 'AngleVal', 'Difference'])

for i in range (len(runs)):
    run = runs[i]  
    for j in range (len(sels)):
        sel = sels[j]
        for k in range (len(Emiss)):
            Emis = Emiss[k]        
            for l in range (len(angles)):
                angle = angles[l]
                
                inpath = '~/Documents/file_simulations/tbl_20180706_{}_trg/heppy/set_EWK_QCD/sel_{}/020_counts/tbl_n.process.htbin.{}.{}.txt'.format(run, sel, Emis, angle)
                tbl = pd.read_table(inpath, delim_whitespace=True) 
                
                keys = ['process', 'htbin', Emis, angle]
                tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
                tbl_mesh.columns = keys
                tbl = pd.merge(tbl_mesh, tbl, how='left')
                tbl.fillna(0, inplace=True)                
                
                tbl['nn'] = tbl['n']
                tbl['nn'] = tbl[::-1].groupby(['htbin', Emis, angle])['nn'].cumsum()[::-1]
                
                tbl = tbl[tbl.process == 'QCD']
                
                for m in range (len(htvals)):
                    htval = htvals[m]
                    for n in range(len(metvals)):
                        metval = metvals[n]
                        
                        tbl_1 = tbl
                        tbl_1 = tbl_1[tbl_1.htbin == htval]
                        tbl_1 = tbl_1[tbl_1[Emis] == metval]
                        tbl_1 = tbl_1.reset_index(drop=True)
                    
                        for o in range (len(tbl_1.index)-2):
                            
                            o1 = o + 1
                            o2 = o + 2
                            O = tbl_1.loc[o, 'nn']
                            O1 = tbl_1.loc[o1, 'nn']
                            O2 = tbl_1.loc[o2, 'nn']
                            
                            if O > 0:
                                if O2 > 0:
                                    if O1 > O2: 
                                        if O1 > O:
                                            avg = (tbl_1.loc[o, 'nn'] + tbl_1.loc[o2, 'nn']) / 2                                        
                                            diff = tbl_1.loc[o1, 'nn'] - avg
                                            
                                            if avg > 0:     
                                                if diff > 0:
                                                    pc = diff / avg
                                                    
                                                    if pc >= spike:
                                                        
                                                        difff = '%.2f' % pc
                                                        angleval =  tbl.loc[o1, angle]
                                                        df = pd.DataFrame([[run, sel, htval, Emis, metval, angle, angleval, difff]], columns = ['run', 'sel', 'htbin', 'Emiss', 'EmissVal', 'Angle', 'AngleVal', 'Difference'])
                                                        df1 = df1.append(df, ignore_index='True')
                                    
                                    
df1.to_csv(r'Spikes{}{}_{}.csv'.format(run, sel, spike), sep='\t', mode='w')    
                
                











