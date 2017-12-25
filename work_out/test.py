# -*-coding:utf8-*-
from db import db_api

users = db_api.search('user')
for u in users:
    print u
user = raw_input("输入用户id（输入0新建）: ")
print user

# db_api.insert('user', {'name': 'xumingfu', 'age': 26, 'gender': 1})