# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:05:00 2020

@author: Mr.rice
"""
from time import time
from pearson_gray import pearson_data_collection,compare_replace,form_pearson,cal_gra
from P1_data_collection import p1_data
from P2_data_collection import p2_data


def main():
    #得到整理好的数据
    county_y=p2_data()
    (data_year_opiod,data_year_not_opiod)=p1_data()
    data_pearson=pearson_data_collection(county_y,data_year_opiod)
    #计算Pearson相关系数
    pearson_mean=compare_replace(form_pearson(data_pearson))
    
    #计算灰色关联度
    gra_sum=compare_replace(cal_gra(data_pearson))
    
    return (pearson_mean,gra_sum)
    
    
if __name__ == '__main__':
    t1=time()
    
    ans=main() #(pearson_mean,gra_sum)
    
    t2=time()
    print('{0:.2f}s'.format(t2-t1))
    
