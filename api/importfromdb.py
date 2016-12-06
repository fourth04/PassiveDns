import sys
sys.path.append('../')

from sqlalchemy import create_engine, text
from sqlalchemy.sql import select
from sqlalchemy.engine.url import URL
from model import Record

import datetime
import time
import logging
import logging.config

def run(engine):
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    db_url_remote = URL(drivername='mysql+mysqldb', username='evil', password='evil^123456', host='10.104.243.193', port='3306', database='edd')
    engine_remote = create_engine(str(db_url_remote) + '?charset=utf8', pool_recycle=1000, encoding='utf-8')

    record = Record.__table__
    s = select([record.c.dname]).where(record.c.source == 11).order_by(record.c.id.desc()).limit(1)
    while True:
        try:
            remote_last_dname = engine.execute(s).fetchone()[0]
            remote_last_id = engine_remote.execute(text('select id from t_result where dname = :dname'), {'dname':remote_last_dname}).scalar() if remote_last_dname else 0
            if not remote_last_id:
                remote_last_id = 0
            result_proxy = engine_remote.execute(text('select dname from t_result where id > :id limit 5000'), {'id':remote_last_id})
            if result_proxy.rowcount > 0:
                logger.info('Select %s data from remote_database' % result_proxy.rowcount)
                insert_values = [{'dname':dname[0], 'source':11, 'updated_at':datetime.datetime.now()} for dname in result_proxy]
                insert_r = engine.execute(record.insert().prefix_with('IGNORE'), insert_values)
                if insert_r.rowcount:
                    logger.info('Insert %s records to local_database' % insert_r.rowcount)
            else:
                logger.info('No data are waiting to resolve, ready to sleep')
                time.sleep(60*30)
        except Exception as e:
            logger.error(e)

def main():
    from utils import get_settings, get_engine
    import settings
    SETTINGS = get_settings(settings)
    engine = get_engine(SETTINGS)
    logging.basicConfig(level=logging.DEBUG)
    run(engine)

if __name__ == '__main__':
    main()
