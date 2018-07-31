import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import itertools
pd.set_option('display.width', None)
matplotlib.style.use('ggplot')


mes = ['metbin']#, 'mhtbin']
angles = ['minArccotF', 'minChi', 'minOmegaHat']
htvals = [0, 50, 60, 70, 80, 90, 100, 110]

for k in range (len(mes)):
    me = mes[k]
    for j in range (len(angles)):    
        angle = angles[j]   
        inpath = '~/Documents/file_simulations/tbl_20180726_01_trg/heppy/set_all/sel_030/020_counts/tbl_n.process.htbin.metbin.mhtbin.{}.txt'.format(angle)
        
        
        
        
        
        
        
        
        
        