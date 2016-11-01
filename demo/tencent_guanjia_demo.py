#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import re
import pprint

pattern = re.compile(r'url_query\((\S+)\)')

def url_query(data, url='http://guanjia.qq.com/tapi/url_query.php'):
    r = requests.post(url, data=data)
    r.encoding='utf8'
    return r.text

#  payloads = [ {'content':'http://www.k0086.com^' + str(i)} for i in xrange(100) ]

#  url_result = []
#  for payload in payloads:
    #  url_result.append(pattern.search(url_query(payload)).group(1))
    #  url_result.append(json.loads(pattern.search(url_query(payload)).group(1)))

def main():
    data = { 'content' : sys.argv[1] + '^0' if '://' in sys.argv[1] else 'http://'+sys.argv[1]+'^0'}
    url_result = pattern.search(url_query(data)).group(1)
    url_d = json.loads(url_result)
    pprint.pprint(url_d)

if __name__ == '__main__':
    main()
