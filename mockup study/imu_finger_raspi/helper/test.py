import random
import pandas as pd
import numpy as np
from IPython.display import display
import string
import os

def find_delinqbucket_corresponding_col_name(delinqbucket_value):
    if delinqbucket_value == '1-29':
        return "1-29 \'1,222,112\'",5
    elif delinqbucket_value == '30':
        return "30-59 \'1,222,112\'",6
    elif delinqbucket_value == '60':
        return "60-89 \'1,222,112\'",7
    elif delinqbucket_value == '90':
        return "90-119 \'1,222,112\'",8
    elif delinqbucket_value == '120':
        return "120-149 \'1,222,112\'",9
    elif delinqbucket_value == '150':
        return "150-179 \'1,222,112\'",10
    else:
        return "180+ \'1,222,112\'",11



def getBusinessServices():
    sample_data = []
    for i in range(6):
        sample_MMDATE = ["2020-01-04"]
        sample_SOURCE_KEY_VALUE = [''.join(random.choices(string.ascii_letters, k=3))+str(random.randint(1000,9999))]
        sample_delinqbucket = [random.choice(['1-29','30','60','90','120','150','180'])]

        randomlist = sample_MMDATE+ sample_SOURCE_KEY_VALUE+random.sample(range(1000, 3000), 11) + sample_delinqbucket
        sample_data.append(randomlist)

    df1_col_name= ['MMDATE','SOURCE_KEY_VALUE','SOURC_ID-DESC',
                   'ORIG_DT','DPD_NA','DAYS_DEL',
                   'NET_BK_AMT','TOTAL_COMMITTMENT','RISK_RTG',
                   'CUR_LOB_CD','PRODUCT','ACT_DA_PST_CNT',
                   'DPD','delinqbucket']
    df2_col_name = ["LOB str","Product str","Month \'2020-02-02\'",
                    "Credit limit \'1,222,112\'","Outstanding '1,222,112'","1-29 \'1,222,112\'",
                    "30-59 \'1,222,112\'","60-89 \'1,222,112\'","90-119 \'1,222,112\'",
                    "120-149 \'1,222,112\'","150-179 \'1,222,112\'","180+ \'1,222,112\'",
                    "Gross charged off \'1,222,112\'","Facilities \'1,222,112\'"]
    delinqbucket_list = ['1-29','30','60','90','120','150','180']

    df = pd.DataFrame(sample_data,columns=df1_col_name)
    display(df)

    result_table = []
    for delinqbucket_value in delinqbucket_list:
        print(delinqbucket_value)
        tmp_result = [0] * 14
        sum_of_TOTAL_COMMITTMENT = df.loc[df['delinqbucket'] == delinqbucket_value, 'TOTAL_COMMITTMENT'].sum()
        sum_of_NET_BK_AMT = df.loc[df['delinqbucket'] == delinqbucket_value, 'NET_BK_AMT'].sum()
        sum_of_row = df.loc[df['delinqbucket'] == delinqbucket_value].shape[0]

        tmp_result[3] = sum_of_TOTAL_COMMITTMENT
        tmp_result[4] = sum_of_NET_BK_AMT
        tmp_result[find_delinqbucket_corresponding_col_name(delinqbucket_value)[1]] = sum_of_NET_BK_AMT
        tmp_result[13] = sum_of_row

        print(tmp_result)
        if sum_of_row != 0:
            result_table.append(tmp_result)

    # print(result_table)
    new_df = pd.DataFrame(result_table, columns=df2_col_name)
    new_df.to_csv('out.csv')
    df.to_csv("input.csv")
    display(new_df)



getBusinessServices()