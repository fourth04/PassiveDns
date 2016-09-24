# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import get_settings
import settings

from sqlalchemy import Table, Column, ForeignKey, create_engine
from sqlalchemy.types import String, Integer, CHAR, BIGINT, TIMESTAMP
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

Base = declarative_base()
SETTINGS = get_settings(settings)
db_url = URL(drivername='mysql+mysqldb', username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'],
        host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
#  db_url = 'mysql+mysqldb://'+SETTINGS['DB_USER']+':'+SETTINGS['DB_PASSWD']+'@'+SETTINGS['DB_HOST']+'/'+SETTINGS['DB_DB']
engine = create_engine(db_url)

domains_ips = Table('domains_ips', Base.metadata,
                    Column('domain_id', ForeignKey('domains.id'), primary_key=True),
                    Column('ip_id', ForeignKey('ips.id'), primary_key=True),
                    Column('created_at', TIMESTAMP, nullable=True),
                    Column('updated_at', TIMESTAMP, nullable=True),
                    mysql_engine='InnoDB'
                    )

class Domain(Base):
    __tablename__ = 'domains'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dname = Column(String(255), unique=True)
    parse_count = Column(Integer, nullable=True)
    urltype = Column(Integer, nullable=True)
    evilclass = Column(Integer, nullable=True)
    eviltype = Column(Integer, nullable=True)
    check_source = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    ips = relationship('Ip',
                        secondary=domains_ips,
                        back_populates='domains')

    def __repr__(self):
        return "<Domain(id='%s', dname='%s', parse_count='%s' urltype='%s', evilclass='%s', eviltype='%s', check_source='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.dname, self.parse_count, self.urltype, self.evilclass, self.eviltype, self.check_source, self.created_at, self.updated_at)

class Ip(Base):
    __tablename__ = 'ips'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(50), unique=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    domains = relationship('Domain',
                            secondary=domains_ips,
                            back_populates='ips')

    def __repr__(self):
        return "<Ip(id='%s', ip='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.ip, self.created_at, self.updated_at )

class ParentDomain(Base):
    __tablename__ = 'parent_domains'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dname = Column(String(50), unique=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return "<ParentDomain(id='%s', dname='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.dname, self.created_at, self.updated_at )

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    init_db()
    #  drop_db()
    #  Base.metadata.tables['domains_ips'].create(engine, checkfirst=True)
    #Base.metadata.tables['t_black_list'].drop(engine, checkfirst=False)
    pass
