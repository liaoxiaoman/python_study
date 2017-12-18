# -*- coding:utf-8 -*-

import urllib
import urllib2
import datetime
import time
import random
import cookielib
import same
import sys
reload(sys)
sys.setdefaultencoding('utf8')
login_token = ''
cj = ''
user_id = '4484089'
last_timestamp = time.mktime(datetime.datetime.now().timetuple())

def receive_msg():
    global login_token, cj, last_timestamp
    url = 'http://im-xs.same.com/immsg/privateHistory'
    createdata = urllib.urlencode({'limit': 50, 'tid': '4484089_15528041', 'uid': user_id})
    req = urllib2.Request(url+'?'+createdata)
    req.add_header("Authorization", "Token %s"%login_token)
    req.add_header("User-Agent", "same-appstore2/800 (iPhone; iOS 11.1.2; Scale/3.00)")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    result = opener.open(req)
    text = result.read()
    print text

def send_msg(txt):
    global login_token, cj, last_timestamp
    url = 'http://im-xs.same.com/immsg/privateHistory'
    createdata = urllib.urlencode({'limit': 50, 'tid': '4484089_15528041', 'uid': user_id})
    req = urllib2.Request(url+'?'+createdata)
    req.add_header("Authorization", "Token %s"%login_token)
    req.add_header("User-Agent", "same-appstore2/800 (iPhone; iOS 11.1.2; Scale/3.00)")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    result = opener.open(req)
    text = result.read()
    print text

def start_talk():
    global login_token, cj
    if not login_token or not cj:
        login_token, cj = same.login()
    send_msg(u'要接受测验么？1.接受 2.不接受')
    receive_msg()

pass