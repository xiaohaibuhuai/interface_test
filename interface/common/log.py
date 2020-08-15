import logging
from datetime import datetime
import threading
import logging
from datetime import datetime
import threading
import os
import readConfig

global logPath, resultPath, proDir
proDir = readConfig.proDir
class Log:
    def __init__(self):
        resultPath = os.path.join(proDir, "result")
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s[%(funcName)s,line:%(lineno)d] - %(levelname)s:  %(message)s')
        # create result file if it doesn't exist
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        # defined test result file name by localtime
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d")))
        # create test result file if it doesn't exist
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # defined logger
        self.logger = logging.getLogger(__name__)
        # defined log level
        self.logger.setLevel(logging.INFO)

        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        # defined formatter
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        # add handler
        self.logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        self.logger.addHandler(console)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()
        return MyLog.log