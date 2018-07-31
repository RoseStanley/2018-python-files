import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
pd.set_option('max_column', 300)
matplotlib.style.use('ggplot')

angles = ['minArccotF']#, 'minChi', 'minOmegaHat']

for i in range (len(angles)):
    angle = angles[i]
    path = '~/Documents/file_simulations/tbl_20180719_01_trg/heppy/set_all/sel_030/020_counts/tbl_n.process.htbin.metbin.mhtbin.{}.txt'.format(angle)

    tbl = pd.read_table(path, delim_whitespace=True)
    keys = ['process', 'htbin', 'metbin', 'mhtbin', angle]
    tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
    tbl_mesh.columns = keys
    tbl = pd.merge(tbl_mesh, tbl, how='left')
    tbl.fillna(0, inplace=True)
    
    
    tbl1 = tbl.groupby(['process', 'metbin','mhtbin',angle])['n'].sum().reset_index()
    
    dbg = tbl1
    dbg = dbg[dbg.process != 'T1tttt_1350_1100']
    dbg = dbg[dbg.process != 'T1tttt_1950_500']
    dbg = dbg[dbg.process != 'T2bb_675_600']
    dbg = dbg[dbg.process != 'T2bb_1200_300']  
    dbg['cumn'] = dbg['n']
    dbg['cumn'] = dbg[::-1].groupby(['process', 'mhtbin', 'metbin'])['cumn'].cumsum()[::-1]
    dbg['cumn'] = dbg[::-1].groupby(['process', 'mhtbin', angle])['cumn'].cumsum()[::-1]
    dbg['cumn'] = dbg[::-1].groupby(['process', 'metbin', angle])['cumn'].cumsum()[::-1]
    #dbg['cumn'] = dbg[::-1].groupby(['mhtbin', 'metbin', angle])['cumn'].cumsum()[::-1]
    
    dbg['nn'] = dbg['n']
    dbg['nn'] = dbg[::-1].groupby(['mhtbin', 'metbin', angle]).cumsum()[::-1]    
    
#    dsg = tbl1 
##    dsg = dsg[dsg.process != 'QCD']
##    dsg = dsg[dsg.process != 'TTJets']
##    dsg = dsg[dsg.process != 'WJetstoLNu']
##    dsg = dsg[dsg.process != 'ZJetstoNuNu']
##    dsg = dsg[dsg.process != 'T1tttt_1350_1100']
##    dsg = dsg[dsg.process != 'T1tttt_1950_500']
##    dsg = dsg[dsg.process != 'T2bb_1200_300']
#    dsg = dsg[dsg.process == 'T2bb_675_600']    
#    
#    dsg['cumn'] = dsg['n']
#    dsg['cumn'] = dsg[::-1].groupby(['process', 'mhtbin', 'metbin'])['cumn'].cumsum()[::-1]
#    dsg['cumn'] = dsg[::-1].groupby(['process', 'mhtbin', angle])['cumn'].cumsum()[::-1]
#    dsg['cumn'] = dsg[::-1].groupby(['process', 'metbin', angle])['cumn'].cumsum()[::-1]
#    
#    dsg['nn'] = dsg['n']
#    
#    d2 = pd.concat([dsg, dbg], axis=0, ignore_index=True)
#        
#    d2['log10cumn'] = np.log10(d2['cumn'])
#    d2['log10n'] = np.log10(d2['nn'])
    
    dbg['log10cumn'] = np.log10(dbg['cumn'])
    dbg['log10n'] = np.log10(dbg['n'])
    
    g = sns.FacetGrid(dbg, col='metbin', row="mhtbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
    g.map(plt.hist, angle, 'log10cumn', where='post')
    g.add_legend()
    plt.show()
    
    g = sns.FacetGrid(dbg, col='metbin', row="mhtbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
    g.map(plt.step, angle, 'log10n', where='post')
    g.add_legend()
