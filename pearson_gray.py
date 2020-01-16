# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:47:28 2020

@author: Mr.rice

"""
#皮尔逊相关系数
import pandas as pd
import numpy as np
def pearson_data_collection(county_y,data_year):
    #county_y=p2_data()
    #(data_year_opiod,data_year_not_opiod)=p1_data()
    data_pearson=dict()
    for year in range(2010,2016+1):
        _=pd.merge(data_year[year],
                     county_y[year],
                     left_index=True,
                     right_index=True,
                     how='inner')
        data_pearson[year]=_.drop(columns=['YYYY','is_opiod','LAT','LNG'])
    return data_pearson


def pearson(x, y):
    meanX = x.mean()
    deviationX = x.std(ddof=0)
    stardardizedX = (x - meanX) / deviationX
    
    meanY = y.mean()
    deviationY = y.std(ddof=0)
    stardardizedY = (y - meanY) / deviationY
    return (stardardizedX*stardardizedY).mean()


#灰色关联度计算
def gra(vec,label,rou=0.5):
    
    vec=(vec - vec.min()) / (vec.max() - vec.min())
    _=(label-vec).apply(abs)
    ma=np.amax(_);mi=np.amin(_)
    return (mi+rou*ma)/(_+rou*ma)

def compare_replace(pearson_mean):
    path=r'C:\Users\Mr.rice\iCloudDrive\毕业\2018_MCMProblemC_DATA\P2_data\ACS_16_5YR_DP02_metadata.csv'
    ori=pd.read_csv(path,engine='python')
    ori=ori.set_index(['GEO.id'])

    comp_dict=ori.to_dict()['Id'] #得到指标编号与内容的对应字典
    pearson_mean.index=pearson_mean.index.map(comp_dict) #替换index
    pearson_mean.sort_values(by='mean',inplace=True,ascending=False) #从大到小排序
    return pearson_mean
    
def cal_func(data_pearson,func):
    pearson_num=dict()
    for year in range(2010,2016+1):
        ori=data_pearson[year]
        _=dict()
        col=ori.columns
        for j in range(1,ori.shape[1]):
            _[col[j]]=func(ori.iloc[:,0],ori.iloc[:,j])
            
            #key=指标名，value=func相关系数
            
        _=pd.DataFrame(data=_,index=[year])
        
        pearson_num[year]=_
    return pearson_num

def form_pearson(data_pearson):
    pearson_num=cal_func(data_pearson,pearson)
    res=pearson_num[2010]
    for year in range(2011,2016+1):
        res=pd.concat([res,pearson_num[year]],sort=True,join='inner')
    res=res.T
    #res.sort_values(by=year,inplace=True,ascending=False)
    pearson_mean=pd.DataFrame(res.mean(axis=1),columns=['mean'])
    
    return pearson_mean
    
def cal_gra(data_pearson):
    gra_num=dict()
    for year in range(2010,2016+1):
        ori=data_pearson[year]
        res=pd.DataFrame()
        col=ori.columns
        for j in range(1,ori.shape[1]):
            res[col[j]]=gra(ori.iloc[:,0],ori.iloc[:,j])
        gra_num[year]=res.sum(axis=0)
    
    res=pd.Series()
    for inde in gra_num[2010].index:
        try:
            res[inde]=gra_num[2010][inde]+gra_num[2011][inde]+gra_num[2012][inde]+\
                    gra_num[2013][inde]+gra_num[2014][inde]+gra_num[2015][inde]+\
                    gra_num[2016][inde]
        except :
            pass
    return pd.DataFrame(data=res,columns=['mean'])