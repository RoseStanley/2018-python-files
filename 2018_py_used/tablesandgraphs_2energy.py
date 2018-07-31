import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')


month = '06'
date = '29'
folder = 'all' #'EWK_QCD'
mes = ['mhtbin']#, 'mhtbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
#htvals = [0, 400, 600, 800, 1000 ]

for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath = '~/Documents/file_simulations/tbl_2018{}{}_01_trg/heppy/set_{}/sel_020/020_counts/tbl_n.process.htbin.{}.{}.txt'.format(month, date, folder, me, angle)
        
        tbl = pd.read_table(inpath, delim_whitespace=True)
        keys = ['process', 'htbin', me, angle]
        tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
        tbl_mesh.columns = keys
        tbl = pd.merge(tbl_mesh, tbl, how='left')
        tbl.fillna(0, inplace=True)
        
        """Background Stacked"""
        dbg = tbl
#        dbg = dbg[dbg.process != 'T1tttt_1350_1100']
#        dbg = dbg[dbg.process != 'T1tttt_1950_500']
#        dbg = dbg[dbg.process != 'T2bb_675_600']
#        dbg = dbg[dbg.process != 'T2bb_1200_300']
        
        dbg['cumn'] = dbg['n']
        dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', me])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['process', me, angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['htbin', me, angle])['cumn'].cumsum()[::-1]
        
        dbg['nn'] = dbg['n']
        dbg['nn'] = dbg.groupby(['htbin', me, angle])['nn'].cumsum()
         
        """Signal Unstacked"""
        dsg = tbl 
        dsg = dsg[dsg.process != 'QCD']
        dsg = dsg[dsg.process != 'TTJets']
        dsg = dsg[dsg.process != 'WJetstoLNu']
        dsg = dsg[dsg.process != 'ZJetstoNuNu']
        
        
        dsg['cumn'] = dsg['n']
#        dsg['cumn'] = dsg.groupby(['htbin', me, angle])['cumn'].cumsum()
        dsg['cumn'] = dsg.groupby(['process', 'htbin', me])['cumn'].cumsum()
        dsg['cumn'] = dsg.groupby(['process', 'htbin', angle])['cumn'].cumsum()
        dsg['cumn'] = dsg.groupby(['process', me, angle])['cumn'].cumsum()
        
        dsg['nn'] = dsg['n']
##        dsg['nn'] = dsg.groupby(['htbin', me, angle])['nn'].cumsum()
        
#        """RateTables"""    
#        for i in range (len(htvals)):
#            df = dbg
#            htval = htvals[i]
#            df = df[df.htbin == htval]
#            df = df[df.process == 'QCD']
#            df2 = df.pivot_table('cumn', [angle], me)
#            df2.to_csv(r'{}_rate.htbin{}.{}.{}.csv'.format(date, htval, me, angle), sep='\t', mode='w') #, float_format='%6f')
        
        """Combine Background and Signal"""    
        d2 = pd.concat([dsg, dbg], axis=0, ignore_index=True)
        
        """StackLogGraphs"""
        d2['log10cumn'] = np.log10(d2['cumn'])
        d2['log10n'] = np.log10(d2['nn'])
        
#        d2 = d2[d2[me] != 0]               
#        d2 = d2[d2.htbin != 0]
        
        """PlotStackedCumnGraphs"""
        g = sns.FacetGrid(d2, col=me, row="htbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10cumn', where='post')
        g.add_legend()
        plt.savefig('R{}{}_cumn_rate.htbin.{}.{}.png'.format(month, date, me, angle))
        
        """PlotStackedNGraphs"""
        g = sns.FacetGrid(d2, col=me, row="htbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10n', where='post')
        g.add_legend()
        plt.savefig('R{}{}_n.htbin.{}.{}.png'.format(month, date, me, angle))
  
    
    
    
    
    
    
    
















