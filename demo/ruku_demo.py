# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

from datetime import datetime

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
#  df3 = pd.read_csv('sort_domain_sh', header=None, quotechar='"',sep='\t', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
chunksize = 10 ** 5
chunks = pd.read_csv('DataSource/sort_domain_sh', chunksize=chunksize, header=None, quotechar='"',sep=',', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
#  chunks = pd.read_csv('DataSource/sort_domain_sh', chunksize=chunksize, header=None, quotechar='"',sep='\t', names = ['dname', 'parse_count'], na_values = ['na', '-', '.', ''])
df3 = pd.concat([chunk for chunk in chunks])
#  df = df1.join(df2, on='dname', how='outer', lsuffix='_cmnet', rsuffix='_gprs')
df = pd.merge(df1, df2, how='outer', on='dname')
df.fillna(0, inplace=True)
df['parse_count']=df['parse_count_x']+df['parse_count_y']
del df['parse_count_x']
del df['parse_count_y']
del df1,df2

df_full = pd.merge(df3, df, how='outer', on='dname')
df_full.fillna(0, inplace=True)
df_full['parse_count']=df_full['parse_count_x']+df_full['parse_count_y']
del df_full['parse_count_x']
del df_full['parse_count_y']
del df

#  下面的方法太耗内存
#  multi_level_dname = df.index.str.findall('[^\.]+')
#  multi_level_dname = df['dname'].str.findall('[^\.]+')
#  df['sld'] = multi_level_dname.str[-2:].map('.'.join)
#  df['tld'] = multi_level_dname.str[-3:].map('.'.join)

df['sld'] = df['dname'].map(lambda x:'.'.join(x.split('.')[-2:]))

sld_pc_sum = df.groupby('sld')['parse_count'].sum().sort_values(ascending=False)
sld_pc_count = df.groupby('sld')['parse_count'].count().sort_values(ascending=False)
df.sld.isin(sld_pc_sum.index[:500]).value_counts()
df_to_sql = df[~df.sld.isin(sld_pc_sum.index[:500])]

data = dict(dname=sld_pc_sum.index[:500],created_at=[datetime.now()]*500,updated_at=[datetime.now()]*500)
df_top = DataFrame(data)
#  df_top = DataFrame(data,columns=['dname','created_at','updated_at'])

#  数字开头的域名
import re
ptn_long = re.compile(r'(?:[a-z]*[0-9]+){12,}')
df_to_sql = df_to_sql[~df_to_sql['dname'].str.contains(ptn_long)]
df_to_sql.iloc[:5000,:2].T.to_dict()

from IPython import embed;embed()

from utils import get_settings
import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from model import SldWhiteItem

SETTINGS = get_settings(settings)
db_url = URL(drivername='mysql+mysqldb', username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'],
        host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
engine = create_engine(db_url)

df_top.index.name = 'id'
df_top.to_sql('t_sld_white_list', engine, if_exists = 'replace')
df_top.iloc[:,:].to_sql('t_sld_white_list',engine,if_exists='append')
