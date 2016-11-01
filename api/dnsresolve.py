import sys
sys.path.append('../')

import asyncio
import aiodns

import logging
import datetime
import time
import traceback

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from model import *

from collections import namedtuple
QueryResult = namedtuple('QueryResult', ['host', 'ttl'])

async def resolve(resolver, dname):
    try:
        return await resolver.query(dname, 'A')
    except Exception as e:
        #  print('when resolve %s an error occurred, %s' % (dname, e))
        query_result = QueryResult('127.0.0.1', '255')
        return [query_result]

async def main_resolve(loop, dnames, resolved_result):
    tasks = []
    resolver = aiodns.DNSResolver(loop=loop)
    for dname in dnames:
        task = asyncio.ensure_future(resolve(resolver, dname))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    data = zip(dnames, responses)
    resolved_result.update(dict(data))
    return resolved_result

def run(engine):
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    Session = sessionmaker(bind=engine)
    session = Session()
    last_id = 0
    while True:
        try:
            query = session.query(Record).outerjoin(records_ips).filter(records_ips.c.record_id == None).filter(Record.id>last_id).order_by(Record.id).limit(5000)
            n_count = query.count()
            if n_count:
                logger.info('Select %s data from database' % n_count)
                dnames = [ record.dname for record in query ]
                last_id = query[-1].id
                resolved_result = {}
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(main_resolve(loop, dnames, resolved_result))
                loop.run_until_complete(future)
                logger.info('Dns resolve Over')
                for record in query:
                    hosts = {tmp.host for tmp in resolved_result[record.dname]}
                    record_ips = {tmp.ip for tmp in record.ips}
                    create_hosts = hosts - record_ips
                    delete_hosts = record_ips - hosts
                    if create_hosts:
                        logger.debug('Create some relationship record of dname and ip')
                        for host in create_hosts:
                            try:
                                session.begin_nested()
                                ip = Ip(ip=host, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
                                #  record.ips.add(ip)
                                record.ips.append(ip)
                                session.flush()
                            except IntegrityError as e:
                                session.rollback()
                                ip = session.query(Ip).filter(Ip.ip == host).first()
                                #  record.ips.add(ip)
                                record.ips.append(ip)
                            else:
                                session.commit()
                    if delete_hosts:
                        logger.debug('Delete some relationship record of dname and ip')
                        try:
                            for host in delete_hosts:
                                ip = [tmp for tmp in record.ips if tmp.ip == host][0]
                                #  ip = session.query(Ip).filter(Ip.ip == host).first()
                                if not ip.records:
                                    session.delete(ip)
                                record.ips.remove(ip)
                        except Exception as e:
                            logger.error(e)
                else:
                    session.commit()
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

