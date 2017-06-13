# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:19:08 2017

@author: nils
"""
# import modules
import os
import pandas as pd
import numpy as np
from numpy import nan as NaN
import datetime


def load_data():
    """
    Asks user for filename (inclusive absolute path) and
    loads the datafile into a Pandas dataframe.

    Input:
    ---------------------
    filename <= name of datafile

    Output:
    ---------------------
    data <= Pandas DataFrame of the datafile
    """
    filename = input('Please enter filename with absolute directory path: ')
    data = pd.read_csv(filename, sep=',', encoding='utf-8')
    return(data, filename)


def user_time_delta():
    """
    Ask user to specify a delta time interval to group data by.

    Output:
    ---------------------
    delta <= time interval by which to group data.
    """
    tinterval = input('Please enter a time interval by which to group data: ')
    tinterval = float(tinterval)
    delta = datetime.timedelta(0, tinterval)
    return(delta)


def adjdata(data, delta):
    """
    Loop over data table inputed and add a average, standard deviation, and
    covariance in three new lines for every delta (second) time group as
    specified by the user.
    Last time group is however long it needs to be.

    Input:
    ---------------------
    data <= Input Pandas DataFrame of existing data.

    delta <= group data by time interval as determined by user.

    Output:
    ---------------------
    adjdata <= Output Pandas DataFrame of adjusted data with
               avg, std, and cov calculated and inserted for every
               delta time groups in 3 new rows.
    """

    [adjdata, firsttime, t1, i1,
     m1, m2, m3, sd1, sd2, sd3, c1, c2, c3] = initialize_variables(data)

    for index, row in data.iterrows():
        t = datetime.datetime.strptime(row['TimeDate'], '%I:%M:%S %p')
        # check time within 30s of first time
        if t <= t1 + delta and index < len(data.index)-1:
            continue
        # ensures last time group is added even if not a full 30s
        elif t <= t1 + delta and index == len(data.index)-1:
            print(row['TimeDate'])
            adjdata = adjdata.append(data.iloc[i1:index, :], ignore_index=True)
            m1 = np.mean(data.iloc[i1:index, 7])
            sd1 = np.std(data.iloc[i1:index, 7])
            c1 = sd1/m1
            m2 = np.mean(data.iloc[i1:index, 9])
            sd2 = np.std(data.iloc[i1:index, 9])
            c2 = sd2/m2
            m3 = np.mean(data.iloc[i1:index, 11])
            sd3 = np.std(data.iloc[i1:index, 11])
            c3 = sd3/m3
            list1 = [NaN, NaN, NaN, NaN, NaN, NaN,
                     'avg', m1, 'avg', m2, 'avg', m3]
            list2 = [NaN, NaN, NaN, NaN, NaN, NaN,
                     'sd', sd1, 'sd', sd2, 'sd', sd3]
            list3 = [NaN, NaN, NaN, NaN, NaN, NaN,
                     'cov', c1, 'cov', c2, 'cov', c3]
            s2 = pd.Series(list1, index=list(data.columns.values))
            s3 = pd.Series(list2, index=list(data.columns.values))
            s4 = pd.Series(list3, index=list(data.columns.values))
            adjdata = adjdata.append(s2, ignore_index=True)
            adjdata = adjdata.append(s3, ignore_index=True)
            adjdata = adjdata.append(s4, ignore_index=True)
        # first time is updated to last time of previous iteration
        # adds each 30s chunk with appended 3 lines with
        # avg, std, cov to adjdata DataFrame
        # time delta is updated after 1st iteration to 29s in order to maintain
        # inclusivity of 30s
        else:
            print(row['TimeDate'])
            adjdata = adjdata.append(data.iloc[i1:index, :], ignore_index=True)
            m1 = np.mean(data.iloc[i1:index, 7])
            sd1 = np.std(data.iloc[i1:index, 7])
            c1 = sd1/m1
            m2 = np.mean(data.iloc[i1:index, 9])
            sd2 = np.std(data.iloc[i1:index, 9])
            c2 = sd2/m2
            m3 = np.mean(data.iloc[i1:index, 11])
            sd3 = np.std(data.iloc[i1:index, 11])
            c3 = sd3/m3
            list1 = [NaN, NaN, NaN, NaN, NaN, NaN,
                     'avg', m1, 'avg', m2, 'avg', m3]
            list2 = [NaN, NaN, NaN, NaN, NaN, NaN,
                     'sd', sd1, 'sd', sd2, 'sd', sd3]
            list3 = [NaN, NaN, NaN, NaN, NaN, NaN,
                     'cov', c1, 'cov', c2, 'cov', c3]
            s2 = pd.Series(list1, index=list(data.columns.values))
            s3 = pd.Series(list2, index=list(data.columns.values))
            s4 = pd.Series(list3, index=list(data.columns.values))
            adjdata = adjdata.append(s2, ignore_index=True)
            adjdata = adjdata.append(s3, ignore_index=True)
            adjdata = adjdata.append(s4, ignore_index=True)
            t1 = datetime.datetime.strptime(row['TimeDate'], '%I:%M:%S %p')
            i1 = index
            delta = delta - datetime.timedelta(0, 1)

    return(adjdata)


def initialize_variables(data):
    """
    Initialize Variables to be used.
    """
    adjdata = pd.DataFrame()
    firsttime = data.loc[0, 'TimeDate']
    t1 = datetime.datetime.strptime(firsttime, '%I:%M:%S %p')
    i1 = 0
    m1 = 0
    m2 = 0
    m3 = 0
    sd1 = 0
    sd2 = 0
    sd3 = 0
    c1 = 0
    c2 = 0
    c3 = 0
    return(adjdata, firsttime, t1, i1, m1, m2, m3, sd1, sd2, sd3, c1, c2, c3)


def save_data(adjdata, filename):
    """
    Export and save adjusted data to a CSV file.
    """
    basename = os.path.basename(filename)
    pathname = os.path.dirname(filename)
    adjdata.to_csv(r'%s/%s-adjusted.csv' % (pathname, basename))


if __name__ == '__main__':
    [data, filename] = load_data()
    delta = user_time_delta()
    adjdata = adjdata(data, delta)
    save_data(adjdata)
