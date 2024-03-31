# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 17:59:04 2024

@author: Marcel Tino
"""

import random
import pandas as pd
import numpy as np
import datetime

def int_column(column_name,start,end,count):
    data[column_name]=np.random.randint(start,end,size=count)
    return data

def cat_column(column_name,variables,count,*args):
    prob=[args]
    select = np.random.choice(variables,size=count)
    data[column_name]=select
    return data

def random_dates(column_name,start,end,n,unit='D',seed=None):
    year1,month1,day1=start.split("-")
    start=datetime.datetime(int(year1),int(month1),int(day1))
    year2,month2,day2=end.split("-")
    end=datetime.datetime(int(year2),int(month2),int(day2))
    if not seed:
        np.random.seed(0)
    ndays=(end-start).days + 1 
    final_date=pd.to_timedelta(np.random.rand(n) * ndays, unit=unit) + start
    start_date=pd.to_datetime(start)
    end_date=pd.to_datetime(end)
    data[column_name]=final_date
    data[column_name]=data[column_name].dt.floor('D')
    return data

