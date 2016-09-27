# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd
from pandas import DataFrame, Series

from datetime import datetime
import re
import os
import shutil
import logging
import pyinotify

from utils import get_settings
import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from watchdirectory import LogEventHandler
from model import Record

class MyEventHandler(LogEventHandler):

    def __init__(self, setting, engine):
        super(MyEventHandler, self).__init__
        self.setting = setting
        self.engine = engine
        self.ptn_long = re.compile(r'(?:[a-z]*[0-9]+){12,}')
        self.df_sld_wl = pd.read_sql_table('t_sld_white_list', self.engine, index_col='id')
        self.df_sld_wl['dname'] = Series(['.']*len(self.df_sld_wl)).str.cat(self.df_sld_wl['danme'], sep='')

    def _move_log(self, file_path, dst):
        shutil.move(file_path, dst)
        self.logger.info("Move the file %s to %s" % (file_path, dst))

    def _check_file(self, event):
        file_path = os.path.join(event.path,event.name)
        if file_path.split('.')[-1] != 'csv':
            self.logger.info('Please put a csv file')
            self._move_log(file_path, self.setting['DPC_DIR'])
            return
        else:
            return file_path

    def _update_sld_wl(self):
        result = self.engine.execute('select updated_at from t_sld_white_list order by updated_at desc limit 1')
        last_update_time = result.first()[0]
        if self.df_sld_wl['updated_at'].max() < last_update_time:
            self.df_sld_wl = pd.read_sql_table('t_sld_white_list', self.engine, index_col='id')
            self.df_sld_wl['dname'] = Series(['.']*len(self.df_sld_wl)).str.cat(self.df_sld_wl['danme'], sep='')

    def _filter(self, s):
        s = s[~s.str.contains(self.ptn_long)]
        s = s[~s.isin(self.df_sld_wl['dname'])]
        return s

    def process_main(self, event):
        file_path = self._check_file(event)
        self._update_sld_wl()
        try:
            chunksize = 5000
            chunks = pd.read_csv(file_path, chunksize=chunksize, header=None, quotechar='"',sep=',', na_values = ['na', '-', '.', ''])
            for chunk in chunks:
                s = self._filter(chunk[0])
                insert_values = [ {'dname':tmp} for tmp in s ]
                self.engine.execute(Record.__table__.insert().prefix_with('IGNORE'), insert_values)
            self._move_log(file_path, self.setting['HST_DIR'])
            self.logger.info('Successfully processed the file %s' % file_path)
        except Exception as e:
            self.logger.info('Some error occurred')
            self.logger.info('%s' % e)

    def process_IN_CLOSE_WRITE(self, event):
        super(LogEventHandler, self).process_IN_CLOSE_WRITE(event)
        self.process_main(event)

    def process_IN_MOVED_TO(self, event):
        super(LogEventHandler, self).process_IN_MOVED_TO(event)
        self.process_main(event)

def main():
    SETTINGS = get_settings(settings)
    db_url = URL(drivername='mysql+mysqldb', username=SETTINGS['DB_USER'], password=SETTINGS['DB_PASSWD'],
            host=SETTINGS['DB_HOST'], port=SETTINGS['DB_PORT'], database=SETTINGS['DB_DB'])
    engine = create_engine(db_url)
    handler = MyEventHandler(SETTINGS, engine)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch(SETTINGS['WK_DIR'], pyinotify.ALL_EVENTS, rec=True)

    logging.config.dictConfig(SETTINGS['LOG_CONF'])
    notifier.loop()

if __name__ == '__main__':

    main()

