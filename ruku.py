# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series

# 方案一
#  df1 = pd.read_csv('hlj_cmnet.csv', header=None, quotechar='"',sep=',', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
#  df2 = pd.read_csv('hlj_gprs.csv', header=None, quotechar='"',sep=',', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
#  df = pd.concat([df1, df2], ignore_index=True).drop_duplicates()

# 方案二
#  df1 = pd.read_csv('hlj_cmnet.csv', header=None, index_col=0, quotechar='"',sep=',', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
#  df2 = pd.read_csv('hlj_gprs.csv', header=None, index_col=0, quotechar='"',sep=',', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
#  full_index = df1.index.union(df2.index)
#  df1 = df1.reindex(full_index,fill_value=0)
#  df2 = df2.reindex(full_index,fill_value=0)
#  df = df1 + df2
#  df = df1.add(df2, fill_value=0)

# 方案三
df1 = pd.read_csv('hlj_cmnet.csv', header=None, quotechar='"',sep=',', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
df2 = pd.read_csv('hlj_gprs.csv', header=None, quotechar='"',sep=',', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
#  df = df1.join(df2, on='dname', how='outer', lsuffix='_cmnet', rsuffix='_gprs')
df = pd.merge(df1, df2, how='outer', on='dname')
df.fillna(0, inplace=True)
df['parse_count']=df['parse_count_x']+df['parse_count_y']
del df['parse_count_x']
del df['parse_count_y']
del df1,df2

#  数字开头的域名
#  df[df['dname'].str.contains('^\d{6}')].head()

#  multi_level_dname = df.index.str.findall('[^\.]+')
#  multi_level_dname = df['dname'].str.findall('[^\.]+')
#  df['sld'] = multi_level_dname.str[-2:].map('.'.join)
#  df['tld'] = multi_level_dname.str[-3:].map('.'.join)

df['sld'] = df['dname'].map(lambda x:'.'.join(x.split('.')[-2:]))

sld_pc_sum = df.groupby('sld')['parse_count'].sum().sort_values(ascending=False)
sld_pc_count = df.groupby('sld')['parse_count'].count().sort_values(ascending=False)
df.sld.isin(sld_pc_sum.index[:499]).value_counts()
from IPython import embed;embed()
#  tld_pc_sum = df.groupby('tld')['parse_count'].sum().sort_values(ascending=False)
#  tld_pc_count = df.groupby('tld')['parse_count'].count().sort_values(ascending=False)

from datetime import datetime
from utils import get_settings
import settings
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from model import Domain,Ip,ParentDomain

SETTINGS = get_settings(settings)
db_url = URL(drivername='mysql+mysqldb', username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'],
        host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
engine = create_engine(db_url)

