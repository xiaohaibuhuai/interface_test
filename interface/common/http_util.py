import requests
import readConfig as readConfig
from common.log import MyLog as Log
localReadConfig = readConfig.ReadConfig()

class HttpUtils:
    def __init__(self,model):
        global host, port, timeout
        host = None
        try:
            host = localReadConfig.get_http(model)
        except Exception :
            host = localReadConfig.get_http("default_base_url")

        port = None

        try:
            port = localReadConfig.get_port(model)
        except Exception :
            port = localReadConfig.get_port("default_port")
        timeout = None
        try:
            timeout = localReadConfig.get_time_out(model)
        except Exception :
            timeout = localReadConfig.get_time_out("default_timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.__headers = {}
        self.__params = {}
        self.__data = {}
        self.__url = None
        self.__files = {}

    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self, url):
        if port is None or port is '':
            self.__url = host  + url
        else:
            self.__url = host + ":" + str(port) + url
    @property
    def headers(self):
        return self.__headers
    @headers.setter
    def headers(self, header):
        self.__headers.update(header)

    @property
    def params(self):
        return self.__params
    @params.setter
    def params(self, param):
        self.__params.update(param)

    # def set_data(self, data):
    #     self.data = data

    @property
    def files(self):
        return self.__files
    @files.setter
    def set_files(self, file):
        self.__files = file

    # defined http get method
    def get(self):
        try:
            response = requests.get(self.__url, params=self.__params, headers=self.__headers, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    def post(self):
        try:
            # response = Request(url=self.__url,headers=self.__headers,cookies=None,method='POST',)
            response = requests.post(self.__url, headers=self.__headers, json=self.__params, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except Exception as te:
            self.logger.exception(te,exc_info=True)
            self.logger.error("Time out!")
            return None
