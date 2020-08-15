import os
import codecs
import configparser
import importlib
from importlib.util import find_spec
from configparser import NoOptionError
from common import log as Log
from common.singletion import Singletion
global proDir
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")

class DefaultSetting():
    attr= ['NAME','TIME_OUT','COOKIE','HEAD','BASE_URL','PORT','CASE_PATH','REPORT_PATH','METHOD','CASE_DATA_PATH']


    def __init__(self,COOKIE=None,HEAD=None,BASE_URL=None,CASE_PATH=None,REPORT_PATH=None,PORT=80):
        self.__COOKIE = dict()
        if COOKIE is not None:
            self.__COOKIE.update(COOKIE)

        self.__HEAD = dict()
        if HEAD is not None:
            self.__HEAD.update(HEAD)
        self.__BASE_URL = BASE_URL
        self.__PORT = PORT
        if CASE_PATH is not None:
            self.__CASE_PATH = CASE_PATH
        else:
            self.__CASE_PATH = proDir + "/test_file"

        if REPORT_PATH is not None:
            self.__REPORT_PATH = REPORT_PATH
        else:
            self.__REPORT_PATH = proDir + "/result"

        self.__NAME = ""
        self.__TIME_OUT = 60
        self.__METHOD = 'POST'
        self.__CASE_DATA_PATH= ''

    @property
    def METHOD(self):
        return self.__COOKIE

    @METHOD.setter
    def METHOD(self, METHOD):
        if isinstance(METHOD, str):
            self.__METHOD=METHOD
        else:
            raise TypeError("METHOD except Str")

    @property
    def CASE_DATA_PATH(self):
        return self.__CASE_DATA_PATH

    @CASE_DATA_PATH.setter
    def CASE_DATA_PATH(self, CASE_DATA_PATH):
        if isinstance(CASE_DATA_PATH, str):
            self.__CASE_DATA_PATH=CASE_DATA_PATH
        else:
            raise TypeError("CASE_DATA_PATH except Str")



    @property
    def COOKIE(self):
        return self.__COOKIE

    @COOKIE.setter
    def COOKIE(self, COOKIE):
        if isinstance(COOKIE, dict):
            self.__COOKIE.update(COOKIE)
        else:
            raise TypeError("COOKIE except dict")

    @property
    def HEAD(self):
        return self.__HEAD

    @HEAD.setter
    def HEAD(self, HEAD):
        if isinstance(HEAD, dict):
            self.__HEAD.update(HEAD)
        else:
            raise TypeError("HEAD except dict")

    @property
    def CASE_PATH(self):
        return self.__CASE_PATH

    @CASE_PATH.setter
    def CASE_PATH(self, CASE_PATH):
        if isinstance(CASE_PATH, str):
            self.__CASE_PATH = CASE_PATH
        else:
            raise TypeError("CASE_PATH except Str")

    @property
    def REPORT_PATH(self):
        return self.__REPORT_PATH

    @REPORT_PATH.setter
    def REPORT_PATH(self, REPORT_PATH):
        if isinstance(REPORT_PATH, str):
            self.__REPORT_PATH = REPORT_PATH
        else:
            raise TypeError("REPORT_PATH except Str")

    @property
    def BASE_URL(self):
        return self.__BASE_URL

    @BASE_URL.setter
    def BASE_URL(self, BASE_URL):
        if isinstance(BASE_URL, str):
            self.__BASE_URL = BASE_URL
        else:
            raise TypeError("BASE_URL except Str")

    @property
    def NAME(self):
        return self.__NAME

    @NAME.setter
    def NAME(self, NAME):
        if isinstance(NAME, str):
            self.__NAME = NAME
        else:
            raise TypeError("NAME except Str")

    @property
    def TIME_OUT(self):
        return self.__TIME_OUT

    @TIME_OUT.setter
    def TIME_OUT(self, TIME_OUT):
        if isinstance(TIME_OUT, int):
            self.__TIME_OUT=TIME_OUT
        else:
            raise TypeError("TIME_OUT except Int")

    @property
    def PORT(self):
        return self.__PORT

    @PORT.setter
    def PORT(self, PORT):
        if isinstance(PORT, int):
            self.__PORT = PORT
        else:
            raise TypeError("PORT except Int")












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
        self.case = dict()
        self.settings= dict()
        for pk in self.cf.sections():
            if pk.startswith("deploy") and pk.endswith("enable"):
                self.case.update({pk:self.cf.get(pk,"project")})
        for k,v in self.case.items():
            self.case.update({k: "test_case.%s"%(self.cf.get("settings", v))})
        for k,v in self.case.items():
            setting = importlib.import_module(v)
            attr_setting = dir(setting)
            s = DefaultSetting()
            for _attr in DefaultSetting.attr:
                if _attr in attr_setting:
                    value = getattr(setting,_attr)
                    if value is not None:
                        setattr(s,_attr,value)

            self.settings.update({v:s})






    # def get_email(self, name):
    #     value = self.cf.get("EMAIL", name)
    #     return value

    def get_http(self, name):
        for setting_key,setting_value in self.settings.items():
            if setting_value.CASE_PATH.endswith("%s.py"%(name)):
                return setting_value.BASE_URL
    def get_port(self, name):
        for setting_key,setting_value in self.settings.items():
            if setting_value.CASE_PATH.endswith("%s.py"%(name)):
                return setting_value.PORT

    def get_time_out(self, name):
        for setting_key, setting_value in self.settings.items():
            if setting_value.CASE_PATH.endswith("%s.py"%(name)):
                return setting_value.TIME_OUT

    def get_http_method(self,name):
        for setting_key, setting_value in self.settings.items():
            if setting_value.CASE_PATH.endswith("%s.py"%(name)):
                return setting_value.METHOD




    # def get_db(self, name):
    #     value = self.cf.get("DATABASE", name)
    #     return value

    def get_model(self, name):
        value = self.cf.get("MODEL", name)
        return value

    def get_cases(self):
        for setting_key,setting_value in self.settings.items():
            p,c = os.path.split(setting_value.CASE_PATH)
            yield (p,c,setting_value.REPORT_PATH,setting_value.NAME)

    def get_case(self, name,file_suffix='json'):
        value = None
        try:
            for setting_key, setting_value in self.settings.items():
                if setting_value.CASE_PATH.endswith("%s.py"%(name)):
                    value =  setting_value.CASE_DATA_PATH
                    break
        except Exception as ex:
            self.log.exception(ex)
            value = '%s/test_file/%s.%s'%(proDir,name,file_suffix)
        return value



    @property
    def request_method(self):
        return 'method'

    @staticmethod
    def getConfig():
        return ReadConfig()

if __name__ == '__main__':
    ReadConfig.getConfig()