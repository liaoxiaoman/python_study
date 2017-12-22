# -*-coding:utf8-*-
from db import db_api, fields


class table_seq:
    _name = 'table_seq'
    no_id = True
    sql_str_list = [
        fields.char('table_name', required=True),
    ]
class table_instagram_teddy:
    _name = 'instagram_teddy'
    sql_str_list = [
        fields.integer('date'),
        fields.char('video'),
        fields.char('pic'),
        fields.char('txt'),
    ]

db_api.create_table(table_seq())
db_api.create_table(table_instagram_teddy())