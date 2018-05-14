#!/usr/bin/python
# -*- coding: UTF-8

"""题目：有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？"""


def python_1():
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                if i != j and i != k and j != k:
                    print i, j, k

def python_2():
    list_num = [1, 2, 3, 4]
    list = [[i, j, k] for i in list_num for j in list_num
            for k in list_num if (i !=j and j != k and j != k)]
    print (list)

def python_3():
    for i in range(123, 433):
        if str(i)[0] != str(i)[1] and str(i)[0] != str(i)[2] and str(i)[1] != str(i)[2]:
            print i
python_3()