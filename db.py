# -*-coding:utf8-*-

import sqlite3

class fields:
    def char(self, field=None, required=False):
        res = ',%s TEXT'%field
        if required == True:
            res += ' NOT NULL'
        return res
    def integer(self, field=None, required=False):
        res = ',%s INT'%field
        if required == True:
            res += ' NOT NULL'
        return res
class db_api:

    def __init__(self):
        self.db = 'test.db'

    def create_table(self, table):
        conn = sqlite3.connect(self.db)
        exist_c = conn.cursor()
        for row in exist_c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"):
            if table._name == row[0]:
                print 'database %s existed' % table._name
                return False
        c = conn.cursor()
        sql_str = "CREATE TABLE " + table._name + "(ID INT PRIMARY KEY NOT NULL"
        for f in table.sql_str_list:
            sql_str += f
        sql_str += ");"
        c.execute(sql_str)
        print "Table created successfully";
        conn.commit()
        conn.close()
        return True

db_api = db_api()
fields = fields()
