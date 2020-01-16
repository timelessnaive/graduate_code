'''
结果：
1. county_y
属性：dict 
key=州编号(int)
value=298个指标(DataFrame)
'''
#import numpy as np
import pandas as pd
#暂不考虑 margin of error

def p2_data():
    path=r'C:\Users\Mr.rice\iCloudDrive\毕业\2018_MCMProblemC_DATA\P2_data\\'
    county_y=dict()
    for year in range(2010,2016+1):
        county_y[year]=pd.read_csv(
                path+r'ACS_{0}_5YR_DP02_with_ann.csv'.format(year-2000)
                ,engine='python') #读取csv文件，路径中含有中文要加engine='python'
        
        data=county_y[year]
        res=data.drop(columns=['GEO.id','GEO.display-label'])#删除多余的列
        #res=res.rename(columns=res.iloc[0]) #删除表头的编号，如HC01_VC03
        
        l=[];col=res.columns
        for i in range(res.shape[1]):
            if('Margin' in res.iloc[0][i] or 'X' in res.iloc[1][i]):
                l.append(col[i])
                
        res_=res.drop(columns=l)
        res_.drop(index=0,inplace=True)
        res__=res_.apply(pd.to_numeric,errors='coerce') #errors='coerce'
        
        county_y[year]=res__.set_index(['GEO.id2'])#将州的编号作为index
        
    return county_y

county_y=p2_data()
        