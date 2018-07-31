import pandas as pd

#d = pd.read_table('tbl_n.process.htbin.metbin.min4Dphi.txt', delim_whitespace=True)
#df = d.groupby(['process','htbin', 'metbin']).sum().loc[::-1].groupby(level=[0]).cumsum().loc[::-1]
#np.cumsum(x[::-1])[::-1] 
#d['cumn'] = d.ix[::-1, 'n'].cumsum()[::-1]



d = pd.read_table('tbl_n.process.htbin.metbin.min4Dphi.txt', delim_whitespace=True)
d['cumn'] = d.groupby('process')['n'].apply(lambda x: x.loc[::-1].cumsum().loc[::-1])
d.to_csv(r'cumn.process.htbin.metbin.min4Dphi.txt', float_format='%e', index=None, sep='\t', mode='w', index_label='index')




#.apply(lambda x: x.loc[::-1].cumsum().loc[::-1])