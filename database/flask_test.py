# -*-coding:utf8-*-
from flask import Flask, render_template
from flask import abort
from flask import redirect
from db import db_api

app = Flask(__name__)

@app.route('/')
def index():
    tables = [
        {'url': 'http://www.baidu.com', 'name': 'baidu'},
        {'url': 'http://www.bilibili.com', 'name': 'bilibili'},
    ]
    all_tables = db_api.get_all_table()
    for table in all_tables:
        tables.append({'url': table[0], 'name': table[0]})
    return render_template('index.html', tables=tables)

@app.route('/<table_name>')
def rows(table_name):
    rows = []
    header = []
    all_rows = db_api.search(table_name)
    if all_rows:
        for row in all_rows:
            row_list = []
            for i in row:
                row_list.append(row[i])
            rows.append(row_list)
        for i in all_rows[0]:
            header.append(i)
    return render_template('rows.html', table_name=table_name, header=header, rows=rows)

@app.route('/user/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(404)

    return '<h1> Hello,%s </h1>' % name


if __name__ == '__main__':
    app.run(debug=True, port=8888)