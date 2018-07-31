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
mes = ['metbin']#, 'mhtbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
#htvals = [400, 600, 800, 1000]

for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath = '~/Documents/file_nanoAOD/tbl_nanoAOD_2018{}{}_01/sel_020/010_component_counts/tbl_n.component.htbin.{}.{}.txt'.format(month,date, me, angle)
        
        tbl = pd.read_table(inpath, delim_whitespace=True)
        keys = ['htbin', me, angle]
        tbl_mesh = pd.DataFrame(list(itertools.product(*[np.sort(tbl[c].unique()) for c in keys])))
        tbl_mesh.columns = keys
        tbl = pd.merge(tbl_mesh, tbl, how='left')
        tbl.fillna(0, inplace=True)
        
        #tbl['n'] = tbl['n'] / 3600000 
        
        """Background Stacked"""
        dbg = tbl        
        dbg['cumn'] = dbg['n']
        dbg['cumn'] = dbg[::-1].groupby(['htbin', me])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby(['htbin', angle])['cumn'].cumsum()[::-1]
        dbg['cumn'] = dbg[::-1].groupby([ me, angle])['cumn'].cumsum()[::-1]
        
        dbg['nn'] = dbg['n']
        dbg['nn'] = dbg[::-1].groupby(['htbin', me, angle])['nn'].cumsum()[::-1]
        
#        """RateTables"""    
#        for i in range (len(htvals)):
#            df = dbg
#            htval = htvals[i]
#            df = df[df.htbin == htval]
#            df2 = df.pivot_table('cumn', [angle], me)
#            df2.to_csv(r'{}_rate.htbin{}.{}.{}.csv'.format(run, htval, me, angle), sep='\t', mode='w') #, float_format='%6f')
#    
        
        """StackLogGraphs"""
        d2 = dbg
        d2['log10cumn'] = np.log10(d2['cumn'])
        d2['log10n'] = np.log10(d2['nn'])
        
#        d2 = d2[d2[me] != 0]               
#        d2 = d2[d2.htbin != 0]
        
        """PlotStackedCumnGraphs"""
        g = sns.FacetGrid(d2, col=me, row="htbin", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10cumn', where='post')
        g.add_legend()
        plt.savefig('{}{}_cumn_rate.htbin.{}.{}.png'.format(month, date, me, angle))
        
        """PlotStackedNGraphs"""
        g = sns.FacetGrid(d2, col=me, row="htbin", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10n', where='post')
        g.add_legend()
        plt.savefig('{}{}_n.htbin.{}.{}.png'.format(month, date, me, angle))
  
    
    
    
    
    
    
    
















