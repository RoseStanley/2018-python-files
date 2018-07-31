import pandas as pd
pd.set_option('display.width', None)
pd.set_option('display.max_columns', 50)

rate = 10
redlim = 2
anglim = 0.8

"""Check file paths"""

run = '3'
sel = '3'

Emiss = ['htbin']#, 'mhtbin', 'metbin']
Emiss2 = ['mhtbin']# 'metbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
htvals = [0, 100, 200, 300, 400, 500]
hetvals = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900']
metvals = ['0', '100', '200', '300', '400', '500']

df1 = pd.DataFrame(columns = ['Emiss', 'EmissVal', 'Angle', 'AngleVal', 'Rate', 'RateZero', 'Reduction'])
df2 = pd.DataFrame(columns = ['mhtbin', 'metbin', 'Angle', 'AngleVal', 'Rate', 'RateZero', 'Reduction'])

for i in range (len(Emiss)):
    Emis = Emiss[i]
    """Tables with 2 forms of Energy"""
    for j in range (len(Emiss2)):
        Emis2 = Emiss2[j]
        for k in range (len(angles)):
            angle  = angles[k]
            for l in range (len(htvals)):
                htval = htvals[l]
                
                inpath = '20180719_01_rate.mhtbin{}.metbin.{}_030.csv'.format(htval, angle)
                tbl = pd.read_table(inpath, delim_whitespace=True)   
                
                for m in range (len(metvals)):
                    metval = metvals[m]
                    limtbl = tbl[[metval]]
                    ratezero = limtbl.iloc[0].item()                        
                    limtbl['diff'] = abs(limtbl[metval] - rate)                       
                    indx = limtbl['diff'].idxmin()
                    
                    rateval = tbl.loc[indx, metval]
                    angleval = tbl.loc[indx, angle]
                    red = ratezero / rateval
                    
                    if red >= redlim:
                        if angleval <= anglim:
                            df = pd.DataFrame([[htval, metval, angle, angleval, rateval, ratezero, red]], columns = ['mhtbin', 'metbin', 'Angle', 'AngleVal', 'Rate', 'RateZero', 'Reduction'])
                            df2 = df2.append(df, ignore_index='True')
                    
    df2.to_csv(r'20180719_01_2Ecuts_0{}0_rate{}.csv'.format(run, rate), sep='\t', mode='w') 
        
#        for n in range (len(angles)):
#            angle  = angles[n]
#            
#            inpath = '~/Documents/201807_trg_plts/20180706_rate_comp/20180706_0{}_0{}0/20180706_0{}_rate.{}.{}_0{}0.csv'.format(run, sel, run, Emis, angle, sel)
#            tbl = pd.read_table(inpath, delim_whitespace=True) 
#            
#            for o in range (len(htvals)):
#                hetval = hetvals[o]
#                limtbl = tbl[[hetval]]
#                ratezero = limtbl.iloc[0].item()                        
#                limtbl['diff'] = abs(limtbl[hetval] - rate)                       
#                indx = limtbl['diff'].idxmin()
#                
#                rateval = tbl.loc[indx, hetval]
#                angleval = tbl.loc[indx, angle]
#                red = ratezero / rateval
#                
#                if red >= redlim:
#                    if angleval <= anglim:
#                        df = pd.DataFrame([[Emis, hetval, angle, angleval, rateval, ratezero, red]], columns = ['Emiss', 'EmissVal', 'Angle', 'AngleVal', 'Rate', 'RateZero', 'Reduction'])
#                        df1 = df1.append(df, ignore_index='True')
#    
#    else:
#        
#        """Tables with 1 form of Energy"""    
#        for n in range (len(angles)):
#            angle = angles[n]
#            
#            inpath = '~/Documents/201807_trg_plts/20180706_rate_comp/20180706_0{}_0{}0/20180706_0{}_rate.{}.{}_0{}0.csv'.format(run, sel, run, Emis, angle, sel)
#            tbl = pd.read_table(inpath, delim_whitespace=True) 
#            
#            for o in range (len(metvals)):
#                metval = metvals[o]
#                limtbl = tbl[[metval]]
#                ratezero = limtbl.iloc[0].item()                        
#                limtbl['diff'] = abs(limtbl[metval] - rate)                       
#                indx = limtbl['diff'].idxmin()
#                
#                rateval = tbl.loc[indx, metval]
#                angleval = tbl.loc[indx, angle]
#                red = ratezero / rateval
#                
#                if red >= redlim:
#                    if angleval <= anglim:
#                        df = pd.DataFrame([[Emis, metval, angle, angleval, rateval, ratezero, red]], columns = ['Emiss', 'EmissVal', 'Angle', 'AngleVal', 'Rate', 'RateZero', 'Reduction'])
#                        df1 = df1.append(df, ignore_index='True')
#                   
#df1.to_csv(r'20180706_0{}_1Ecuts_0{}0_rate{}.csv'.format(run, sel, rate), sep='\t', mode='w')                     
#                        
                    
                    
        


        
        
        

