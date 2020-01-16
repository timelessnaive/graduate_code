'''
目标：针对问题1：溯源的数据整理脚本
结果：
1. data_year_opiod
属性：dict
key=年份(int)，value=每年阿片类药物成瘾的上报情况(DataFrame)
DataFrame:
    Index:州编号
    col:年份(YYYY),是否为阿片类药物成瘾(is_opiod),上报人数(DrugReports),
    所在地经度(LAT)，纬度(LNG)
    
2. data_year_not_opiod :基本同上
'''

import pandas as pd

def p1_data():
    
    path='C:/Users/Mr.rice/iCloudDrive/毕业/2018_MCMProblemC_DATA/MCM_NFLIS_Data.xlsx'
    NFLIS_Data=pd.read_excel(path,sheet_name=1)
    data_deal=NFLIS_Data.loc[:,['YYYY','FIPS_Combined','SubstanceName','DrugReports']]
    opioid=['Morphine','Methadone','Opium','Heroin','Oxycodone']
    
    _=data_deal.SubstanceName.isin(opioid) #某个元素是否在一类中要用isin
    data_deal=pd.DataFrame({'is_opiod':_})
    data_deal=pd.concat([data_deal,data_deal],axis=1) #列操作要加axis=1
    
    data_deal.drop(columns='SubstanceName',inplace=True) #删除药品名称这一列
    
    data_clean=data_deal['DrugReports'].groupby([data_deal.YYYY,
                        data_deal.FIPS_Combined,data_deal.is_opiod]).sum() #iloc按位置选择，loc按标签选择
    
    data_clean=data_deal.groupby(['YYYY','FIPS_Combined','is_opiod'])[['DrugReports']].sum() #iloc按位置选择，loc按标签选择
    
    data_clean.reset_index(inplace=True) 
    
    #地理位置坐标
    
    loc=pd.read_excel('C:/Users/Mr.rice/iCloudDrive/毕业/2018_MCMProblemC_DATA/C题经纬度数据.xlsx',sheet_name=1)
    res=pd.concat([loc.FIPS_Combined,loc.LAT,loc.LNG],axis=1) #列合并
    loc=res.drop_duplicates()#去除重复的行
    # 合并数据，包括地理位置和每年上报人数
    
    data_ad=pd.merge(data_clean,loc,how='outer',on='FIPS_Combined')
    data_ad_opiod=data_ad[data_ad.is_opiod==True]
    data_ad_not_opiod=data_ad[data_ad.is_opiod==False]
    
    data_year_opiod=dict()
    data_year_not_opiod=dict()
    
    # dict[年份]=对应年份的合并数据
    for year in range(2010,2017+1):
        data_year_opiod[year]=data_ad_opiod[data_ad_opiod.YYYY==year].set_index(['FIPS_Combined'])
        data_year_not_opiod[year]=data_ad_not_opiod[data_ad_not_opiod.YYYY==year].set_index(['FIPS_Combined'])
    
    return [data_year_opiod,data_year_not_opiod]

(data_year_opiod,data_year_not_opiod)=p1_data()