import os
import codecs
import configparser
from common import log as Log
from common.singletion import Singletion
global proDir
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")



class ReadConfig(metaclass=Singletion):

    def __init__(self):
        fd = open(configPath)
        data = fd.read()
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()
        self.log = Log.MyLog.get_log().logger
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)




    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_model(self, name):
        value = self.cf.get("MODEL", name)
        return value

    def get_case_path(self, name):
        value = self.cf.get("CASE_PATH", name)
        return value

    def get_case(self, name,file_suffix='json'):
        try:
            value = self.cf.get("CASE_PATH", name)
        except Exception as ex:
            self.log.exception(ex)
            value = '%s/test_file/%s.%s'%(proDir,name,file_suffix)
        return value

    def get_http_method(self, name='default_method'):
        try:
            value = self.cf.get("HTTP", name)
        except Exception as ex:
            self.log.exception(ex)
            value = '%s/test_file/%s.json'%(proDir,name)
        return value

    @property
    def request_method(self):
        return 'method'

    @staticmethod
    def getConfig():
        return ReadConfig()

