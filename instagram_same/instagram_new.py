# -*- coding:utf-8 -*-
import json
from lxml import etree
import requests
import click
import re
import time
import same
import datetime
import sys
from db import db_api
reload(sys)
sys.setdefaultencoding('utf8')

PAT = re.compile(r'queryId:"(\d*)?"', re.MULTILINE)
headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/teddysphotos/",
    "Host": "www.instagram.com",
}

BASE_URL = 'https://www.instagram.com'
USER = '/teddysphotos/'
uid = 'teddysphotos'

NEXT_URL = 'https://www.instagram.com/graphql/query/?query_id={0}&variables={1}'
jso = {"id": "", "first": 12, "after": ""}
proxy = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}
query_id = 17888483320059182   # 请求版本号，可能更新， 用get_query_id重新获取最后一条
def crawl():
    result = []
    click.echo('start')
    try:
        res = requests.get(BASE_URL+USER, headers=headers)
        html = etree.HTML(res.content)
        all_a_tags = html.xpath('//script[@type="text/javascript"]/text()')
        for a_tag in all_a_tags:
            if a_tag.strip().startswith('window'):
                data = a_tag.split('= {')[1][:-1]  # 获取json数据块
                js_data = json.loads('{' + data, encoding='utf-8')
                nodes = js_data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"]
                end_cursor = js_data["entry_data"]["ProfilePage"][0]["user"]["media"]["page_info"]["end_cursor"]
                has_next = js_data["entry_data"]["ProfilePage"][0]["user"]["media"]["page_info"]["has_next_page"]
                id = nodes[0]["owner"]["id"]
                for node in nodes:
                    click.echo(node["display_src"])
                    url_dict = {'txt': node['caption'] if 'caption' in node.keys() else '',
                                'pic':  node['display_src'] if 'display_src' in node.keys() else '',
                                'date':  node['date'] if 'date' in node.keys() else ''}
                    # ------尝试获取mp4url------
                    try:
                        mp4_url = '/p/'+node["code"]+'/?taken-by='+uid
                        res = requests.get(BASE_URL+mp4_url, headers=headers)
                        html = etree.HTML(res.content)
                        all_a_tags = html.xpath('//script[@type="text/javascript"]/text()')
                        for a_tag in all_a_tags:
                            if a_tag.strip().startswith('window'):
                                data = a_tag.split('= {')[1][:-1]  # 获取json数据块
                                js_data = json.loads('{' + data, encoding='utf-8')
                                mp4_src = js_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_url']
                                click.echo(mp4_src)
                                url_dict['video'] = mp4_src if mp4_src else ''
                    except:
                        click.echo('just picture!')
                    # ------尝试获取mp4url------
                    result.append(url_dict)

                count = 0
                # 更多的图片加载
                while has_next and count <= -1:
                    jso["id"] = id
                    jso["after"] = end_cursor
                    text = json.dumps(jso)
                    url = NEXT_URL.format(query_id, text)
                    res = requests.get(url, headers=headers)
                    time.sleep(2)
                    html = json.loads(res.content.decode(), encoding='utf-8')
                    has_next = html["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
                    end_cursor = html["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
                    edges = html["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
                    for edge in edges:
                        click.echo(edge["node"]["display_url"])
                        count += 1
                        result.append({'txt': edge["node"]['edge_media_to_caption']['edges'][0]['node']['text'] if edge["node"]['edge_media_to_caption']['edges'] else '',
                                       'pic': edge["node"]['display_url'] if 'display_url' in edge["node"].keys() else '',
                                       'date': edge["node"]['taken_at_timestamp'] if 'taken_at_timestamp' in edge["node"].keys() else ''})

                click.echo('ok')
                return result
    except Exception as e:
        raise e
def get_query_id():
    # 请求query_id
    res = requests.get(BASE_URL+USER, headers=headers)
    html = etree.HTML(res.content)
    query_id_url = html.xpath('//script[@crossorigin="anonymous"]/@src')  # query_id 作为内容加载
    click.echo(query_id_url)
    js_url = ''
    for i in query_id_url:
        if 'Common' in i:
            js_url = i
    if not js_url:
        print 'instagram 的某个common.js获取失败!!'
        return False
    query_content = requests.get(BASE_URL + js_url, headers=headers)
    query_id_list = PAT.findall(query_content.text)
    for u in query_id_list:
        click.echo(u)
    return '取最后一条作为query_id'

def make_sort(ret):
    new_ret = []
    for i in ret:
        seq = 0
        for j in new_ret:
            if i['date'] < j['date']:
                break
            seq += 1
        new_ret.insert(seq, i)
    return new_ret

if __name__ == '__main__':
    result = crawl()
    done = db_api.search('instagram_teddy')
    done_date = [j['date'] for j in done]
    ret = [i for i in result if i['date'] not in done_date]  # 将要写入的动态
    # 对ret中的元素按date排序
    if len(ret) > 1:
        ret = make_sort(ret)
    print ret
    for j in ret:
        # 下载图片并写入
        ss = requests.session()
        video = ss.get(j['video']).content if 'video' in j.keys() else None
        pic = ss.get(j['pic']).content
        txt = j['txt'] +'\r\n\r\n' + u"teddysphotos' instagram\r\n" + str(datetime.datetime.fromtimestamp(j['date']))
        result = same.same_api(pic, txt, video)
        # 成功写入same
        if result == True:
            db_api.insert('instagram_teddy', j)
            print str(datetime.datetime.fromtimestamp(j['date']))
        else:
            print '写入same失败'
            break