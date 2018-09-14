#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；
利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；
20万到40万之间时，高于20万元的部分，可提成5%；
40万到60万之间时高于40万元的部分，可提成3%；
60万到100万之间时，高于60万元的部分，可提成1.5%，
高于100万元时，超过100万元的部分按1%提成，从键盘输入当月利润I，求应发放奖金总数？"""

def python_1(total):
    arr = [1000000, 600000, 400000, 200000, 100000, 0]
    rate = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
    r = 0
    for i in range(0, 6):
        if total > arr[i]:
            r += (total-arr[i]) * rate[i]
            total = arr[i]
    print r

#使用两种方式创建生成器
a=[100,60,40,20,10,0]
b=[0.01,0.015,0.03,0.05,0.075,0.1]

#生成器函数
def f(x):
    for i in range(len(a)):
        if n>a[i]:
            #生成器推导式
            c=(a[j]-a[j+1] for j in range(i,len(a)-1))
            break
    r=sum(map(lambda x,y:x*y,b[i:],[(n-a[i])]+list(c)))
    yield r*10000

k=int(input("是否继续计算奖金？是：1， 否：0\n"))
while k:
    n=int(input('请输入利润，单位(万元):'))
    print('应发奖金为:',next(f(n)),'(元)')
    print()
    k=int(input("是否继续计算奖金？是：1， 否：0\n"))
print('感谢使用，程序结束！')



# 生成器函数

"""一边循环一边计算的机制，称为生成器（Generator）"""

# 类似列表生成式的for循环创建一个generator

list = [x*x for x in range(10)]

generator = (x*x for x in range(10))

# 将generator的元素一个一个打印出来

# generator保存的是算法，每次调用next()，就计算出下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。
generator.next()

# or

for i in generator:
    print i

# 类似列表生成式的for循环无法实现的时候，还可以用函数来实现。如斐波拉契数列

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1

print fib(8)

"""generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行函数语句就返回。
而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。"""

# dict的iteritems()可以同时迭代key和value
d = {'x': 'A', 'y': 'B', 'z': 'C'}
for k, v in d.iteritems():
    print k + "=" + v

# 判断是否为 int，float，bool，complex，str(字符串)，list，dict(字典)，set，tuple
isinstance('1', int)

# 大小写转换
'Abc'.lower()
'Abc'.upper()
