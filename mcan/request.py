# -*- coding: utf-8 -*-

import requests
import logging

from .exceptions import McanApiError


logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
fmt = logging.Formatter('%(message)s')
sh.setFormatter(fmt)
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)


class McanRequest(object):
    """
    McanRequest 请求类
    对美餐服务器的请求响应处理进行封装
    """

    HEADERS = {
        'Accept-Charset': 'utf-8',
        'Accept': 'application/json',
        'UserAgent': 'okhttp/2.7.5',
    }

    def __init__(self, conf=None):
        """
        :param conf: McanConf 配置类实例
        """
        self.__conf = conf

    @property
    def debug(self):
        """ 是否开启debug模式 """
        return self.__conf.debug_mode

    def log(self, msg):
        """ 输出调试日志 """
        if self.debug:
            logger.debug(msg)

    def request(self, method, url, without_token=False, **kwargs):
        """
        向美餐服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param without_token: 不需要token
        :param kwargs: 附加数据
        :return: 美餐服务器响应的 JSON 数据
        """
        if not without_token:
            self.HEADERS['Authorization'] = '{} {}'.format(self.__conf.token_type, self.__conf.access_token)

        if method == 'post':
            kwargs.setdefault('params', {})
            kwargs['params']['client_id'] = self.__conf.appid
            kwargs['params']['client_secret'] = self.__conf.appsecret
        elif method == 'get':
            kwargs.setdefault('data', {})
            kwargs['data']['client_id'] = self.__conf.appid
            kwargs['data']['client_secret'] = self.__conf.appsecret
        else:
            logger.warning('Undefined method {}'. format(method))
            exit(1)

        self.log('{} request {} with header {} params {}'.format(method.capitalize(), url, self.HEADERS, kwargs))
        r = requests.request(
            method=method,
            url=url,
            headers=self.HEADERS,
            **kwargs
        )
        r_json = r.json()
        self.log('Response {}'.format(r_json))
        self._check_api_error(r_json)

        return r_json

    def get(self, url, without_token=False, **kwargs):
        """
        使用 GET 方法向美餐服务器发出请求
        :param url: 请求地址
        :param without_token: 不需要token
        :param kwargs: 附加数据
        :return: 美餐服务器响应的 JSON 数据
        """
        return self.request(
            method="get",
            url=url,
            without_token=without_token,
            **kwargs
        )

    def post(self, url, without_token=False, **kwargs):
        """
        使用 POST 方法向美餐服务器发出请求
        :param url: 请求地址
        :param without_token: 不需要token
        :param kwargs: 附加数据
        :return: 美餐服务器响应的 JSON 数据
        """
        return self.request(
            method="post",
            url=url,
            without_token=without_token,
            **kwargs
        )

    def _check_api_error(self, resp):
        if 'error' in resp and 'error_description' in resp:
            raise McanApiError('%s: %s' % (resp['error'], resp['error_description']))
