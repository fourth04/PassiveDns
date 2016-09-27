# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import datetime
import pyinotify
import logging

class LogEventHandler(pyinotify.ProcessEvent):

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    def __init__(self):
        self.logger.info("Starting monitor...")
        super(LogEventHandler, self).__init__()

    def process_IN_ACCESS(self, event):
        self.logger.info("ACCESS event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_ATTRIB(self, event):
        self.logger.info("ATTRIB event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_CLOSE_NOWRITE(self, event):
        self.logger.info("CLOSE_NOWRITE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_CLOSE_WRITE(self, event):
        self.logger.info("CLOSE_WRITE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_CLOSE(self, event):
        self.logger.info("CLOSE_event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_CREATE(self, event):
        self.logger.info("CREATE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_DELETE_SELF(self, event):
        self.logger.info("DELETE_SELF event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_DELETE(self, event):
        self.logger.info("DELETE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_MODIFY(self, event):
        self.logger.info("MODIFY event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_OPEN(self, event):
        self.logger.info("OPEN event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_MOVED_FROM(self, event):
        self.logger.info("MOVED_FROM event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_MOVED_TO(self, event):
        self.logger.info("MOVED_TO event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_MOVED_SELF(self, event):
        self.logger.info("MOVED_SELF event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_MOVE(self, event):
        self.logger.info("MOVE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

    def process_IN_UNMOUNT(self, event):
        self.logger.info("UNMOUNT event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

def main():
    # watch manager
    handler = LogEventHandler()
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch('./tmp', pyinotify.ALL_EVENTS, rec=True)

    notifier.loop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
