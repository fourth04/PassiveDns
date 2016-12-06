from multiprocessing import Process
import logging
import logging.config
import time
import os
import signal


from utils import get_settings, get_engine
import settings
from api import *

def term(sig_num, addtion):
    print('current pid is %s, group id is %s' % (os.getpid(), os.getpgrp()))
    os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)

def main():
    SETTINGS = get_settings(settings)
    engine = get_engine(SETTINGS)
    logger = logging.getLogger('default')
    logging.config.dictConfig(SETTINGS['LOG_CONF'])

    ps = []
    for f in (dnsresolve.run, whoisresolve.run, importfromdb.run, restserver.run):
        name = f.__module__+'.'+f.__name__
        p = Process(target=f, args=(engine,), daemon=True, name=name)
        logger.info('Run function {}'.format(name))
        ps.append(p)
    p = Process(target=importfromfile.run, args=(SETTINGS, engine,), daemon=True, name='importfromfile.run')
    logger.info('Run function {}'.format(p.name))
    ps.append(p)
    for p in ps:
        p.daemon = True
        p.start()
    signal.signal(signal.SIGTERM, term)
    while True:
        for i, p in enumerate(ps):
            if not p.is_alive():
                logger.error('{} occured error, trying to reboot it'.format(p.name))
                ps[i] = Process(target=p._target, args=p._args, daemon=p.daemon, name=p._name)
                ps[i].start()
        time.sleep(60*5)

    #  can't pickle _thread.lock objects，怀疑与sqlalchemy的pool是用线程建立的有关系
    #  from multiprocessing import Pool
    #  def err_cb(e):
        #  logger.error(e)

    #  pool = Pool(5)
    #  for f in (dnsresolve.run, whoisresolve.run, importfromdb.run, restserver.run):
        #  logger.info('Add {} process'.format(f.__module__+'.'+f.__name__))
        #  pool.apply_async(func=f, args=(engine,), error_callback=err_cb)
    #  logger.info('Add {} process'.format(importfromfile.run.__module__+'.'+importfromfile.run.__name__))
    #  pool.apply_async(func=importfromfile.run, args=(SETTINGS, engine,), error_callback=err_cb)
    #  pool.close()
    #  pool.join()
    #  logger.info('Something wronge occured')

    #  can't pickle _thread.lock objects，怀疑与sqlalchemy的pool是用线程建立的有关系
    #  from concurrent.futures import ProcessPoolExecutor
    #  def err_cb(r):
        #  logger.error(r)

    #  with ProcessPoolExecutor(10) as pool:
        #  logger.info('Run dnsresolve process')
        #  future_dns = pool.submit(dnsresolve.run, engine)
        #  future_dns.add_done_callback(err_cb)
        #  logger.info('Run importfromdb process')
        #  future_db = pool.submit(importfromdb.run, engine)
        #  future_db.add_done_callback(err_cb)
        #  logger.info('Run importfromfile process')
        #  future_file = pool.submit(importfromfile.run, SETTINGS, engine)
        #  future_file.add_done_callback(err_cb)
        #  logger.info('Run restserver process')
        #  future_server = pool.submit(restserver.run, engine)
        #  future_server.add_done_callback(err_cb)
        #  logger.info('Run whoisresolve process')
        #  future_whois = pool.submit(whoisresolve.run, engine)
        #  future_whois.add_done_callback(err_cb)

if __name__ == '__main__':
    main()
