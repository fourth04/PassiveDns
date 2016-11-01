import aiohttp
import asyncio
import async_timeout
import aiodns

import json
import logging

from collections import namedtuple
QueryResult = namedtuple('QueryResult', ['host', 'ttl'])

async def fetch(session, url, params):
    with async_timeout.timeout(100):
        async with session.get(url, params=params) as response:
            return await response.text()

async def fetch_no_params(session, url):
    with async_timeout.timeout(100):
        async with session.get(url) as response:
            return await response.text()

async def resolve(resolver, dname):
    try:
        return await resolver.query(dname, 'A')
    except aiodns.error.DNSError as e:
        query_result = QueryResult('127.0.0.1', '255')
        return [query_result]

async def main_resolve(loop, dnames, resolved_result):
    tasks = []
    resolver = aiodns.DNSResolver(loop=loop)
    #  dnames = [ 'www.sfasdfasdfasdfasdfasdfasd.com.cn.jp', 'sssss.baddddssasf.avwefaw.z' ]
    for dname in dnames:
        task = asyncio.ensure_future(resolve(resolver, dname))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    #  print(responses)
    data = zip(dnames, responses)
    resolved_result += [(dname, result.host, result.ttl) for dname,response in data for result in response]
    return resolved_result

async def main_address(loop, ips):
    url = 'http://ip.taobao.com/service/getIpInfo.php?'
    #  url = 'http://freeapi.ipip.net/'
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for ip in ips:
            task = asyncio.ensure_future(fetch(session, url, {'ip':ip}))
            #  task = asyncio.ensure_future(fetch_no_params(session, url+ip))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print(responses)
        #  return [json.loads(response) for response in responses]

async def main_resolve_address(loop, dnames):
    resolved_result = await main_resolve(loop, dnames)
    ips = resolved_result
    await main_address(loop, ips)

from sqlalchemy import create_engine, select, bindparam
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from model import *

def main():
    SETTINGS = get_settings(settings)

    db_url = URL(drivername=SETTINGS['DB_DRIVER'], username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'],
            host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
    engine = create_engine(db_url, pool_recycle=1000)
    Session = sessionmaker(bind=engine)
    session = Session()

    #  logger = logging.getLogger('resolve')
    logger = logging.getLogger()

    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    #  records = session.query(Record).filter(Record.urltype == 2).limit(5)
    records = session.query(Record).filter(and_(Record.urltype == 2, Record.ips.any(Ip.ip != None))).limit(5)

    record = Record.__table__
    select_s = select([record.c.id, record.c.dname]).where(record.c.urltype != None).limit(10)
    while True:
        try:
            select_r = engine.execute(select_s)
            data_tmp = select_r.fetchall()
            if data_tmp:
                logger.info('Select data from database')
                data_chunk = [dict(_id=tmp[0], dname=tmp[1]) for tmp in data_tmp]
                dnames = [_['dname'] for _ in data_chunk]
                resolved_result = []
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(main_resolve(loop, dnames, resolved_result))
                loop.run_until_complete(future)
                #  if update_r:
                    #  logger.info('Update %s records' % update_r)
            else:
                time.sleep(999)
                continue
        except Exception as e:
            logger.error(e)



if __name__ == '__main__':
    main()

