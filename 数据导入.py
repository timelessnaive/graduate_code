import pandas as pd

# 文件名：MCM_NFLIS_Data.xlsx
# 文件内容：
# sheet1:DATE RANGE:
#        REQUESTED DRUGS:
#        LOCATION:
#
# sheet2:data
#
# sheet3:指标解释

NFLIS_Data=pd.read_excel('C:/Users/Mr.rice/OneDrive/毕业/2018_MCMProblemC_DATA/MCM_NFLIS_Data.xlsx',sheet_name=2)

