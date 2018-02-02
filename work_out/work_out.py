# -*-coding:utf8-*-
from flask import Flask, render_template
from flask import abort
from flask import redirect
from db import db_api
from flask import request
from flask import make_response,Response
import json
import random
import datetime, time

app = Flask(__name__)

# 登陆
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        datax = request.form.to_dict()
        user = db_api.search('user', [('name', '=', datax['name']), ('password', '=', datax['password'])])
        if not user:
            content = json.dumps({"success": False, 'data': {"reason": '用户名密码错误。'}})
            return Response(content)
        cookie = str(random.randint(1111111111,9999999999))
        db_api.update('user', user[0]['ID'], {'cookie': cookie})
        content = json.dumps({"success": True, 'data': {"uid": user[0]['ID'], 'cookie': cookie}})
        return Response(content)
    elif request.method == 'GET':
        return render_template('login.html')

# 注册
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        datax = request.values.to_dict()
        user = db_api.search('user', [('name', '=', datax['name'])])
        if user:
            content = json.dumps({"success": False, 'data': {"reason": '该用户名已经被注册了。'}})
            return Response(content)
        else:
            cookie = str(random.randint(1111111111, 9999999999))
            user_id = db_api.insert('user', {'name': datax['name'], 'password': datax['password'], 'cookie': cookie})
            content = json.dumps({'success': True, 'data': {'uid': user_id, 'cookie': cookie}})
            return Response(content)
    else:
        content = json.dumps({"success": False, 'data': {"reason": '不是post方法提交'}})
        resp = Response(content)
        return resp

# 首页
@app.route('/index')
def index():
    uid = request.cookies.get('the_work_out_uid')
    cookie = request.cookies.get('the_work_out_cookie')
    if uid and cookie:
        if not db_api.search('user', [('ID', '=', int(uid)), ('cookie', '=', cookie)]):
            return render_template('login.html')
    else:
        return render_template('login.html')
    data = request.values.to_dict()
    user_id = data['uid']
    user = db_api.search('user', [('id', '=', user_id)])[0]
    parts = db_api.search('part', [('user', '=', user_id)])
    parts_list = []
    for part in parts:
        parts_list.append(part)
    return render_template('index.html', parts=parts_list, user=user, page='2')

# 健身记录 近五天
@app.route('/work_out')
def work_out():
    data = {}
    uid = request.cookies.get('the_work_out_uid')
    if uid:
        first_page_href = '/index?uid='+uid
        data['first_page_href'] = first_page_href
    return render_template('work_out.html', data=data)

# 某日详细记录
@app.route('/get_details')
def get_details():
    datax = request.values.to_dict()
    data = {}
    uid = request.cookies.get('the_work_out_uid')
    if uid:
        first_page_href = '/index?uid='+uid
        data['first_page_href'] = first_page_href
    return render_template('details.html', data=data)

# 开始记录
@app.route('/start_record')
def start_record():
    data = {}
    uid = request.cookies.get('the_work_out_uid')
    if uid:
        first_page_href = '/index?uid='+uid
        data['first_page_href'] = first_page_href
        data['uid'] = uid
        parts = db_api.search('part', [('user', '=', uid)])
        data['parts'] = parts
    return render_template('records.html', data=data)

@app.route('/create_part', methods=['POST', 'GET'])
def create_part():
    datax = request.values.to_dict()
    db_api.insert('part', {'user': datax['user_id'], 'name': datax['name']})
    return start_record()

# 选择部位
@app.route('/select_part/<part_id>')
def select_part(part_id):
    data = {}
    uid = request.cookies.get('the_work_out_uid')
    if uid:
        first_page_href = '/index?uid='+uid
        data['first_page_href'] = first_page_href
        data['uid'] = uid
        data['part_id'] = part_id
        items = db_api.search('item', [('part', '=', part_id)])
        data['item_lists'] = items
    return render_template('parts.html', data=data)

@app.route('/create_item', methods=['POST', 'GET'])
def create_item():
    datax = request.values.to_dict()
    db_api.insert('item', {'part': datax['part_id'], 'name': datax['name']})
    return select_part(datax['part_id'])

def make_sort(ret):
    new_ret = []
    for i in ret:
        seq = 0
        for j in new_ret:
            if i['datetime'] < j['datetime']:
                break
            seq += 1
        new_ret.insert(seq, i)
    return new_ret

# 选择动作
@app.route('/select_item/<item_id>')
def select_item(item_id):
    data = {}
    uid = request.cookies.get('the_work_out_uid')
    if uid:
        first_page_href = '/index?uid='+uid
        data['first_page_href'] = first_page_href
        data['uid'] = uid
        data['item_id'] = item_id
        min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        records = db_api.search('record', [('item', '=', item_id), ('datetime', '>', time.mktime(min.timetuple())), ('datetime', '<', time.mktime(max.timetuple()))])
        if len(records) > 1:
            records = make_sort(records)
        index = 1
        total = 0.0
        for r in records:
            r['index'] = index
            total += r['total']
            index += 1
        data['record_lists'] = records
        data['total'] = total
    return render_template('items.html', data=data)

@app.route('/create_record', methods=['POST', 'GET'])
def create_record():
    datax = request.values.to_dict()
    weight = float(datax['weight'])
    count = int(datax['count'])
    now = datetime.datetime.now()
    db_api.insert('record', {'item': datax['item_id'], 'weight': weight, 'count': count, 'total': weight*count, 'datetime': time.mktime(now.timetuple())})
    return select_item(datax['item_id'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8888)