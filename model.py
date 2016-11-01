# -*- coding: utf-8 -*-
#  import sys
#  reload(sys)
#  sys.setdefaultencoding('utf-8')

import datetime
from utils import get_settings, get_engine
import settings

from sqlalchemy import Table, Column, ForeignKey, text
from sqlalchemy.types import String, Integer, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def to_dict(self):
    r = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    for key,value in r.items():
        if isinstance(value, datetime.datetime):
            r[key] = str(value)
    return r
Base.to_dict = to_dict

SETTINGS = get_settings(settings)
engine = get_engine(SETTINGS)

records_ips = Table('t_records_ips', Base.metadata,
                    Column('record_id', ForeignKey('t_records.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
                    Column('ip_id', ForeignKey('t_ips.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
                    Column('created_at', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True),
                    #  Column('updated_at', TIMESTAMP, nullable=True),
                    mysql_engine='InnoDB'
                    )

class Record(Base):
    __tablename__ = 't_records'
    #  __tablename__ = 't_hlj_cmnet'
    #  __tablename__ = 't_hlj_gprs'
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
                       #  不知道为什么注销了就好了，看样子这个是什么意思得好好研究研究
                        #  back_populates='t_records',
                        #  lazy="dynamic",
                        #  collection_class=set,
                       )

    whois = relationship('Whois',
                        cascade='all')

    content = relationship('Content',
                        cascade='all')

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
                            #  back_populates='t_ips',
                            #  lazy="dynamic",
                            #  collection_class=set,
                           )

    def __repr__(self):
        return "<Ip(id='%s', ip='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.ip, self.created_at, self.updated_at )

class Whois(Base):
    __tablename__ = 't_whois'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('t_records.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True)
    domain_name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    dnssec = Column(String(255), nullable=True)
    emails = Column(String(255), nullable=True)
    expiration_date = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    name_servers = Column(String(255), nullable=True)
    org = Column(String(255), nullable=True)
    referral_url = Column(String(255), nullable=True)
    registrar = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    creation_date = Column(String(255), nullable=True)
    updated_date = Column(String(255), nullable=True)
    whois_server = Column(String(255), nullable=True)
    zipcode = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    record = relationship('Record',
                            cascade='all')

    def __repr__(self):
        return "<Whois(id='%s', record_id ='%s', address = '%s', city = '%s', country = '%s', creation_date = '%s', dnssec = '%s', domain_name = '%s', emails = '%s', expiration_date = '%s', name = '%s', name_servers = '%s', org = '%s', referral_url = '%s', registrar = '%s', state = '%s', status = '%s', updated_date = '%s', whois_server = '%s', zipcode = '%s', created_at='%s', updated_at='%s')>" % ( self.id, self.record_id, self.address, self.city, self.country, self.creation_date, self.dnssec, self.domain_name, self.emails, self.expiration_date, self.name, self.name_servers, self.org, self.referral_url, self.registrar, self.state, self.status, self.updated_date, self.whois_server, self.zipcode, self.created_at, self.updated_at )

class Hlj(Base):
    __tablename__ = 't_hlj'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dname = Column(String(255), unique=True)
    ips = Column(Text, nullable=True)
    parse_count = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Top(id='%s', dname='%s', ips='%s', parse_count='%s')>" % ( self.id, self.dname, self.ips, self.parse_count)

class Content(Base):
    __tablename__ = 't_contents_mobile'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('t_records.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    whois_server = Column(String(255), nullable=True)
    words = Column(Text, nullable=True)
    label = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    records = relationship('Record',
                            cascade='all')

    def __repr__(self):
        return "<Content(id='%s', record_id='%s',redirect_urls='%s', words='%s', target='%s', created_at='%s', updated_at='%s')>" % ( self.id, self.record_id, self.redirect_urls, self.words, self.target, self.created_at, self.updated_at )

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

class Dictionary(Base):
    __tablename__ = 't_dictionary'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(255))
    key = Column(Integer)
    value = Column(String(255))

    def __repr__(self):
        return "<Dictionary(id='%s', category='%s', key='%s', value='%s')>" % ( self.id, self.category, self.key, self.value )

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    init_db()
    #  drop_db()
    #  init_db()
    #  Base.metadata.tables['domains_ips'].create(engine, checkfirst=True)
    #  Base.metadata.tables['t_black_list'].drop(engine, checkfirst=False)
    pass
