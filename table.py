# -*-coding:utf8-*-
from db import db_api, fields


class table:
    _name = 'people'
    sql_str_list = [
        fields.char('name', required=True),
        fields.integer('age'),
    ]


db_api.create_table(table())