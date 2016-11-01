import sys
sys.path.append('../')

import datetime
import time
import json
import logging
import logging.config
from multiprocessing.dummy import Pool as ThreadPool

import traceback

from sqlalchemy.sql import select, and_, func

from model import Record, Whois
import whois

def to_string(d):
    for key,value in d.items():
        if value:
            try:
                d[key] = json.dumps(value, ensure_ascii = False)
            except TypeError:
                tmp_value = [str(tmp) for tmp in value]
                d[key] = json.dumps(tmp_value, ensure_ascii = False)
    return d

def whois_plus(d):
    try:
        w = whois.whois(d['dname'])
        if w and [tmp for tmp in w.values() if tmp]:
            tmp_set1 = set(['country', 'referral_url', 'creation_date', 'org', 'updated_date', 'whois_server', 'city', 'registrar', 'dnssec', 'expiration_date', 'status', 'state', 'name_servers', 'domain_name', 'address', 'zipcode', 'emails', 'name']) - set(w.keys())
            for tmp in tmp_set1:
                w.update({tmp:None})
            tmp_set2 = set(w.keys()) - set(['country', 'referral_url', 'creation_date', 'org', 'updated_date', 'whois_server', 'city', 'registrar', 'dnssec', 'expiration_date', 'status', 'state', 'name_servers', 'domain_name', 'address', 'zipcode', 'emails', 'name'])
            for tmp in tmp_set2:
                del w[tmp]
            d.update(to_string(w))
            del d['dname']
            return d
        else:
            return None
    except Exception:
        #  traceback.print_exc()
        return None

def whois_check(data, n_threads):
    pool = ThreadPool(n_threads)
    try:
        results = pool.map(whois_plus, data)
        pool.close()
        pool.join()
        return [ tmp for tmp in results if tmp ]
    except Exception:
        traceback.print_exc()
        raise

def run(engine):
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    record = Record.__table__
    whois = Whois.__table__
    select_s = select([record.c.id, record.c.dname]).select_from(record.outerjoin(whois)).where(whois.c.record_id == None).order_by(record.c.id).limit(5000)
    last_id = 0
    while True:
        try:
            select_r = engine.execute(select_s.where(record.c.id>last_id))
            n_count = select_r.rowcount
            if n_count:
                logger.info('Select %s data from database' % n_count)
                data_chunk = [dict(record_id=tmp[0], dname=tmp[1], updated_at = str(datetime.datetime.now())) for tmp in select_r]
                last_id = data_chunk[-1]['record_id']
                checked_results = whois_check(data_chunk, 30)
                if checked_results:
                    logger.info('Whois check over, get {} results'.format(len(checked_results)))
                    insert_s = whois.insert().prefix_with("IGNORE")
                    insert_r = engine.execute(insert_s, checked_results)
                    logger.info('Insert %s records to dababase' % insert_r.rowcount)
            else:
                last_id = 0
                logger.info('No data are waiting to resolve, ready to sleep')
                time.sleep(60*5)
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
