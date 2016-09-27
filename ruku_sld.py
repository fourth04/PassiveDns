# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

from datetime import datetime
import re

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

df_white_list = pd.read_csv(u'DataSource/白名单域v1.1.csv', header=None, quotechar='"',sep=',', names = ['dname'], na_values = ['na', '-', '.', ''])
df_white_list['created_at'] = [datetime.now()] * len(df_white_list)
df_white_list['updated_at'] = df_white_list['created_at']
df_white_list.index.name = 'id'
df_white_list.to_sql('t_sld_white_list', engine, if_exists='replace')


result = engine.execute('select updated_at from t_sld_white_list order by updated_at desc limit 1')
last_update_time = result.first()[0]
if df_white_list['updated_at'].max() < last_update_time:
    df_white_list = pd.read_sql_table('t_sld_white_list', engine, index_col='id')
