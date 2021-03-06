import unittest,os
import common.log as Log
import types
from common.common import get_xls,my_assert
from ddt import ddt,data,unpack,file_data
from readConfig import ReadConfig
from common.common import request
model = __name__
if model is '__main__':
    model = 'papi_hao_xin_qing'
@ddt(model=ReadConfig.getConfig().get_model("model"))
class PapiHaoXinQing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = Log.MyLog.get_log().logger
        cls.model=model
        # param = import_module('settings')
        # print(param)

    @file_data(ReadConfig.getConfig().get_case(model))
    @request()
    @my_assert()
    def test(self,status_code,res,*args,assert_res=None,**kwargs):
        self.log.info(res)
        self.log.info(kwargs)
        if assert_res is not None:
            for ar in assert_res:
                if isinstance(ar,types.GeneratorType):
                    for a in ar:
                        self.log.info(a.assert_res)
                        self.log.info(a.assert_msg)
                        self.assertEqual(True,a.assert_res,a.assert_msg)










# if __name__ == '__main__':
#     unittest.main()
    # import pandas as pd
    # pd.set_option('display.max_columns', 200)
    # pd.set_option('display.width', 2000)
    # pd.set_option('display.max_colwidth', 30)
    # print(get_xls('/Users/liweichao/workspace/sklean/test_data.xlsx'))

