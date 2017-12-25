# -*-coding:utf8-*-
from flask import Flask, render_template
from flask import abort
from flask import redirect

app = Flask(__name__)

@app.route('/')
def index():
    tables = [
        {'url': 'http://www.baidu.com', 'name': 'baidu'},
        {'url': 'http://www.bilibili.com', 'name': 'bilibili'},
    ]
    return render_template('index.html', tables=tables)



@app.route('/user/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(404)

    return '<h1> Hello,%s </h1>' % name


if __name__ == '__main__':
    app.run(debug=True, port=8888)