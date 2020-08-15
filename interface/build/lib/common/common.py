import os
import pandas as pd
import json
import common.log as Log
from requests import Response
from readConfig import ReadConfig as config
from functools import wraps
import itertools
from common.http_util import HttpUtils

log = Log.MyLog.get_log()
logger = log.get_logger()

# 从excel文件中读取测试用例
def get_xls(xls_name, sheet_name="Sheet1"):
    if xls_name is None:
        raise ValueError("文件名不能为空")
    exists = os.path.exists(xls_name)
    if not exists:
        raise ValueError("%s 不存在"%(xls_name))
    import json
    def conv_dict(a):
        return  json.loads(a)

    case_data_df = pd.read_excel(xls_name,sheet_name=sheet_name,header=[0, 1])
    # (     'assert', 'Unnamed: 11_level_1')
    columnss = case_data_df.columns.values

    _columns = []
    multi_index = dict()
    for col in columnss:
        col_1, col_2 = col
        if not col_2.startswith('Unnamed'):
            if col_1 in multi_index:
                multi_index[col_1]["multi_columns"].append(col)
                multi_index[col_1]["new_columns"].append(col_2)
            else:
                multi_index[col_1] = {
                    "multi_columns": [col],
                    "new_columns": [col_2]
                }
        else:
            _columns.append(col_1)

    if len(multi_index) > 0:
        for key, indexs in multi_index.items():
            multi_columns = indexs.get('multi_columns')
            new_columns = indexs.get('new_columns')
            new_df = case_data_df.loc[:, multi_columns]
            new_df.columns = new_columns
            new_df = pd.Series(new_df.to_dict(orient='records')).reset_index()
            new_df.columns = ['index', key]
            case_data_df.drop(columns=multi_columns,inplace=True)
            _columns.append(key)
            case_data_df[[key]] = new_df.loc[:, [key]]
    case_data_df.columns = _columns
    if 'assert' in case_data_df.columns:
        assert_series =  case_data_df.loc[:,'assert'].apply(func=conv_dict)
        assert_series = assert_series.reset_index()
        case_data_df['assert']=assert_series['assert']
        assert_series = None
    return case_data_df

def get_csv(csv_name):
    if csv_name is None:
        raise ValueError("文件名不能为空")
    exists = os.path.exists(csv_name)
    if not exists:
        raise ValueError("%s 不存在"%(csv_name))

    case_data_df = pd.read_csv(csv_name,header=[0,1])
    columns = case_data_df.columns.values

    _columns = []
    multi_index = dict()
    for col in columns:
        col_1,col_2 = col
        if not col_2.startswith('Unnamed'):
            if col_1 in multi_index:
                multi_index[col_1]["multi_columns"].append(col)
                multi_index[col_1]["new_columns"].append(col_2)
            else:
                multi_index[col_1]={
                    "multi_columns":[col],
                    "new_columns":[col_2]
                }
        else:
            _columns.append(col_1)

    if len(multi_index)>0:
        for key,indexs in multi_index.tiems():
            multi_columns = indexs.get('multi_columns')
            new_columns = indexs.get('new_columns')
            new_df = case_data_df.loc[:,multi_columns].columns=new_columns
            new_df = pd.Series(new_df.to_dict(orient='records')).reset_index(inplace=True)
            new_df.columns=['index',key]
            case_data_df.drop(columns=multi_columns)
            _columns.append(key)
            case_data_df[[key]]=new_df.loc[:,[key]]
    case_data_df.columns = _columns
    return case_data_df

def get_json(json_name):
    if json_name is None:
        raise ValueError("文件名不能为空")
    exists = os.path.exists(json_name)
    if not exists:
        raise ValueError("%s 不存在"%(json_name))

    case_data_df = pd.read_json("%s"%(json_name),orient='records')
    case_data_df = case_data_df.loc[case_data_df.skip==False]
    return case_data_df



def logged(level,name=None,message=None):

    def decorate(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        return wrapper
    return decorate


def request():
    def decorate(func):
        @wraps(func)
        def wrapper(self,*args,**kwargs):
            try:
                kwargs = args[0].to_dict()
                m = kwargs.get(config.getConfig().request_method,config.getConfig().get_http_method())
                req = HttpUtils(self.model)
                req.url = kwargs.get('api')
                self.log.info("api:%s"%(req.url))
                req.headers.update(kwargs.get('header',{}))
                req.params.update(kwargs.get('param',{}))
                req = getattr(req,str.lower(m))
                res = req()
                status_code = res.status_code
                res = res.json()

            except Exception as e:
                logger.exception(e,exc_info=True)
                res=None

            return func(self,status_code,res,*args,**kwargs)
        return wrapper
    return decorate

def my_assert():
    def decorate(func):
        @wraps(func)
        def wrapper(self,status_code,res,*args,**kwargs):
            _assert = None
            if 'assert' in kwargs:
                _assert = kwargs.get('assert')
            assert_data = {
                'status_code':status_code,
                'assert_status_code':['&','int','=',200],
                'res':_assert,
                'assert_res':['&','dict','?','!']
            }
            res_data={
                'status_code':status_code,
                'res':res
            }
            v = AssertConstruction(assert_data=assert_data,res_data=res_data)
            assert_res = v.action(Evaluator())
            return func(self,status_code,res,*args,assert_res=assert_res,**kwargs)
        return wrapper
    return decorate



class AssertNode():
    def __init__(self):
        self.logger = Log.MyLog.get_log().logger

class Attr(AssertNode):
    def __init__(self,assert_key,assert_value):
        super().__init__()
        self.assert_key=assert_key
        self.assert_value = assert_value
        self.logger.info("assert_key:   %s"%assert_key)
        if isinstance(assert_value,dict):

            self.logger.info("assert_value: %s" % json.dumps(assert_value, sort_keys=True, indent=4, separators=(',', ':')))
        elif isinstance(assert_value,list):
            self.logger.info("assert_value: %s" % json.dumps(assert_value, sort_keys=True, indent=4, separators=(',', ':')))
        else:
            self.logger.info("assert_value: %s"%assert_value)
    @staticmethod
    def buildAttr(condition,assert_key,assert_value):
        if condition[0] == AttrValueExsitTrue.name:
            return AttrValueExsitTrue(assert_key,assert_value)
        elif condition[0] == AttrValueExsitFalse.name:
            return AttrValueExsitFalse(assert_key,assert_value)
        elif condition[0] == AttrValueExsitNull.name:
            return AttrValueExsitNull(assert_key,assert_value)
        else:
            raise ValueError('属性操作符不存在%s'%(condition[0]))

class Type(AssertNode):
    def __init__(self,assert_key,assert_value):
        super().__init__()
        self.assert_key=assert_key
        self.assert_value = assert_value

    @staticmethod
    def buildType(condition, assert_key, assert_value):
        if condition[1] == TypeStr.name:
            return TypeStr(assert_key,assert_value)
        elif condition[1] == TypeInt.name:
            return TypeInt(assert_key,assert_value)
        elif condition[1] == TypeBool.name:
            return TypeBool(assert_key,assert_value)
        elif condition[1] == TypeList.name:
            return TypeList(assert_key,assert_value)
        elif condition[1] == TypeDict.name:
            return TypeDict(assert_key,assert_value)
        else:
            raise ValueError('类型操作符不存在%s'%(condition[1]))
class Value(AssertNode):
    def __init__(self,assert_key,expect_value,practical_value):
        super().__init__()
        self.assert_key=assert_key
        self.expect_value = expect_value
        self.practical_value = practical_value

    @staticmethod
    def buildValue(condition, assert_key, assert_value):
        if condition[2] == ValueEq.name:
            return ValueEq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueNeq.name:
            return ValueNeq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLt.name:
            return ValueLt(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLtEq.name:
            return ValueLtEq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueGt.name:
            return ValueGt(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueGtEq.name:
            return ValueGtEq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueIn.name:
            return ValueIn(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLenEq.name:
            return ValueLenEq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLenNeq.name:
            return ValueLenNeq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLenLt.name:
            return ValueLenLt(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLenLtEq.name:
            return ValueLenLtEq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLenGt.name:
            return ValueLenGt(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLenGtEq.name:
            return ValueLenGtEq(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueLenIn.name:
            return ValueLenIn(assert_key=assert_key,expect_value=condition[3],practical_value=assert_value)
        elif condition[2] == ValueNull.name:
            return ValueNull(assert_key=assert_key, expect_value=condition[3], practical_value=assert_value)
        else:
            raise ValueError('值操作符不存在%s'%(condition[2]))
        # logger.info("logger")
class AttrValueExsitTrue(Attr):
    name = "&" # 判断属性存在
    pass
class AttrValueExsitFalse(Attr):
    name = "!" # 判断属性不存在
    pass
class AttrValueExsitNull(Attr):
    name = "?" # 不做任何处理
    pass

class TypeDict(Type):
    name = 'dict' # 判断数据类型为字典
    pass

class TypeStr(Type):
    name = 'str'  # 判断数据类型为字符串
    pass


class TypeNull(Type):
    name = '?'  # 不多判断
    pass

class TypeList(Type):
    name = 'list'  # 判断数据类型为数组
    pass

class TypeBool(Type):
    name = 'bool'  # 判断数据类型为Bool
    pass
class TypeInt(Type):
    name = 'int'  # 判断数据类型为int
    pass

class ValueNull(Value):
    name = '?'  # 等于
    pass

class ValueEq(Value):
    name = '='  # 等于
    pass
class ValueGt(Value):
    name = '>'  # 大于
    pass
class ValueGtEq(Value):
    name = '>='  # 大于等于
    pass
class ValueLt(Value):
    name = '<'  # 小于
    pass
class ValueLtEq(Value):
    name = '<='  # 小于等于
    pass
class ValueNeq(Value):
    name = '<>'  # 不等于
    pass
class ValueIn(Value):
    name = 'in'  # in
    pass
class ValueLenEq(Value):
    name = 'len.='  # 判断数据长度
    pass
class ValueLenGt(Value):
    name = 'len.>'  # 大于
    pass
class ValueLenGtEq(Value):
    name = 'len.>='  # 大于等于
    pass
class ValueLenLt(Value):
    name = 'len.<'  # 小于
    pass
class ValueLenLtEq(Value):
    name = 'len.<='  # 小于等于
    pass
class ValueLenNeq(Value):
    name = 'len.<>'  # 不等于
    pass
class ValueLenIn(Value):
    name = 'len.in'  # in
    pass

class AssertRes():
    def __init__(self,assert_res,assert_msg):
        self.__assert_res = assert_res
        self.__assert_msg = assert_msg

    @property
    def assert_res(self):
        return self.__assert_res

    @assert_res.setter
    def assert_res(self,assert_res):
        self.__assert_res = assert_res

    @property
    def assert_msg(self):
        return self.__assert_msg

    @assert_msg.setter
    def assert_msg(self, assert_msg):
        self.__assert_msg = assert_msg






class AssertConstruction():

    def __init__(self,assert_data,res_data):
        self.log = Log.MyLog.get_log().get_logger()
        self.__assert_stack = []
        self.__stack = [(assert_data, res_data)]
        while self.__stack.__len__() > 0:
            try:
                r = self.__stack.pop()
                _assert_data, _res_data = r
                if _assert_data is not None:
                    if isinstance(_assert_data, dict):
                        for key, value in _assert_data.items():
                            if not key.startswith('assert'):
                                assert_key = 'assert_%s' % (key)
                                assert_value = None
                                if assert_key in _assert_data:
                                    condition = _assert_data.get(assert_key)
                                    if _res_data is None:
                                        assert_value = _res_data
                                    elif key in _res_data:
                                        assert_value = _res_data.get(key)
                                    self.__assert_stack.append(Attr.buildAttr(condition, key, assert_value))
                                    self.__assert_stack.append(Type.buildType(condition, key, assert_value))
                                    self.__assert_stack.append(Value.buildValue(condition, key, assert_value))
                                if value is not None:
                                    if isinstance(value,dict):
                                        self.__stack.append((value, assert_value))
                                    elif isinstance(value,list):
                                        self.__stack.append((value, assert_value))
                                    else:
                                        pass
                    elif isinstance(_assert_data, list):
                        if not isinstance(_res_data,list):
                            _res_data  = [_res_data]
                        for item in itertools.product(_assert_data,_res_data):
                            self.__stack.append(item)

            except ValueError as ve:
                self.log.exception(ve,exc_info=True)




    def action(self, visitor):
        for node in self.__assert_stack:
            yield self._visit(visitor,node)

    def _visit(self,visitor, node):
        methname = 'operate_' + type(node).__name__
        meth = getattr(visitor, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('no {} method'.format('operate_'+type(node).__name__))

    # @property
    # def assert_stack(self):
    #     return self.__assert_stack
    # @assert_stack.setter
    # def assert_stack(self,assert_stack):
    #     self.__assert_stack = assert_stack

class AssertVisitor():
    pass

class Evaluator(AssertVisitor):
    def operate_AttrValueExsitTrue(self,node:AttrValueExsitTrue):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望属性值:%s,实际值:%s"
        if node.assert_value is None:
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, "不为空",node.assert_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, "不为空", node.assert_value)

        yield AssertRes(assert_res,assert_msg)

    def operate_AttrValueExsitFalse(self, node: AttrValueExsitFalse):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望属性值:%s,实际值:%s"
        if node.assert_value is not None:
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, "不存在",node.assert_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, "不存在",node.assert_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_AttrValueExsitNull(self, node: AttrValueExsitNull):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望属性值:%s,实际值:%s"
        assert_msg = assert_msg % (
            node.name, node.assert_key, "Attr不做断言", "Attr不做断言")
        yield AssertRes(assert_res, assert_msg)


    def operate_TypeDict(self, node: TypeDict):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望类型:%s,实际类型:%s"
        if not isinstance(node.assert_value,dict):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Dict", type(node.assert_value))
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Dict", type(node.assert_value))
        yield AssertRes(assert_res, assert_msg)

    def operate_TypeList(self, node:TypeList):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望类型:%s,实际类型:%s"
        if not isinstance(node.assert_value, list):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, "List", type(node.assert_value))
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, "List", type(node.assert_value))
        yield AssertRes(assert_res, assert_msg)

    def operate_TypeBool(self, node: TypeBool):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望类型:%s,实际类型:%s"
        if not isinstance(node.assert_value, bool):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Bool", type(node.assert_value))
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Bool", type(node.assert_value))
        yield AssertRes(assert_res, assert_msg)

    def operate_TypeInt(self, node: TypeInt):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望类型:%s,实际类型:%s"
        if not isinstance(node.assert_value, int):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Int", type(node.assert_value))
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Int", type(node.assert_value))
        yield AssertRes(assert_res, assert_msg)

    def operate_TypeStr(self, node: TypeStr):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望类型:%s,实际类型:%s"
        if not isinstance(node.assert_value, str):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Str", type(node.assert_value))
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, "Str", type(node.assert_value))
        yield AssertRes(assert_res, assert_msg)

    def operate_TypeNull(self, node: TypeStr):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望类型:%s,实际类型:%s"
        assert_msg = assert_msg % (
            node.name, node.assert_key, "Type不做断言","Type不做断言")

        yield AssertRes(assert_res, assert_msg)

    def operate_ValueEq(self, node: ValueEq):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if node.expect_value is node.practical_value:
            assert_res = True
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value,node.practical_value)
        elif node.expect_value == node.practical_value:
            assert_res = True
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueGt(self, node: ValueGt):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (node.practical_value > node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueGtEq(self, node: ValueGtEq):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (node.practical_value >= node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueLt(self, node: ValueLt):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (node.practical_value < node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueLtEq(self, node: ValueLtEq):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (node.practical_value <= node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueNeq(self, node: ValueNeq):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (node.practical_value == node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueIn(self, node: ValueIn):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (node.practical_value in node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueLenEq(self, node: ValueLenEq):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (len(node.practical_value) == node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueLenGt(self, node: ValueLenGt):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (len(node.practical_value) > node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueLenGtEq(self, node: ValueLenGtEq):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (len(node.practical_value) >= node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueLenLt(self, node: ValueLenLt):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (len(node.practical_value) < node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueLenLtEq(self, node: ValueLenLtEq):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (len(node.practical_value) <= node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)


    def operate_ValueLenIn(self, node: ValueLenIn):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"
        if not (len(node.practical_value) in node.expect_value):
            assert_res = False
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        else:
            assert_msg = assert_msg % (
                node.name, node.assert_key, node.expect_value, node.practical_value)
        yield AssertRes(assert_res, assert_msg)

    def operate_ValueNull(self, node: ValueNull):
        assert_res = True
        assert_msg = "操作符:%s,断言key:%s,期望值:%s,实际值:%s"

        assert_msg = assert_msg % (
            node.name, node.assert_key, "Value不做断言", "Value不做断言")

        yield AssertRes(assert_res, assert_msg)
