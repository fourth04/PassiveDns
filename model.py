# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import get_settings
import settings

from sqlalchemy import Table, Column, ForeignKey, create_engine, text
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

records_ips = Table('t_records_ips', Base.metadata,
                    Column('record_id', ForeignKey('t_records.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
                    Column('ip_id', ForeignKey('t_ips.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
                    Column('created_at', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True),
                    Column('updated_at', TIMESTAMP, nullable=True),
                    mysql_engine='InnoDB'
                    )

class Record(Base):
    __tablename__ = 't_records'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dname = Column(String(255), unique=True)
    urltype = Column(Integer, nullable=True)
    evilclass = Column(Integer, nullable=True)
    eviltype = Column(Integer, nullable=True)
    source = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    ips = relationship('Ip',
                        cascade='all',
                        secondary=records_ips,
                        back_populates='t_records')

    def __repr__(self):
        return "<Record(id='%s', dname='%s', urltype='%s', evilclass='%s', eviltype='%s', source='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.dname, self.urltype, self.evilclass, self.eviltype, self.source, self.created_at, self.updated_at)

class Ip(Base):
    __tablename__ = 't_ips'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(50), unique=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    records = relationship('Record',
                            cascade='all',
                            secondary=records_ips,
                            back_populates='t_ips')

    def __repr__(self):
        return "<Ip(id='%s', ip='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.ip, self.created_at, self.updated_at )

class SldWhiteItem(Base):
    __tablename__ = 't_sld_white_list'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dname = Column(String(50), unique=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<SldWhiteItem(id='%s', dname='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.dname, self.created_at, self.updated_at )

class WhiteItem(Base):
    __tablename__ = 't_white_list'
    __table_args__ = {'mysql_engine':'InnoDB'}
    record_id = Column(Integer, ForeignKey('t_records.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True )
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    record = relationship('Record',
                          cascade='all')

    def __repr__(self):
        return "<WhiteItem(record_id='%s', created_at='%s', updated_at='%s')>" % ( self.record_id, self.created_at, self.updated_at )

class BlackItem(Base):
    __tablename__ = 't_black_list'
    __table_args__ = {'mysql_engine':'InnoDB'}
    record_id = Column(Integer, ForeignKey('t_records.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True )
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    record = relationship('Record',
                          cascade='all')

    def __repr__(self):
        return "<BlackItem(record_id='%s', created_at='%s', updated_at='%s')>" % ( self.record_id, self.created_at, self.updated_at )

class GreyItem(Base):
    __tablename__ = 't_grey_list'
    __table_args__ = {'mysql_engine':'InnoDB'}
    record_id = Column(Integer, ForeignKey('t_records.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True )
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    record = relationship('Record',
                          cascade='all')

    def __repr__(self):
        return "<GreyItem(record_id='%s', created_at='%s', updated_at='%s')>" % ( self.record_id, self.created_at, self.updated_at )

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
