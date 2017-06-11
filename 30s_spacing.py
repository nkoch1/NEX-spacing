# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:19:08 2017

@author: nils
"""
#import modules
import pandas as pd
import numpy as np
from numpy import nan as NaN
import datetime

#read data from csv file saved from excel
#change path as appropriate for desired file
data = pd.read_csv(r'C:\Users\nils\NEX spacing\Testdata.csv', sep = ',', encoding = 'utf-8')

#initializing variables for new dataframe concat
adjdata = pd.DataFrame()
firsttime = data.loc[0,'TimeDate']
t1 = datetime.datetime.strptime(firsttime,'%I:%M:%S %p')
i1 = 0
delta = datetime.timedelta(0, 30)
#initialize mean, std, and cov variables
m1 = 0
m2 = 0
m3 = 0
sd1 = 0
sd2 = 0
sd3 = 0
c1 = 0
c2 = 0
c3 = 0

#loop over old data and generate new time chunked data as well as tack on the 
#last chunk no matter how small
for index, row in data.iterrows():
    t = datetime.datetime.strptime(row['TimeDate'],'%I:%M:%S %p')
    #check time within 30s of first time
    #first time is updated to last time of previous iteration
    if t <= t1 + delta and index < len(data.index)-1:
        continue
    #also ensures last chunk added if not a full 30s
    elif t <= t1 + delta and index == len(data.index)-1:
        print(row['TimeDate'])
        adjdata = adjdata.append(data.iloc[i1:index, :], ignore_index = True)
        m1 = np.mean(data.iloc[i1:index, 7])
        sd1 = np.std(data.iloc[i1:index, 7])
        c1 = sd1/m1
        m2 = np.mean(data.iloc[i1:index, 9])
        sd2 = np.std(data.iloc[i1:index, 9])
        c2 = sd2/m2
        m3 = np.mean(data.iloc[i1:index, 11])
        sd3 = np.std(data.iloc[i1:index, 11])
        c3 = sd3/m3
        list1 = [NaN, NaN, NaN, NaN, NaN, NaN, 'avg', m1, 'avg', m2,'avg', m3]
        list2 = [NaN, NaN, NaN, NaN, NaN, NaN, 'sd', sd1, 'sd', sd2, 'sd', sd3]
        list3 = [NaN, NaN, NaN, NaN, NaN, NaN, 'cov', c1, 'cov', c2, 'cov', c3]
        s2 = pd.Series(list1, index = list(data.columns.values))
        s3 = pd.Series(list2, index = list(data.columns.values))
        s4 = pd.Series(list3, index = list(data.columns.values))
        adjdata = adjdata.append(s2, ignore_index = True)
        adjdata = adjdata.append(s3, ignore_index = True)
        adjdata = adjdata.append(s4, ignore_index = True)
    #adds each 30s chunk with appended 3 lines with avg, std, cov
    #time delta is updated after first iteration to 29s in order to maintain 
    #inclusivity of 30s
    else:
        print(row['TimeDate'])
        adjdata = adjdata.append(data.iloc[i1:index, :], ignore_index = True)
        m1 = np.mean(data.iloc[i1:index, 7])
        sd1 = np.std(data.iloc[i1:index, 7])
        c1 = sd1/m1
        m2 = np.mean(data.iloc[i1:index, 9])
        sd2 = np.std(data.iloc[i1:index, 9])
        c2 = sd2/m2
        m3 = np.mean(data.iloc[i1:index, 11])
        sd3 = np.std(data.iloc[i1:index, 11])
        c3 = sd3/m3
        list1 = [NaN, NaN, NaN, NaN, NaN, NaN, 'avg', m1, 'avg', m2,'avg', m3]
        list2 = [NaN, NaN, NaN, NaN, NaN, NaN, 'sd', sd1, 'sd', sd2, 'sd', sd3]
        list3 = [NaN, NaN, NaN, NaN, NaN, NaN, 'cov', c1, 'cov', c2, 'cov', c3]
        s2 = pd.Series(list1, index = list(data.columns.values))
        s3 = pd.Series(list2, index = list(data.columns.values))
        s4 = pd.Series(list3, index = list(data.columns.values))
        adjdata = adjdata.append(s2, ignore_index = True)
        adjdata = adjdata.append(s3, ignore_index = True)
        adjdata = adjdata.append(s4, ignore_index = True)
        t1 = datetime.datetime.strptime(row['TimeDate'],'%I:%M:%S %p')
        i1 = index
        delta = datetime.timedelta(0, 29)

#export to csv file, change file name as desired
adjdata.to_csv('outputdata.csv', sep = ',')
    