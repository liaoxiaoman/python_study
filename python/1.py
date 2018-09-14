#!/usr/bin/python
# -*- coding: UTF-8

"""题目：有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？"""


def python_1():
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                # if i != j and i != k and j != k:
                if i != k != j:
                    print i, j, k

def python_2():
    list_num = [1, 2, 3, 4]
    list = [[i, j, k] for i in list_num for j in list_num
            for k in list_num if (i !=j and j != k and j != k)]
    print (list)

def python_3():
    lit = []
    for i in range(123, 433):
        a = i % 10
        b = (i % 100)/10
        c = (i % 1000)/100
        if a != b and a != c and b != c and 0<a<5 and 0<b<5 and 0<c<5:
            print a, b, c
            lit.append([a,b,c])
    print len(lit)

def python_4():
    list_num = ['1', '2', '3', '4']
    res = [int(i+j+k) for i in list_num for j in list_num for k in list_num if len(set(i+j+k)) == 3]
    print len(res)
    print res

from itertools import permutations
def python_5():
    l = []
    for i in permutations('1234', 3):
        print i
        l.append(''.join(i))
    print l


def f01(i):
    if i==123:
        list = [i]
        return list
    else:
        list = f01(i-1)
        if (set('567890') & set(str(i))==set()) and (len(set(str(i)))==3):
            list.append(i)
        return list
def f02():
    for i in range(123,433):
        if (set('567890') & set(str(i))==set()) and (len(set(str(i)))==3):
            yield i

def consumer():
    r = 'yield'
    while True:
        #当下边语句执行时，先执行yield r，然后consumer暂停，此时赋值运算还未进行
        #等到producer调用send()时，send()的参数作为yield r表达式的值赋给等号左边
        n = yield r #yield表达式可以接收send()发出的参数
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)   #调用consumer生成器
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)