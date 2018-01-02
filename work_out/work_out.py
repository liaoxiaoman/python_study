# -*-coding:utf8-*-
from flask import Flask, render_template
from flask import abort
from flask import redirect
from db import db_api
from flask import request
from flask import make_response,Response
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        datax = request.form.to_dict()
        user = db_api.search('user', [('name', '=', datax['name']), ('password', '=', datax['password'])])
        if not user:
            content = json.dumps({"success": False, 'data': {"reason": '用户名密码错误。'}})
            return Response(content)
        content = json.dumps({"success": True, 'data': {"uid": user[0]['ID'], 'token': 'test'}})
        return Response(content)
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        datax = request.values.to_dict()
        user = db_api.search('user', [('name', '=', datax['name'])])
        if user:
            content = json.dumps({"success": False, 'data': {"reason": 'this user is already existed.'}})
            return Response(content)
        else:
            user_id = db_api.insert('user', {'name': datax['name'], 'password': datax['password']})
            content = json.dumps({'success': True, 'data': {'user': user_id}})
            return Response(content)
    else:
        content = json.dumps({"success": False, 'data': {"reason": '不是post方法提交'}})
        resp = Response(content)
        return resp

# 首页
@app.route('/index')
def index():
    data = request.values.to_dict()
    user_id = data['uid']
    token = data['token']
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
    app.run(debug=True, port=8069)