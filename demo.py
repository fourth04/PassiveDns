from utils import get_settings, get_engine
import settings

from sqlalchemy import create_engine
from sqlalchemy import select, and_, or_, func, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.url import URL
from model import *

SETTINGS = get_settings(settings)
engine = get_engine(SETTINGS)
Session = sessionmaker(bind=engine)
session = Session()
#  from IPython import embed;embed()
#  column = Record.id
#  q = session.query(column, func.row_number().over(order_by=column).label('rownum')).from_self(column)
#  record = Record.__table__
#  windowsize = 100
#  select_s = select([record.c.id, func.row_number().over(order_by=record.c.id)]).where(text("rownum %% %d=1" % windowsize))

#  dictionary = Dictionary.__table__
#  insert_s = dictionary.insert().prefix_with('IGNORE')
#  urltype_dict = SETTINGS['URLTYPE_DICT']
#  insert_v1 = [{'category':'urltype', 'key':key, 'value':value }for key,value in urltype_dict.items()]
#  evilclass_dict = SETTINGS['EVILCLASS_DICT']
#  insert_v2 = [{'category':'evilclass', 'key':key, 'value':value }for key,value in evilclass_dict.items()]
#  eviltype_dict = SETTINGS['EVILTYPE_DICT']
#  insert_v3 = [{'category':'eviltype', 'key':key, 'value':value }for key,value in eviltype_dict.items()]
#  engine.execute(insert_s, insert_v1)
#  engine.execute(insert_s, insert_v2)
#  engine.execute(insert_s, insert_v3)

record = Record.__table__
content = Content.__table__
hlj = Hlj.__table__
import pdb; pdb.set_trace()  # XXX BREAKPOINT
#  select_s = select([record.c.dname, record.c.id]).select_from(record.join(hlj, record.c.dname==hlj.c.dname)).where(record.c.evilclass==5).order_by(hlj.c.parse_count.desc()).limit(1200)
