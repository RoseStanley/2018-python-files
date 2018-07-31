import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
pd.set_option('display.max_columns', 10)
matplotlib.style.use('ggplot')


month = '07'
date = '10'
folder = 'EWK_QCD'
mes = ['metbin']#, 'mhtbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
htvals = [400, 600, 800, 1000]

for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath_sim = '~/Documents/file_nanoAOD/tbl_2018{}{}_01_trg/nanoaod/set_{}/sel_020/020_counts/tbl_n.process.htbin.{}.{}.txt'.format(month, date, folder, me, angle)
        inpath_data = '~/Documents/file_nanoAOD/tbl_2018{}{}_01_trg/nanoaod/MET/sel_020/010_dataset_counts/tbl_n.dataset.htbin.{}.{}.txt'.format(month, date, me, angle)
           
        tbl_sim = pd.read_table(inpath_sim, delim_whitespace=True)
        keys = ['process', 'htbin', me, angle]
        tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl_sim[c].unique()) for c in keys])))
        tbl_mesh.columns = keys
        tbl_sim = pd.merge(tbl_mesh, tbl_sim, how='left')
        tbl_sim.fillna(0, inplace=True)
             
        
        tbl_data = pd.read_table(inpath_data, delim_whitespace=True)  
        keys = ['htbin', me, angle]
        tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl_data[c].unique()) for c in keys])))
        tbl_mesh.columns = keys
        tbl_data = pd.merge(tbl_mesh, tbl_data, how='left')
        tbl_data.fillna(0, inplace=True)
        tbl_data['n'] = tbl_data['n'] / 3600000 
        
        """Sim Background Stacked"""              
        sbs = tbl_sim 
        sbs['cumn'] = sbs['n']
        sbs['cumn'] = sbs[::-1].groupby(['process', 'htbin', me])['cumn'].cumsum()[::-1]
        sbs['cumn'] = sbs[::-1].groupby(['process', 'htbin', angle])['cumn'].cumsum()[::-1]
        sbs['cumn'] = sbs[::-1].groupby(['process', me, angle])['cumn'].cumsum()[::-1]
        sbs['cumn'] = sbs[::-1].groupby(['htbin', me, angle])['cumn'].cumsum()[::-1]
        
        sbs['nn'] = sbs['n']
        sbs['nn'] = sbs[::-1].groupby(['htbin', me, angle])['nn'].cumsum()[::-1]
                  
        #sbs = sbs[sbs.process == 'QCD']
        
        """Data Cumulation"""
        dcs = tbl_data        
        dcs['cumn'] = dcs['n']
        dcs['cumn'] = dcs[::-1].groupby(['htbin', me])['cumn'].cumsum()[::-1]
        dcs['cumn'] = dcs[::-1].groupby(['htbin', angle])['cumn'].cumsum()[::-1]
        dcs['cumn'] = dcs[::-1].groupby([ me, angle])['cumn'].cumsum()[::-1]
        
        dcs['nn'] = dcs['n']
        dcs['nn'] = dcs[::-1].groupby(['htbin', me, angle])['nn'].cumsum()[::-1] 
        
        dcs['dataset'] = 'MET'
        
#        """RateTables"""    
#        for i in range (len(htvals)):
#            df = dcs
#            htval = htvals[i]
#            df = df[df.htbin == htval]
#            df2 = df.pivot_table('cumn', [angle], me)
#            df2.to_csv(r'{}{}_rate.htbin{}.{}.{}.csv'.format(month, date, htval, me, angle), sep='\t', mode='w')
#       
        """Combine Background and Signal"""         
        dcs['process'] = dcs['dataset']
        sbs['dataset'] = sbs['process']
        d2 = pd.concat([dcs, sbs], axis=0, ignore_index=True)
#        
#        
        """StackLogGraphs"""
        d2['log10cumn'] = np.log10(d2['cumn'])
        d2['log10n'] = np.log10(d2['nn'])
        
        d2 = d2[d2[me] != 0]               
        d2 = d2[d2[me] != 100]
        
        """PlotStackedCumnGraphs"""
        g = sns.FacetGrid(d2, col=me, row="htbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10cumn', where='post')
        g.add_legend()
        plt.savefig('MET_SIM_{}{}_cumn_rate.htbin.{}.{}_020.png'.format(month, date, me, angle))
        
        """PlotStackedNGraphs"""
        g = sns.FacetGrid(d2, col=me, row="htbin", hue="process", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10n', where='post')
        g.add_legend()
        plt.savefig('MET_SIM_{}{}_n.htbin.{}.{}_020.png'.format(month, date, me, angle))
        
       
        
        
        
        
        
        
        
        
        
        
        