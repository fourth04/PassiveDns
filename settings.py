ENV = 'debug'

#Database settings
if ENV == 'debug':
    DB_DRIVER = 'mysql+mysqldb'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'evil'
    DB_PASSWD = 'evil^123456'
    DB_DB = 'passive_dns'
elif ENV == 'local':
    DB_DRIVER = 'mysql+mysqldb'
    DB_HOST = '10.104.243.193'
    DB_PORT = 3306
    DB_USER = 'evil'
    DB_PASSWD = 'evil^123456'
    DB_DB = 'passive_dns'


#  Monitor folder settings
WK_DIR = '/home/cyber/WorkSpace/working'
HST_DIR = '/home/cyber/WorkSpace/history'
DPC_DIR = '/home/cyber/WorkSpace/deprecated'

# logging settings
LOG_CONF = {
    'version': 1,
    'formatters': {
        'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': '../log/default.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
        'file_importfromfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': '../log/importfromfile.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
        'file_importfromdb': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': '../log/importfromdb.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
        'file_dnsresolve': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': '../log/dnsresolve.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
        'file_whoisresolve': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': '../log/whoisresolve.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
        'file_restserver': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': '../log/restserver.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
    },
    'loggers': {
        'default': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'api.watchdirectory': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_importfromfile']
        },
        'api.importfromfile': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_importfromfile']
        },
        'api.importfromdb': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_importfromdb']
        },
        'api.dnsresolve': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_dnsresolve']
        },
        'api.whoisresolve': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_whoisresolve']
        },
        'api.restserver': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_restserver']
        },
    },
    'disable_existing_loggers': False
}


URLTYPE_DICT = {0:u'未知', 1:u'未知', 2:u'危险网站', 3:u'安全', 4:u'安全', 99:u'未知'}
EVILCLASS_DICT = {0:u'未知',
                  1:u'社工欺诈 （仿冒、账号钓鱼、中奖诈骗）',
                  2:u'信息诈骗 （虚假充值、虚假兼职、虚假金融投资、虚假信用卡代办、网络赌博诈骗）',
                  3:u'虚假销售 （男女保健美容减肥产品、电子产品、虚假广告、违法销售）',
                  4:u'恶意文件 （病毒文件，木马文件，恶意apk文件的下载链接以及站点，挂马网站）',
                  5:u'博彩网站 （博彩网站，在线赌博网站）',
                  6:u'色情网站 （涉嫌传播色情内容，提供色情服务的网站）',
                  7:u'风险网站 （弱类型，传播垃圾信息的网站, 如果客户端有阻断，不建议使用这个数据）',
                  8:u'非法内容 （根据法律法规不能传播的内容，主要为政治敏感内容，默认内部使用）',
                  9:u'腾讯内部使用 （不对外同步数据，外部查询不返回恶意 诱导分享、高可疑、内部打击专用类型，不对外）'}
EVILTYPE_DICT = {2:u'该网站已被篡改，有QQ被盗风险',
                 3:u'该空间可能发布了虚假消息',
                 4:u'这可能是虚假的中奖网站',
                 5:u'这可能是虚假的充值网站',
                 6:u'该网站可能存在非法内容',
                 7:u'这可能是欺诈网站',
                 8:u'这可能是欺诈网站',
                 9:u'这可能是欺诈网站',
                 10:u'这可能是非法的销售网站',
                 11:u'该网站可能存在恶意推广信息',
                 12:u'该网页可能发布的是虚假信息',
                 13:u'这可能是非法的销售网站',
                 14:u'该网页可能发布的是虚假电话',
                 16:u'该网站可能会骗取手机话费',
                 17:u'这可能是传播病毒的假色情网站',
                 18:u'该网站存在欺诈风险',
                 19:u'该网站可能存在非法内容',
                 20:u'该网站可能存在非法内容',
                 21:u'该网站可能存在非法内容',
                 22:u'该网站可能存在非法内容',
                 23:u'该网站可能存在非法内容',
                 24:u'该网站可能存在下载风险',
                 25:u'该链接下载的文件可能存在病毒',
                 26:u'该链接下载的文件可能存在病毒',
                 27:u'该链接下载的文件可能存在病毒',
                 28:u'漏洞网站',
                 29:u'该网站是非法网站',
                 30:u'这可能是欺诈网站',
                 31:u'您访问的是仿冒网站',
                 32:u'您访问的是仿冒网站',
                 33:u'您访问的网站是仿冒网站',
                 34:u'该网站是非法网站',
                 35:u'您访问的是仿冒网站',
                 36:u'您访问的是木马链接',
                 37:u'您访问的是移动恶意传播源网址',
                 38:u'您访问的是钓鱼网站',
                 39:u'这可能是骗取财产的假娱乐网站',
                 40:u'这可能是欺诈网站',
                 41:u'该网站含有未经证实的信息',
                 42:u'这可能是虚假的销售网站',
                 43:u'红包欺诈',
                 44:u'该网站可能存在非法内容',
                 45:u'这可能是虚假的中奖网站',
                 47:u'该网站可能发布虚假信息',
                 50:u'您访问的网站是侵权网站',
                 52:u'该网站含有未经证实的信息',
                 53:u'该网站可能是虚假的兼职网站',
                 56:u'该网站可能存在非法内容',
                 57:u'未经证实的销售信息',
                 58:u'该网站可能是虚假的兼职网站',
                 60:u'您访问的是仿冒网站',
                 61:u'这可能是虚假的销售网站',
                 70:u'该网站可能存在非法内容',
                 71:u'该网站可能存在非法内容',
                 72:u'您访问的是仿冒网站',
                 74:u'该网站可能含有虚假信息',
                 75:u'这可能是仿冒网站',
                 76:u'该网站可能存在下载风险',
                 256:u'该网站可能存在非法内容',
                 258:u'该网站存在非法内容',
                 512:u'该网站可能存在病毒木马风险',
                 598:u'该网站可能存在漏洞利用！',
                 2048:u'该网站可能含有虚假广告',
                 2300:u'该网站含有未经证实的信息',
                 8192:u'这可能是虚假的销售网站',
                 8193:u'该网站可能存在交易风险',
                 8195:u'这可能是虚假的销售网站',
                 8197:u'这可能是虚假的销售网站',
                 8198:u'这可能是虚假的贷款网站',
                 8199:u'这可能是假信用卡代办网站',
                 16384:u'这可能是非法的博彩网站',
                 16385:u'这可能是非法的博彩网站',
                 32768:u'该网站可能销售虚假火车票',
                 65536:u'这可能是传播病毒的假色情网站',
                 65537:u'这可能是含病毒的假色情网站',
                 262144:u'该网站可能含有虚假信息',
                 524288:u'该链接下载的文件可能存在病毒',
                 524289:u'这可能是传播病毒的假播放器',
                 1048577:u'该网站可能存在非法内容',
                 1048578:u'这可能是虚假的外挂网站',
                 1048579:u'该网站可能存在非法内容',
                 2097152:u'这可能是仿冒淘宝的网站',
                 4194304:u'这可能是仿冒腾讯游戏的网站',
                 8388608:u'该网站可能销售虚假机票',
                 16777216:u'这可能是假金融证券网站',
                 16777217:u'这可能是虚假金融证券网站',
                 33554432:u'这可能是仿冒网站',
                 67108864:u'这可能是虚假的销售网站',
                 67108866:u'这可能是虚假的销售网站',
                 268435456:u'该网站可能存在交易风险'}
PROVINCES = [u'河北',
            u'山西',
            u'辽宁',
            u'吉林',
            u'黑龙江',
            u'江苏',
            u'浙江',
            u'安徽',
            u'福建',
            u'江西',
            u'山东',
            u'河南',
            u'湖北',
            u'湖南',
            u'广东',
            u'海南',
            u'四川',
            u'贵州',
            u'云南',
            u'陕西',
            u'甘肃',
            u'青海',
            u'台湾',
            u'北京',
            u'天津',
            u'上海',
            u'重庆',
            u'广西',
            u'内蒙古',
            u'西藏',
            u'宁夏',
            u'新疆',
            u'香港',
            u'澳门']
