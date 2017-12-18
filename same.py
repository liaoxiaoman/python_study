# -*- coding:utf-8 -*-
import urllib
import urllib2
import datetime
import time
import random
import cookielib
import sys
import os
from mutagen import File
reload(sys)
sys.setdefaultencoding('utf8')

login_token = ''
cj = ''
login_url = 'http://v2.same.com/user/login'
uptoken_url = 'http://v2.same.com/qiniu/token'
upload_pic_url = 'http://upload.qiniu.com'
test_data = {'push_token': '', 'password': '6767285lxm', 'mobile': '+86-18222930521', 'format': 'json', 'device': '2D6C406A-EC81-4CB4-7B2A7D832252'}
# channel_id = 1597837  # test
channel_id = 1600220  # teddy

# 登陆操作， 获取token和cookie
def login():
    formData = urllib.urlencode(test_data)
    req = urllib2.Request(url=login_url, data=formData)
    cj=cookielib.CookieJar()   #获取cookiejar实例
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    result = opener.open(req)
    # result = urllib2.urlopen(req)
    text = result.read().replace('true', 'True')
    result = eval(text)
    login_token = result['data']['user']['token']
    return login_token, cj

# 获取上传图片token
def get_uptoken(login_token, cj):
    req = urllib2.Request(uptoken_url)
    req.add_header("Authorization", "Token %s"%login_token)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    result = opener.open(req)
    text = result.read().replace('true', 'True')
    uptoken = eval(text)['uptoken']
    return uptoken

def createnew(login_token, cj, uptoken, txt, img=None, mp4=None):
    img_path = post_multipart(uptoken, cj, img, 'jpg') if img else ''
    video_path = post_multipart(uptoken, cj, mp4, 'mp4') if mp4 else ''
    headers = {
        'Authorization': 'Token %s' % login_token,
        'User-Agent': 'same-appstore2/800 (iPhone; iOS 11.1.2; Scale/3.00)',
    }
    url = 'http://v2.same.com/sense/create'
    if mp4:
        createdata = urllib.urlencode({'channel_id': channel_id, 'r': 12345678, 'src': img_path, 'txt': txt, 'cover_url': img_path, 'video_source_url': video_path})
    else:
        createdata = urllib.urlencode({'channel_id': channel_id, 'r': 12345678, 'src': img_path, 'txt': txt})
    req = urllib2.Request(
        url=url,
        data=createdata,
        headers=headers
    )
    try:
        result = urllib2.urlopen(req)
    # 若出错则pass
    except:
        print '下一条日期的动态，加载失败：'
    if result.msg == 'OK' and result.code == 200:
        return True
    else:
        return False

# 上传二进制文件post   multipart请求     file_b二进制文件流    type 文件类型
def post_multipart(token, cj, file_b, type):
    boundary = 'Boundary+CA4FF33141662568'
    data = []
    filename = 'andy' + str(time.mktime(datetime.datetime.now().timetuple())) + str(random.randint(0, 999999))
    if type == 'mp4':
        src = 'video/' + filename + '.mp4'
    elif type == 'jpg':
        src = 'sense/' + filename + '.jpg'
    elif type == 'mp3':
        src = 'sense/' + filename + '.mp3'
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="key"\r\n')
    data.append(src)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="token"\r\n')
    data.append(token)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="file"; filename="%s"' % src)
    data.append('Content-Type: application/octet-stream\r\n')
    data.append(file_b)
    data.append('--%s--\r\n' % boundary)
    httpBody = '\r\n'.join(data)
    req = urllib2.Request(upload_pic_url, data=httpBody)
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    result = opener.open(req)
    response = result.read()
    path = eval(response)['key']
    return path

def same_api(pic=None, txt=None, mp4=None):
    global login_token, cj
    if not login_token or not cj:
        login_token, cj = login()  # 取登录token和缓存
    uptoken = get_uptoken(login_token, cj)  # 取上传token
    result = createnew(login_token, cj, uptoken, txt, pic, mp4)
    return result

def upload_mv():
    # mp3文件目录
    file_list = os.listdir('d:/eminem')
    for file_name in file_list:
        # 取mp3封面图片和 歌手-歌名
        afile = File('d:/eminem/'+file_name)
        artwork = afile.tags._DictProxy__dict['APIC:'].data  # 封面图片
        file = open('d:/eminem/'+file_name, 'rb').read()
        try:
            txt = '%s \r\n by %s'%(file_name.split('-')[1].split('.')[0], file_name.split('-')[0])
        except:
            txt = ''
        same_api(artwork, txt, file)
upload_mv()