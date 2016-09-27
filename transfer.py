# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from utils import get_settings
import settings
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from model import Record

import re
import re
ptn_long = re.compile(r'(?:[a-z]*[0-9]+){12,}')

SETTINGS = get_settings(settings)
db_url = URL(drivername='mysql+mysqldb', username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'], host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
engine = create_engine(db_url)

db_url_remote = URL(drivername='mysql+mysqldb', username='evil', password='evil^123456', host='119.29.37.122', port='3306', database='edd')
engine_remote = create_engine(db_url_remote)

n_tmp = engine_remote.execute(text('select count(*) from t_hlj_cmnet'))
n_all = n_tmp.first()[0]
for i in range(0, n_all, 5000):
    select_sql = text('select id, dname, parse_count, urltype, evilclass, eviltype, created_at, updated_at from t_hlj_cmnet limit %s,%s' % (i, i+5000))
    result = engine_remote.execute(select_sql)
    insert_values = [dict(zip(('dname', 'parse_count', 'urltype', 'evilclass', 'eviltype', 'created_at', 'updated_at'), tmp[1:])) for tmp in result.fetchall() if not ptn_long.search(tmp[1])]
    map(lambda x:x.update({'source':0}), insert_values)
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    engine.execute(Record.__table__.insert().prefix_with('IGNORE'), insert_values[:5000])
