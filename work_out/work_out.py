# -*-coding:utf8-*-
from flask import Flask, render_template
from flask import abort
from flask import redirect
from db import db_api
from flask import request
from flask import make_response,Response
import json

app = Flask(__name__)

@app.route('/')
def index():
    users = []
    all_users = db_api.search('user')
    for user in all_users:
        users.append({'url': '/user/' + str(user['ID']), 'name': user['name']})
    return render_template('index.html', users=users, page='1')

@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        datax = request.form.to_dict()
        content = str(datax)
        resp = Response(content)
        users = []
        all_users = db_api.search('user')
        for user in all_users:
            users.append({'url': '/user/' + str(user['ID']), 'name': user['name']})
        return render_template('index.html', users=users, page='1')

    else:
        content = json.dumps({"error_code":"1001"})
        resp = Response(content)
        return resp



# @app.route('/create_user/<name>/<gender>/<age>')
# def create_user(name, gender, age):
#     user_id = db_api.insert('user', {'name': name, 'age': age, 'gender': gender})
#     user = db_api.search('user', [('id', '=', user_id)])[0]
#     parts = db_api.search('part', [('user', '=', user_id)])
#     parts_list = []
#     for part in parts:
#         parts_list.append(part)
#     return render_template('index.html', parts=parts_list, user=user, page='2')

@app.route('/user/<user_id>')
def users(user_id):
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
    app.run(debug=True, port=8888)