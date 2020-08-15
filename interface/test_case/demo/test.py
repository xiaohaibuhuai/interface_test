from functools import wraps
def t():
    def decorate(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            print("tttttttttttt")
            return func(*args,**kwargs)
        return wrapper
    return decorate



def d():
    def decorate(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            print("ddddddddddddd")
            return func(*args,**kwargs)
        return wrapper
    return decorate

class test():
    def __init__(self):
        print("__init__")

    def __new__(cls, *args, **kwargs):
        print("__new__")
        cls.__init__(cls)

    def __call__(self, *args, **kwargs):
        print("__call__")

import common.log as Log
class AssertNode():
    def __init__(self):
        self.log = Log.MyLog.get_log().logger

class Attr(AssertNode):
    def __init__(self,assert_key,assert_value):
        super().__init__()
        self.assert_key=assert_key
        self.assert_value = assert_value
        self.log.info(assert_key)
        self.log.info(assert_value)

class Type(AssertNode):
    def __init__(self,assert_key,assert_value):
        super().__init__()
        self.assert_key=assert_key
        self.assert_value = assert_value
        self.log.info(assert_key)
        self.log.info(assert_value)
class Value(AssertNode):
    def __init__(self,assert_key,assert_value):
        super().__init__()
        self.assert_key=assert_key
        self.assert_value = assert_value
        self.log.info(assert_key)
        self.log.info(assert_value)
class AttrValueExsitTrue(Attr):
    name = "&" # 判断属性存在
    pass
import types

import time
def consetomer():
    print('服务员点餐')
    time.sleep(5)
    for i in range(5):
         cai=yield i   #接受send的传值，并向下执行，直到结束或遇到下一个yield(此时的yield会向send传回一个值)
         print('顾客开始吃第%s个菜' %cai)

def canting():
    g1=consetomer()
    print(g1.__next__())
    print('厨师准备做菜')
    for i in range(1,10):
        time.sleep(1)
        print('第%s个菜做好了' %i)
        print('第%s个好吃' %g1.send(str(i)+"_2")) #传送上一次挂起的yield并等待接受下一次yeild返回值

if __name__ == '__main__':
    canting()