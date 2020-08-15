import unittest
import common.log as _log
import time
import BeautifulReport as br
import os
from readConfig import ReadConfig as config
log = _log.MyLog.get_log().logger

def main():

    case_path = '%s/%s'%(_log.proDir,'test_case/%s'%(config.getConfig().get_case_path("path")))
    log.info("case_path:%s"%case_path)
    discover = unittest.defaultTestLoader.discover(case_path,'papi_hao_xin_qing.py')
    # discover.debug()
    # discover = unittest.TestLoader.
    now = time.strftime("%Y-%m-%d %H_%M_%S")

    report_name = now+'测试报告.html'
    log.info("report_name:%s"%(report_name))
    report_path = '%s/result/%s'%(_log.proDir,config.getConfig().get_case_path("path"))
    report_path_exists = os.path.exists(report_path)
    if not report_path_exists:
        os.makedirs(report_path)
    log.info("report_path:%s" % (report_path))
    desription = '自动化测试报告'
    log.info("desription:%s" % (desription))
    br.BeautifulReport(discover).report(filename=report_name,description=desription,log_path=report_path)


if __name__ == '__main__':
    main()