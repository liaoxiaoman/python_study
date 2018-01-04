# -*-coding:utf8-*-
from flask import Flask, render_template
from flask import abort
from flask import redirect
from db import db_api
from flask import request
from flask import make_response,Response
import json
import random

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

@app.route('/create_part/<user_id>/<name>')
def create_part(user_id, name):
    part_id = db_api.insert('part', {'user': user_id, 'name': name})
    part = db_api.search('part', [('id', '=', part_id)])[0]
    items = db_api.search('item', [('part', '=', part_id)])
    items_list = []
    for item in items:
        items_list.append(item)
    return render_template('index.html', items=items_list, part=part, page='3')

@app.route('/part/<part_id>')
def parts(part_id):
    part = db_api.search('part', [('id', '=', part_id)])[0]
    items = db_api.search('item', [('part', '=', part_id)])
    items_list = []
    for item in items:
        items_list.append(item)
    return render_template('index.html', items=items_list, part=part, page='3')

@app.route('/create_item/<part_id>/<name>')
def create_item(part_id, name):
    item_id = db_api.insert('item', {'part': part_id, 'name': name})
    part = db_api.search('part', [('id', '=', part_id)])[0]
    items = db_api.search('item', [('part', '=', part_id)])
    items_list = []
    for item in items:
        items_list.append(item)
    return render_template('index.html', items=items_list, part=part, page='3')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8888)