# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import json
import re
from multiprocessing.dummy import Pool as ThreadPool
import MySQLdb
from DBUtils.PooledDB import PooledDB

import traceback
import datetime
import subprocess, shlex
from threading import Timer,Thread
import Queue

OVER_SIGNAL = object()

urltype_dict = {0:u'未知', 1:u'未知', 2:u'危险网站', 3:u'安全', 4:u'安全', u'其他':u'未知'}
evilclass_dict = {1:u'社工欺诈 （仿冒、账号钓鱼、中奖诈骗）',
                  2:u'信息诈骗 （虚假充值、虚假兼职、虚假金融投资、虚假信用卡代办、网络赌博诈骗）',
                  3:u'虚假销售 （男女保健美容减肥产品、电子产品、虚假广告、违法销售）',
                  4:u'恶意文件 （病毒文件，木马文件，恶意apk文件的下载链接以及站点，挂马网站）',
                  5:u'博彩网站 （博彩网站，在线赌博网站）',
                  6:u'色情网站 （涉嫌传播色情内容，提供色情服务的网站）',
                  7:u'风险网站 （弱类型，传播垃圾信息的网站, 如果客户端有阻断，不建议使用这个数据）',
                  8:u'非法内容 （根据法律法规不能传播的内容，主要为政治敏感内容，默认内部使用）',
                  9:u'腾讯内部使用 （不对外同步数据，外部查询不返回恶意 诱导分享、高可疑、内部打击专用类型，不对外）'}
eviltype_dict = {2:'该网站已被篡改，有QQ被盗风险',
                 3:'该空间可能发布了虚假消息',
                 4:'这可能是虚假的中奖网站',
                 5:'这可能是虚假的充值网站',
                 6:'该网站可能存在非法内容',
                 7:'这可能是欺诈网站',
                 8:'这可能是欺诈网站',
                 9:'这可能是欺诈网站',
                 10:'这可能是非法的销售网站',
                 11:'该网站可能存在恶意推广信息',
                 12:'该网页可能发布的是虚假信息',
                 13:'这可能是非法的销售网站',
                 14:'该网页可能发布的是虚假电话',
                 16:'该网站可能会骗取手机话费',
                 17:'这可能是传播病毒的假色情网站',
                 18:'该网站存在欺诈风险',
                 19:'该网站可能存在非法内容',
                 20:'该网站可能存在非法内容',
                 21:'该网站可能存在非法内容',
                 22:'该网站可能存在非法内容',
                 23:'该网站可能存在非法内容',
                 24:'该网站可能存在下载风险',
                 25:'该链接下载的文件可能存在病毒',
                 26:'该链接下载的文件可能存在病毒',
                 27:'该链接下载的文件可能存在病毒',
                 28:'漏洞网站',
                 29:'该网站是非法网站',
                 30:'这可能是欺诈网站',
                 31:'您访问的是仿冒网站',
                 32:'您访问的是仿冒网站',
                 33:'您访问的网站是仿冒网站',
                 34:'该网站是非法网站',
                 35:'您访问的是仿冒网站',
                 36:'您访问的是木马链接',
                 37:'您访问的是移动恶意传播源网址',
                 38:'您访问的是钓鱼网站',
                 39:'这可能是骗取财产的假娱乐网站',
                 40:'这可能是欺诈网站',
                 41:'该网站含有未经证实的信息',
                 42:'这可能是虚假的销售网站',
                 43:'红包欺诈',
                 44:'该网站可能存在非法内容',
                 45:'这可能是虚假的中奖网站',
                 47:'该网站可能发布虚假信息',
                 50:'您访问的网站是侵权网站',
                 52:'该网站含有未经证实的信息',
                 53:'该网站可能是虚假的兼职网站',
                 56:'该网站可能存在非法内容',
                 57:'未经证实的销售信息',
                 58:'该网站可能是虚假的兼职网站',
                 60:'您访问的是仿冒网站',
                 61:'这可能是虚假的销售网站',
                 70:'该网站可能存在非法内容',
                 71:'该网站可能存在非法内容',
                 72:'您访问的是仿冒网站',
                 74:'该网站可能含有虚假信息',
                 75:'这可能是仿冒网站',
                 76:'该网站可能存在下载风险',
                 256:'该网站可能存在非法内容',
                 258:'该网站存在非法内容',
                 512:'该网站可能存在病毒木马风险',
                 598:'该网站可能存在漏洞利用！',
                 2048:'该网站可能含有虚假广告',
                 2300:'该网站含有未经证实的信息',
                 8192:'这可能是虚假的销售网站',
                 8193:'该网站可能存在交易风险',
                 8195:'这可能是虚假的销售网站',
                 8197:'这可能是虚假的销售网站',
                 8198:'这可能是虚假的贷款网站',
                 8199:'这可能是假信用卡代办网站',
                 16384:'这可能是非法的博彩网站',
                 16385:'这可能是非法的博彩网站',
                 32768:'该网站可能销售虚假火车票',
                 65536:'这可能是传播病毒的假色情网站',
                 65537:'这可能是含病毒的假色情网站',
                 262144:'该网站可能含有虚假信息',
                 524288:'该链接下载的文件可能存在病毒',
                 524289:'这可能是传播病毒的假播放器',
                 1048577:'该网站可能存在非法内容',
                 1048578:'这可能是虚假的外挂网站',
                 1048579:'该网站可能存在非法内容',
                 2097152:'这可能是仿冒淘宝的网站',
                 4194304:'这可能是仿冒腾讯游戏的网站',
                 8388608:'该网站可能销售虚假机票',
                 16777216:'这可能是假金融证券网站',
                 16777217:'这可能是虚假金融证券网站',
                 33554432:'这可能是仿冒网站',
                 67108864:'这可能是虚假的销售网站',
                 67108866:'这可能是虚假的销售网站',
                 268435456:'该网站可能存在交易风险'}

def parse(d):
    url_attr = d.get('safe_tencent', {}).get('url_attr',[])
    tmp_d = url_attr[0] if url_attr else {}
    urltype = tmp_d.get('urltype',-99)
    evilclass = tmp_d.get('evilclass',-99)
    eviltype = tmp_d.get('eviltype',-99)
    d['urltype_result'] = urltype_dict.get(urltype, '')
    d['evilclass_result'] = evilclass_dict.get(evilclass, '')
    d['eviltype_result'] = eviltype_dict.get(eviltype, '')
    d['safe_tencent'] = json.dumps(d['safe_tencent'])
    d['urltype'] = urltype
    d['evilclass'] = evilclass
    d['eviltype'] = eviltype
    d['created_at'] = datetime.datetime.now()
    d['updated_at'] = datetime.datetime.now()
    return d

def popen_plus(d, timeout_sec=2):
    cmd = '/home/cyber/http_demo 123.151.179.168 80 140 0123456789012345 %s TEST_TENCENT rVQ25ruX3GeqQsiCJCWZHvcZaOxRdcB7' % d['dname']
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        stdout,stderr = proc.communicate()
    finally:
        timer.cancel()
    try:
        tmp = re.search(r'({"echostr.*})', stdout, re.M)
        response_body = json.loads(tmp.group(0)) if tmp else {}
        d['safe_tencent'] = response_body
    except Exception:
        d['safe_tencent'] = {}
    d = parse(d)
    return d

def tencent_check(data, n_threads):
    pool = ThreadPool(n_threads)
    try:
        results = pool.map(popen_plus, data)
        pool.close()
        pool.join()
        return results
    except Exception:
        traceback.print_exc()

def connect_mysql(pool, table_name, over_signal):
    def insert_database(q):
        while True:
            data_chunk = q.get()
            if not data_chunk is over_signal:
                conn = pool.connection()
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
                data_list = [tmp.values() for tmp in data_chunk]
                mydict = data_chunk[0]
                insert_table = table_name
                placeholders = ', '.join(['%s'] * len(mydict))
                columns = ', '.join(mydict.keys())
                insert_sql =  "REPLACE INTO %s ( %s ) VALUES ( %s )" % (insert_table, columns, placeholders)
                try:
                    print 'Ready to insert into database'
                    cursor.executemany(insert_sql, data_list)
                    conn.commit()
                    print 'Insert to database over'
                except Exception as e:
                    conn.rollback()
                    print("Error: {}".format(e))
            else:
                return
    return insert_database

def select_database(q, pool, table_name, n_rows=1000):
    conn = pool.connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    for i in xrange(0,200000,n_rows):
        select_sql = 'SELECT id,dname,parse_count FROM %s LIMIT %d,%d' % (table_name, i, i+n_rows)
        select_result = cursor.execute(select_sql)
        if select_result:
            print select_sql
            data_chunk = [row for row in cursor]
            checked_results = tencent_check(data_chunk, 20)
            print 'Tencent check over'
            q.put(checked_results)
        else:
            for i in xrange(NUM_THREAD):
                print 'Put a OVER_SIGNAL into queue'
                q.put(OVER_SIGNAL)
            break

if __name__ == '__main__':

    NUM_THREAD = 3
    q = Queue.Queue()

    SETTINGS = dict(
        DB_HOST = '10.104.243.193',
        DB_USER = 'evil',
        DB_PASSWD = 'evil^123456',
        DB_PORT = 3306,
        DB_DB = 'edd'
    )
    pool = PooledDB(
        MySQLdb,
        NUM_THREAD + 1,
        host=SETTINGS['DB_HOST'],
        user=SETTINGS['DB_USER'],
        passwd=SETTINGS['DB_PASSWD'],
        port=SETTINGS['DB_PORT'],
        db=SETTINGS['DB_DB'],
        charset='utf8'
    )
    table_name = sys.argv[1]

    t = Thread(target=select_database, args=(q,pool,table_name,1000))
    print 'Create 1 thread to select from database'
    t.start()

    insert_database = connect_mysql(pool, table_name, OVER_SIGNAL)
    thread_pool = ThreadPool(NUM_THREAD)
    print 'Create %d thread to insert into database' % NUM_THREAD
    try:
        thread_pool.map(insert_database, [q] * NUM_THREAD)
    except Exception:
        traceback.print_exc()

    thread_pool.close()
    thread_pool.join()
    t.join()
