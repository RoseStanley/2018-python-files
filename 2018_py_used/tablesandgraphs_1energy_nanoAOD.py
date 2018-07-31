import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')

run = 29
mes = ['metbin', 'mhtbin'] #['htbin'] 
angles = ['minArccotF', 'minChi', 'minOmegaHat']
for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath = '~/Documents/file_nanoAOD/tbl_nanoAOD_201806{}_01/sel_020/010_component_counts/tbl_n.component.{}.{}.txt'.format(run, me, angle)
    
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
        
        dbg['nn'] = dbg['n']
        dbg['nn'] = dbg[::-1].groupby([ me, angle])['nn'].cumsum()[::-1]
        
        """RateTables"""    
        
        df = dbg
        df2 = df.pivot_table('cumn', [angle], me)
        df2.to_csv(r'{}_rate.{}.{}.csv'.format(run, me, angle), sep='\t', mode='w') #, float_format='%6f')
        
        """StackLogGraphs"""
        d2 = dbg
        d2['log10cumn'] = np.log10(d2['cumn'])
        d2['log10n'] = np.log10(d2['nn'])
        
        d2 = d2[d2[me] != 0]               

        
        """PlotStackedCumnGraphs"""
        g = sns.FacetGrid(d2, col=me, hue="process", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10cumn', where='post')
        g.add_legend()
        plt.savefig('{}_cumn_rate.{}.{}.png'.format(run, me, angle))
        
        """PlotStackedNGraphs"""
        g = sns.FacetGrid(d2, col=me, hue="process", margin_titles=True, legend_out = True, sharey=True)
        g.map(plt.step, angle, 'log10n', where='post')
        g.add_legend()
        plt.savefig('{}_n.{}.{}.png'.format(run, me, angle))