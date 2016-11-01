import sys
sys.path.append('../')

import pandas as pd
import re
import os
import shutil
import logging
import logging.config
import pyinotify

#  from .watchdirectory import LogEventHandler
from api.watchdirectory import LogEventHandler
#  from watchdirectory import LogEventHandler
from model import Record

class MyEventHandler(LogEventHandler):

    def __init__(self, settings, engine):
        super(MyEventHandler, self).__init__()
        self.settings = settings
        self.engine = engine
        self.ptn_long = re.compile(r'\w{6,}\d\w{6,}')
        self.df_sld_wl = pd.read_sql_table('t_sld_white_list', self.engine, index_col='id')
        #  self.df_sld_wl['dname'] = Series(['.']*len(self.df_sld_wl)).str.cat(self.df_sld_wl['dname'], sep='')

    def _move_log(self, file_path, dst):
        dst_path = os.path.join(dst, os.path.basename(file_path))
        shutil.move(file_path, dst_path)
        self.logger.info("Move the file %s to %s" % (file_path, dst))

    def _check_file(self, event):
        """检查文件是否为csv文件，如果检查通过，返回文件名和分隔符

        @param event: pyinotify定义的文件夹变动事件
        @type  event: event

        @return file_path: 导入文件夹的文件路径
        @rtype : String

        @return sep: csv文件的分隔符
        @rtype : String

        """

        file_path = os.path.join(event.path,event.name)
        if file_path.split('.')[-1] != 'csv':
            self.logger.info('Please put a csv file')
            self._move_log(file_path, self.settings['DPC_DIR'])
            return None, None
        else:
            with open(file_path, 'r') as f:
                first_line = f.readline()
            if ',' in first_line:
                sep = ','
            elif '\t' in first_line:
                sep = '\t'
            else:
                self.logger.info('Can not detect separator')
                self._move_log(file_path, self.settings['DPC_DIR'])
                return None, None
            return file_path, sep

    def _update_sld_wl(self):
        result = self.engine.execute('select updated_at from t_sld_white_list order by updated_at desc limit 1')
        last_update_time = result.first()[0]
        if self.df_sld_wl['updated_at'].max() < last_update_time:
            self.df_sld_wl = pd.read_sql_table('t_sld_white_list', self.engine, index_col='id')
            #  self.df_sld_wl['dname'] = Series(['.']*len(self.df_sld_wl)).str.cat(self.df_sld_wl['dname'], sep='')

    #  def _filter(self, s):
        #  s = s[~s.str.contains(self.ptn_long)]
        #  tmp_s = s.map(lambda x:'.'.join(x.split('.')[-2:]))
        #  s = s[~tmp_s.isin(self.df_sld_wl['dname'])]
        #  s = s[s.notnull()]
        #  return s

    def _filter(self, df):
        df = df[~df[0].str.contains(self.ptn_long)]
        tmp_s = df[0].map(lambda x:'.'.join(x.split('.')[-2:]))
        df = df[~tmp_s.isin(self.df_sld_wl['dname'])]
        df = df[df[0].notnull()]
        return df

    def process_main(self, event):
        file_path, sep = self._check_file(event)
        file_name = os.path.basename(file_path).split('.')[0]
        if file_path:
            self._update_sld_wl()
            try:
                chunksize = 5000
                chunks = pd.read_csv(file_path, chunksize=chunksize, header=None, quotechar='"',sep=sep, na_values = ['na', '-', '.', ''])
                for chunk in chunks:
                    df = self._filter(chunk)
                    if not df.empty:
                        insert_values = [ {'dname':tmp, 'source':0} for tmp in df[0] ]
                        self.engine.execute(Record.__table__.insert().prefix_with('IGNORE'), insert_values)
                        if file_name != Record.__tablename__:
                            df = df[df.columns[[0, -1]]]
                            df = df.rename(index=str, columns={0:'dname', df.columns[-1]:'parse_count'})
                            df.to_sql(file_name, self.engine, index=False, if_exists='append')
                self._move_log(file_path, self.settings['HST_DIR'])
                self.logger.info('Successfully processed the file %s' % file_path)
            except Exception as e:
                self.logger.info('Some error occurred')
                self._move_log(file_path, self.settings['DPC_DIR'])
                self.logger.info('%s' % e)

    def process_IN_CLOSE_WRITE(self, event):
        super(MyEventHandler, self).process_IN_CLOSE_WRITE(event)
        self.process_main(event)

    def process_IN_MOVED_TO(self, event):
        super(MyEventHandler, self).process_IN_MOVED_TO(event)
        self.process_main(event)

def run(settings, engine):
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    SETTINGS = settings
    handler = MyEventHandler(SETTINGS, engine)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO
    wm.add_watch(SETTINGS['WK_DIR'], mask, rec=True)
    logger.info('Start Watching directory %s' % SETTINGS['WK_DIR'])
    notifier.loop()

def main():
    from utils import get_settings, get_engine
    import settings
    SETTINGS = get_settings(settings)
    engine = get_engine(SETTINGS)
    logging.basicConfig(level=logging.DEBUG)
    run(SETTINGS, engine)

if __name__ == '__main__':
    main()

