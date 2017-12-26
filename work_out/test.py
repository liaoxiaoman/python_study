# -*-coding:utf8-*-
from db import db_api

users = db_api.search('user')
for u in users:
    print u
user = int(raw_input("输入用户id（输入0新建）: "))
print user
while not user:
    name = raw_input("姓名: ")
    age = raw_input("年龄: ")
    gender = raw_input("性别: ")
    try:
        user = db_api.insert('user', {'name': name, 'age': age, 'gender': gender})
    except:
        pass

# db_api.insert('user', {'name': 'xumingfu', 'age': 26, 'gender': 1})