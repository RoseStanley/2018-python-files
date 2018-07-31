import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')


run = '3'
sel = '2'
folder = 'all'
mes = ['metbin', 'mhtbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
htvals = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]

for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath = '~/Documents/file_simulations/tbl_20180706_0{}_trg/heppy/set_{}/sel_0{}0/020_counts/tbl_n.process.htbin.{}.{}.txt'.format(run, folder, sel, me, angle)
        
        tbl = pd.read_table(inpath, delim_whitespace=True)        
        keys = ['process', 'htbin', me, angle]
        tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
        tbl_mesh.columns = keys
        tbl = pd.merge(tbl_mesh, tbl, how='left')
        tbl.fillna(0, inplace=True)

        """Background Stacked"""
        dbg = tbl
        
        dbg['cumn'] = dbg['n']
        dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', me])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['process', me, angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['htbin', me, angle])['cumn'].cumsum()[::-1]
        
        
    
        """RateTables"""    
        for i in range (len(htvals)):
            df = dbg
            htval = htvals[i]
            df = df[df.htbin == htval]
            df = df[df.process == 'QCD']
            df2 = df.pivot_table('cumn', [angle], me)
            df2.to_csv(r'20180706_0{}_rate.htbin{}.{}.{}_0{}0.csv'.format(run, htval, me, angle, sel), sep='\t', mode='w') #, float_format='%6f')
          
    
#    
#        """Background Stacked"""
#        dbg = tbl
#        dbg = dbg[dbg.process != 'T1tttt_1350_1100']
#        dbg = dbg[dbg.process != 'T1tttt_1950_500']
#        dbg = dbg[dbg.process != 'T2bb_675_600']
#        dbg = dbg[dbg.process != 'T2bb_1200_300']
#        
#        
#        dbg['cumn'] = dbg['n']
#        dbg['cumn'] = dbg[::-1].groupby(['htbin', me, angle])['cumn'].cumsum()[::-1]       
#        dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', me])['cumn'].cumsum()[::-1]
#        dbg['cumn'] = dbg[::-1].groupby(['process', 'htbin', angle])['cumn'].cumsum()[::-1]
#        dbg['cumn'] = dbg[::-1].groupby(['process', me, angle])['cumn'].cumsum()[::-1]
#        
#        dbg['nn'] = dbg['n']
#        dbg['nn'] = dbg.groupby(['htbin', me, angle])['nn'].cumsum()
#         
#        """Signal Unstacked"""
#        dsg = tbl 
#        dsg = dsg[dsg.process != 'QCD']
#        dsg = dsg[dsg.process != 'TTJets']
#        dsg = dsg[dsg.process != 'WJetstoLNu']
#        dsg = dsg[dsg.process != 'ZJetstoNuNu']       
#        
#        dsg['cumn'] = dsg['n']
#        dsg['cumn'] = dsg[::-1].groupby(['process', 'htbin', me])['cumn'].cumsum()[::-1]
#        dsg['cumn'] = dsg[::-1].groupby(['process', 'htbin', angle])['cumn'].cumsum()[::-1]
#        dsg['cumn'] = dsg[::-1].groupby(['process', me, angle])['cumn'].cumsum()[::-1]
#        
#        dsg['nn'] = dsg['n']
#        
#        """Combine Background and Signal"""    
#        d2 = pd.concat([dsg, dbg], axis=0, ignore_index=True)
#        
#        """StackLogGraphs"""
#        d2['log10cumn'] = np.log10(d2['cumn'])
#        d2['log10n'] = np.log10(d2['nn'])      
#        
#        d2 = d2[d2[me] != 0]                       
#        d2 = d2[d2.htbin != 0]
#        d2 = d2[d2.htbin != 90]
#        d2 = d2[d2[me] != 150] 
#        
#        """PlotStackedCumnGraphs"""
#        g = sns.FacetGrid(d2, col=me, row="htbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
#        g.map(plt.step, angle, 'log10cumn', where='post')
#        g.add_legend()
#        plt.savefig('20180706_0{}_cumnrate.htbin.{}.{}_0{}0.png'.format(run, me, angle, sel))
#        
#        """PlotStackedNGraphs"""
#        g = sns.FacetGrid(d2, col=me, row="htbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
#        g.map(plt.step, angle, 'log10n', where='post')
#        g.add_legend()
#        plt.savefig('20180706_0{}_nrate.htbin.{}.{}_0{}0.png'.format(run, me, angle, sel))   
#    
#    
#    
#    
#















