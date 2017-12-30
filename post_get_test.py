# -*-coding:utf8-*-
import urllib2
import urllib

url = 'http://localhost:8888/test'
createdata = urllib.urlencode({'channel_id': 1, 'r': 12345678, 'src': 2, 'txt': 3})
# 有data为post请求， 无data则为get请求。
req = urllib2.Request(
    url=url,
    data=createdata,
)
result = urllib2.urlopen(req)
res = result.read()
print res
pass