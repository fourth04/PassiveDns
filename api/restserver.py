import sys
sys.path.append('../')

from aiohttp import web

import logging
import logging.config

from sqlalchemy import create_engine, select, bindparam, func, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from model import *

def run(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    async def detail_handle(request):
        in_dname = request.match_info.get('dname')
        record = session.query(Record).filter(Record.dname == in_dname).scalar()
        try:
            data = {
                'ck_result':record.to_dict(),
                'ips':[tmp.ip for tmp in record.ips] if record.ips else [],
                'whois':record.whois.to_dict() if record.whois else ''
            }
            return web.json_response(data)
        except Exception as e:
            return web.Response(text="Sorry, i can't find record in our database")

    async def dnamecheck_handle(request):
        in_dname = request.match_info.get('dname')
        record = session.query(Record).filter(Record.dname == in_dname).scalar()
        try:
            data = {
                'ck_result':record.to_dict()
            }
            return web.json_response(data)
        except Exception as e:
            return web.Response(text="Sorry, i can't find record in our database")

    async def dname2ip_handle(request):
        in_dname = request.match_info.get('dname')
        record = session.query(Record).filter(Record.dname == in_dname).scalar()
        try:
            data = {
                'ips':[tmp.ip for tmp in record.ips] if record.ips else [],
            }
            return web.json_response(data)
        except Exception as e:
            return web.Response(text="Sorry, i can't find record in our database")

    async def ip2dname_handle(request):
        in_ip = request.match_info.get('ip')
        ip = session.query(Ip).filter(Ip.ip == in_ip).scalar()
        try:
            data = {
                'dnames':[tmp.dname for tmp in ip.records] if ip.records else []
            }
            return web.json_response(data)
        except Exception as e:
            return web.Response(text="Sorry, i can't find record in our database")

    async def dname2whois_handle(request):
        in_dname = request.match_info.get('dname')
        record = session.query(Record).filter(Record.dname == in_dname).scalar()
        try:
            data = {
                'whois':record.whois.to_dict() if record.whois else ''
            }
            return web.json_response(data)
        except Exception as e:
            return web.Response(text="Sorry, i can't find record in our database")

    async def whois2dname_handle(request):
        in_whois = request.match_info.get('whois')
        whois_query = session.query(Whois).filter(or_(Whois.emails.like('%'+in_whois+'%'), Whois.registrar.like('%'+in_whois+'%')))
        try:
            data = {
                'dnames':[tmp.record.dname for tmp in whois_query]
            }
            return web.json_response(data)
        except Exception as e:
            return web.Response(text="Sorry, i can't find record in our database")

    app = web.Application()
    app.router.add_get('/detail/{dname}', detail_handle)
    app.router.add_get('/dnamecheck/{dname}', dnamecheck_handle)
    app.router.add_get('/dname2ip/{dname}', dname2ip_handle)
    app.router.add_get('/ip2dname/{ip}', ip2dname_handle)
    app.router.add_get('/dname2whois/{dname}', dname2whois_handle)
    app.router.add_get('/whois2dname/{whois}', whois2dname_handle)

    web.run_app(app, port=8000)


def main():
    from utils import get_settings, get_engine
    import settings
    SETTINGS = get_settings(settings)
    engine = get_engine(SETTINGS)
    logging.basicConfig(level=logging.DEBUG)
    run(engine)

if __name__ == '__main__':
    main()
