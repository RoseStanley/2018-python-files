import pandas as pd

tbl = pd.read_table('tbl_n.process.htbin.metbin.min4Dphi.txt', delim_whitespace=True)

tbl['cumn'] = tbl['n']
tbl['cumn'] = tbl[::-1].groupby(['process', 'htbin', 'metbin'])['cumn'].cumsum()[::-1]
tbl['cumn'] = tbl[::-1].groupby(['process', 'htbin', 'min4Dphi'])['cumn'].cumsum()[::-1]
tbl['cumn'] = tbl[::-1].groupby(['process', 'metbin', 'min4Dphi'])['cumn'].cumsum()[::-1]

tbl.to_csv(r'cumn.process.htbin.metbin.min4Dphi.txt', float_format='%e', index=None, sep='\t', mode='w', index_label='index')
