import unittest,os
import common.log as Log
import types
from common.common import get_xls,my_assert
from ddt import ddt,data,unpack,file_data
from readConfig import ReadConfig
from common.common import request






@ddt(model=ReadConfig.getConfig().get_model("model"))
class Testwork(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = Log.MyLog.get_log().logger

    @file_data(ReadConfig.getConfig().get_case('test_demo'))
    @request()
    @my_assert()
    def test(self,status_code,res,*args,assert_res=None,**kwargs):
        self.log.info(res)
        # self.log.info(kwargs)
        if assert_res is not None:
            for ar in assert_res:
                if isinstance(ar,types.GeneratorType):
                    for a in ar:
                        self.log.info(a.assert_res)
                        self.log.info(a.assert_msg)
                        self.assertEqual(True,a.assert_res,a.assert_msg)

        # self.failIf(http_status in (404,400,500),"%s 服务请求失败"%(http_status))
        # assert_dic:dict = kwargs.get('assert')











if __name__ == '__main__':
    unittest.main()
    # import pandas as pd
    # pd.set_option('display.max_columns', 200)
    # pd.set_option('display.width', 2000)
    # pd.set_option('display.max_colwidth', 30)
    # print(get_xls('/Users/liweichao/workspace/sklean/test_data.xlsx'))

