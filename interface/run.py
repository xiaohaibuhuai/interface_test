import unittest
import common.log as _log
import time
import BeautifulReport as br
import os
from readConfig import ReadConfig as config
log = _log.MyLog.get_log().logger

def main():

    # case_path = '%s/%s'%(_log.proDir,'test_case/%s'%(config.getConfig().get_case_path("path")))
    # log.info("case_path:%s"%case_path)
    # discover = unittest.defaultTestLoader.discover(case_path,'papi_hao_xin_qing.py')
    # discover.debug()
    # discover = unittest.TestLoader.


    # suite = unittest.TestSuite()
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(config.get_cases()))


    # from importlib.util import find_spec
    # d = find_spec('Users.liweichao.workspace.interface_test.interface.test_case.dapi_hao_xin_qing.settings.py')

    for case_path_p,case_path_c,report_path,report_name in  config.getConfig().get_cases():
        discover = unittest.defaultTestLoader.discover(case_path_p, case_path_c)
        # discover.debug()
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        report_name = now+report_name+'测试报告.html'
        log.info("report_name:%s"%(report_name))
        report_path_exists = os.path.exists(report_path)
        if not report_path_exists:
            os.makedirs(report_path)
        log.info("report_path:%s" % (report_path))
        desription = '自动化测试报告'
        log.info("desription:%s" % (desription))
        br.BeautifulReport(discover).report(filename=report_name,description=desription,log_path=report_path)


if __name__ == '__main__':
    main()