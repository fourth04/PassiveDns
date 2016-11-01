import sys
sys.path.append('../')

def get_settings(settings):
    return {tmp:getattr(settings, tmp) for tmp in dir(settings) if tmp.isupper()}

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

def get_engine(settings):
    SETTINGS = settings
    db_url = URL(drivername=SETTINGS['DB_DRIVER'], username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'],
            host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
    engine = create_engine(str(db_url) + '?charset=utf8', pool_recycle=1000, encoding='utf-8')
    return engine
