# -*-coding:utf8-*-
from db import db_api

# db_api.insert('people2', {'name': 'liaoxiaoman', 'age': 25})
result = db_api.search('people2')
pass