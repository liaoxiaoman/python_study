# -*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree
reload(sys)
sys.setdefaultencoding( "utf-8" )
def runwb(user_id):
    cookie = {"Cookie": "SCF=AvGjyXYN1TIrvfxyIxruiJiwOs9xkBALpTGrdYJ9nK0NK-ObN5pv5oeg2dUtWUmrqtofBKy4FFsAJkplPW3Dkug.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFw6oxqZJ7qkzmT_IaN0wyP5JpX5K-hUgL.Fo-0Soz41K2pSKB2dJLoI0YLxKML1h.LBo.LxKBLBo.L1hnLxKML1-2L1hBLxKqL1hML1KzLxKML1K.L12eLxKqLB.zL1-2LxK-LB.eL1h5t; _T_WM=0736b708ef0f7bf08963db14e8325010; H5_INDEX=3; H5_INDEX_TITLE=%E7%89%B9%E4%B9%88%E7%9A%84%E6%87%92%E7%99%8C%E6%BB%9A%E5%BC%80; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26fid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D10000011; SUB=_2A253DhEeDeRhGeNN7VAY-S_NzjiIHXVU8L9WrDV6PUJbkdANLVD2kW1vPIRO7Zm2XIkBCBtyFhiansp-Tw..; SUHB=0OMkcKYBWDBAbQ; SSOLoginState=1510629740"}
    url = 'http://weibo.cn/u/%d?filter=0&page=1' % user_id

    html = requests.get(url, cookies=cookie).content
    selector = etree.HTML(html)
    pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

    result = ""
    urllist_set = set()
    word_count = 1
    image_count = 1

    print u'爬虫准备就绪...'

    for page in range(1, pageNum + 1):

        # 获取lxml页面
        url = 'http://weibo.cn/u/%d?filter=0&page=%d' % (user_id, page)
        lxml = requests.get(url, cookies=cookie).content

        # 文字爬取
        selector = etree.HTML(lxml)
        content = selector.xpath('//span[@class="ctt"]')
        for each in content:
            text = each.xpath('string(.)')
            if word_count >= 4:
                text = "%d :" % (word_count - 3) + text + "\n\n"
            else:
                text = text + "\n\n"
            result = result + text
            word_count += 1

        # 图片爬取
        sys.stdout.flush()
        soup = BeautifulSoup(lxml, "lxml")
        urllist = soup.find_all('a', href=re.compile(r'^http://weibo.cn/mblog/oripic', re.I))
        urllist1 = soup.find_all('a', href=re.compile(r'^http://weibo.cn/mblog/picAll', re.I))
        first = 0
        for imgurl in urllist:
            urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)
            image_count += 1
        for imgurl_all in urllist1:
            html_content = requests.get(imgurl_all['href'], cookies=cookie).content
            soup = BeautifulSoup(html_content, "lxml")
            urllist2 = soup.find_all('a', href=re.compile(r'^/mblog/oripic', re.I))
            for imgurl in urllist2:
                imgurl['href'] = 'http://weibo.cn' + re.sub(r"amp;", '', imgurl['href'])
                urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)
                image_count += 1
            image_count -= 1

    fo = open("d:/python_study/%s.txt" % user_id, "wb")
    fo.write(result)
    word_path = "d:/python_study/%s" + '/%d' % user_id
    print u'文字微博爬取完毕'

    link = ""
    fo2 = open("d:/python_study/%s_imageurls.txt" % user_id, "wb")
    for eachlink in urllist_set:
        link = link + eachlink + "\n"
    fo2.write(link)
    print u'图片链接爬取完毕'

    if not urllist_set:
        print u'该页面中不存在图片'
    else:
        # 下载图片,保存在当前目录的pythonimg文件夹下
        image_path = "d:/python_study" + '/weibo_image'
        if os.path.exists(image_path) is False:
            os.mkdir(image_path)
        x = 1
        for imgurl in urllist_set:
            temp = image_path + '/%s.jpg' % x
            print u'正在下载第%s张图片' % x
            try:
                urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(), temp)
            except:
                print u"该图片下载失败:%s" % imgurl
            x += 1

runwb(3184748135)