# -*- coding: utf-8 -*-

import time
try:
    import json
except ImportError as e:
    import simplejson as json

from .request import McanRequest


class McanConf(object):
    HOST = 'https://api.meican.com'
    VERSION = 'v2.1'

    def __init__(self, **kwargs):
        must_conf = ('client_id', 'client_secret', 'username', 'password')
        for key in must_conf:
            if key not in kwargs:
                raise RuntimeError('The config param %r must be given.' % key)
        self.__appid = kwargs.get('client_id')
        self.__appsecret = kwargs.get('client_secret')
        self.__username = kwargs.get('username')
        self.__password = kwargs.get('password')

        self.__debug = kwargs.get('debug')

        self.__access_token = kwargs.get('access_token')
        self.__access_token_expires_at = kwargs.get('access_token_expires_at')
        self.__token_type = kwargs.get('token_type')

        self.__request = McanRequest(self)

    def url(self, url):
        return '%s/%s/%s' % (self.HOST, self.VERSION, url.lstrip('/'))

    def grant_access_token(self):
        resp = self.__request.get(
            self.url('/oauth/token'),
            without_token=True,
            params={
                'username': self.__username,
                'password': self.__password,
                'grant_type': 'password',
                'meican_credential_type': 'password',
            }
        )
        self.__access_token = resp['access_token']
        self.__access_token_expires_at = int(time.time()) + resp['expires_in']
        self.__token_type = resp['token_type']

        return self.__access_token

    def refresh_access_token(self):
        resp = self.__request.get(
            self.url('/oauth/token'),
            without_token=True,
            params={
                'refresh_token': self.__access_token,
                'grant_type': 'refresh',
            }
        )
        self.__access_token = resp['access_token']
        self.__access_token_expires_at = int(time.time()) + resp['expires_in']
        self.__token_type = resp['token_type']

        return self.__access_token

    @property
    def access_token(self):
        if self.__access_token:
            now = time.time()
            if self.__access_token_expires_at - now > 60:
                return self.__access_token
        else:
            return self.grant_access_token()

        return self.refresh_access_token()

    @property
    def token_type(self):
        self.access_token

        return self.__token_type

    @property
    def appid(self):
        return self.__appid

    @property
    def appsecret(self):
        return self.__appsecret

    @property
    def debug_mode(self):
        return self.__debug
