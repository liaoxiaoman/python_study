# -*-coding:utf8-*-
from db import db_api, fields


class table_seq:
    _name = 'table_seq'
    no_id = True
    sql_str_list = [
        fields.char('table_name', required=True),
    ]
class table:
    _name = 'people2'
    sql_str_list = [
        fields.char('name', required=True),
        fields.integer('age'),
    ]

db_api.create_table(table_seq())
db_api.create_table(table())

# db_api.insert('people2', {'name': 'liaoxiaoman', 'age': 25})
result = db_api.search('people2')
pass