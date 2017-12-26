# -*-coding:utf8-*-
from db import db_api, fields


class table_seq:
    _name = 'table_seq'
    no_id = True
    sql_str_list = [
        fields.char('table_name', required=True),
    ]
class table_user:
    _name = 'user'
    sql_str_list = [
        fields.char('name', required=True),
        fields.integer('age'),
        fields.char('gender'),
    ]
class table_part:
    _name = 'part'
    sql_str_list = [
        fields.char('name', required=True),
        fields.many2one('user', 'user', required=True),
    ]
class table_item:
    _name = 'item'
    sql_str_list = [
        fields.char('name', required=True),
        fields.many2one('part', 'part', required=True),
    ]

db_api.create_table(table_seq())
db_api.create_table(table_user())
db_api.create_table(table_part())
db_api.create_table(table_item())

# db_api.insert('people2', {'name': 'liaoxiaoman', 'age': 25})
# result = db_api.search('people2')
pass