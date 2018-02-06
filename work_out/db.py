# -*-coding:utf8-*-

import sqlite3

class fields:
    def char(self, field=None, required=False, unique=False):
        res = ',%s TEXT'%field
        if required == True:
            res += ' NOT NULL'
        return res
    def integer(self, field=None, required=False):
        res = ',%s INT'%field
        if required == True:
            res += ' NOT NULL'
        return res
    def float(self, field=None, required=False):
        res = ',%s REAL'%field
        if required == True:
            res += ' NOT NULL'
        return res
    def many2one(self, field, table, required=False):
        x = """
            ,CONSTRAINT fk_%s  
            FOREIGN KEY (%s)  
            REFERENCES %s(ID)  on delete cascade 
            """ % (field, field, table)
        res = ',%s INT'%field
        if required == True:
            res += ' NOT NULL'
        return res + x

class db_api:

    def __init__(self):
        self.db = 'test.db'

    def get_all_table(self):
        conn = sqlite3.connect(self.db)
        exist_c = conn.cursor()
        exist_c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        return exist_c.fetchall()

    def create_table(self, table):
        conn = sqlite3.connect(self.db)
        exist_c = conn.cursor()
        for row in exist_c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"):
            if table._name == row[0]:
                print 'database %s existed' % table._name
                return False
        c = conn.cursor()
        sql_str = "CREATE TABLE " + table._name + "(ID INT"
        if table._name != 'table_seq':
            sql_str += " PRIMARY KEY NOT NULL"
            c.execute("INSERT INTO table_seq (ID, table_name) VALUES (0, '%s');"%table._name)
        for f in table.sql_str_list:
            sql_str += f
        sql_str += ");"
        c.execute(sql_str)
        print "Table created successfully"
        conn.commit()
        conn.close()
        return True

    def insert(self, table, values={}):
        conn = sqlite3.connect(self.db)
        c_seq = conn.cursor()
        c_seq.execute("SELECT id FROM table_seq WHERE table_name = '%s';"%table)
        seq = c_seq.fetchall()[0][0] + 1
        c_seq.execute("update table_seq set id=%d where table_name = '%s';"%(seq, table))
        fields_str = "(id"
        values_str = "(%d"%seq
        for k in values:
            fields_str += ","+k
            values_str += ",'"+values[k].replace("'", "''")+"'" if type(values[k]) == str or type(values[k]) == unicode else ","+str(values[k]).replace("'", "''")
        fields_str += ")"
        values_str += ")"
        sql_str = "INSERT INTO " + table + " " + fields_str + " VALUES " + values_str + ";"
        c_seq.execute(sql_str)
        conn.commit()
        conn.close()
        print "Record insert successfully"
        return seq

    def search(self, table, co=[]):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("PRAGMA  table_info([%s]);"%table)
        info = c.fetchall()
        table_fields_list = []
        for i in info:
            table_fields_list.append(i[1])

        sql_str = "SELECT * FROM " + table
        if co:
            sql_str += " WHERE"
            for i in range(0, len(co)):
                if i != 0:
                    sql_str += " AND"
                v = "'%s'"%co[i][2] if type(co[i][2]) == str or type(co[i][2]) == unicode else "%s"%co[i][2]
                sql_str += " %s %s %s" % (co[i][0], co[i][1], v)

        c.execute(sql_str)
        records = c.fetchall()
        result = []
        for record in records:
            x = {}
            for i in range(0, len(table_fields_list)):
                x[table_fields_list[i]] = record[i]
            result.append(x)
        conn.close()
        return result

    def update(self, table, record_id, values):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        change_sql = ''
        for i in values:
            change_sql += " %s = '%s',"%(i, values[i])
        sql_str = "UPDATE %s SET %s WHERE ID = %d" % (table, change_sql[:-1], record_id)
        c.execute(sql_str)
        conn.commit()
        conn.close()
        print "Record update successfully"
        return True

    def delete(self, table, id):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        sql_str = "DELETE FROM %s WHERE ID = %d" % (table, int(id))
        c.execute(sql_str)
        conn.commit()
        conn.close()
        print "Record delete successfully"
        return True

db_api = db_api()
fields = fields()
