# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from utils import get_settings
import settings
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from model import Record,Ip,SldWhiteItem

SETTINGS = get_settings(settings)
db_url = URL(drivername='mysql+mysqldb', username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'], host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
#  engine = create_engine(db_url)
#  DBSession = sessionmaker(engine)
#  session = DBSession()

#  session.add(Domain(dname='www.qq.com', parse_count='100000', created_at=datetime.now(), updated_at=datetime.now()))
#  session.query(Domain).first().ips = [Ip(ip='1.1.1.1', created_at=datetime.now(), updated_at=datetime.now()]

import json
import pprint
import requests
import traceback
from multiprocessing.dummy import Pool as ThreadPool

def domain_report(domain):
    url = "http://www.virustotal.com/vtapi/v2/domain/report"
    parameters = {"domain": domain,
                  "apikey": "164be93e854cf96810730375aebda0a0843e35400876392d73e056b0a570d06d"}
    i = 1
    while True:
        try:
            if i > 3:
                return
            r = requests.get(url, params=parameters)
        except requests.exceptions.ConnectionError as e:
            print e
            print 'The %s attempt' % i
            time.sleep(5)
            i += 1
    return json.loads(r.text)

domains = ['10086dx.com.cn.w.kunlunno.com', 'byc.00810086.com', 'ccbgdhcs03.ccbgz.com', 'hxkmjbhozev.www.m3637.com']
#  domains = ['www.baidu.com', 'www.10086.com', 'www.qq.com', 'www.bilibili.com', 'www.163.com'] * 3
#  pool = ThreadPool(4)
#  results = pool.map(domain_report, domains)
#  pool.close()
#  pool.join

results = []
for domain in domains:
    print domain
    results.append( domain_report(domain) )

i = 0
for tmp_d in results:
    with open(str(i) + '.json', 'wb') as f:
        json.dump(tmp_d, f, indent=4, ensure_ascii=False)
    i += 1
