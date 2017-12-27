# -*-coding:utf8-*-
from db import db_api

users = db_api.search('user')
for u in users:
    print u
user = int(raw_input("输入用户id（输入0新建）: "))
while not user:
    name = raw_input("姓名: ")
    age = raw_input("年龄: ")
    gender = raw_input("性别: ")
    try:
        user = db_api.insert('user', {'name': name, 'age': age, 'gender': gender})
    except:
        pass
print user



parts = db_api.search('part', [('user', '=', user)])
for p in parts:
    print p
part = int(raw_input("输入部位id（输入0新建）: "))
while not part:
    name = raw_input("部位名称: ")
    try:
        part = db_api.insert('part', {'name': name, 'user': user})
    except:
        pass
print part


items = db_api.search('item', [('part', '=', part)])
for i in items:
    print i
item = int(raw_input("输入动作id（输入0新建）: "))
while not item:
    name = raw_input("动作名称: ")
    try:
        item = db_api.insert('item', {'name': name, 'part': part})
    except:
        pass
print item