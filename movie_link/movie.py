# -*- coding:utf-8 -*-
import requests
from lxml import etree
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector

res = requests.get('http://diaodiaode.me/rss/feed/28688')
sel = Selector(text="""""")

rawCont = sel.xpath("//ed2k")
for cont in rawCont:
  for nn in cont.xpath('text()').extract():
    if '1024X576' in nn:
      print nn