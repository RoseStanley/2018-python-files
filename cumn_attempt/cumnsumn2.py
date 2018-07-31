import pandas as pd

d = pd.read_table('tbl_n.process.metbin.min4Dphi.txt', delim_whitespace=True)

total = d.groupby('process')['n'].sum()
print(total)

#group_htbin = d.groupby(['process','htbin'])
#s1 = group_htbin['n'].apply(lambda x: x.loc[::-1].cumsum().loc[::-1])
#print(s1)

group_metbin = d.groupby(['process','metbin'])
s2 = group_metbin['n'].loc[::-1].cumsum().loc[::-1]
t2 = group_metbin['n'].sum()



#group_min4Dphi = d.groupby(['process','min4Dphi'])
#s3 = group_min4Dphi['n'].apply(lambda x: x.loc[::-1].cumsum().loc[::-1])
#t3 = group_min4Dphi['n'].apply(lambda x: x.sum())
#
#
#
#group_met_4Dphi = d.groupby(['process','metbin','min4Dphi'])
#s4 = group_met_4Dphi['n'].apply(lambda x: x.loc[::-1].cumsum().loc[::-1])
#t4 = group_met_4Dphi['n'].apply(lambda x: x.sum())

print(s2)
#print(s3)
#print(s4)

print(t2)
#print(t3)
#print(t4)

