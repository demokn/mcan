# -*- coding: utf-8 -*-

"""
MCan.

Cli tools for meican app.
Copyright (C) 2016 demokn <https://github.com/demokn/mcan>

Usage:
  mcan [option] [-c PATH] [-u USER] [-p PASSWD] [--appid=APPID] [--appsecret=APPSECRET] [--favourite=FAVOURITE]
  mcan (-h | --help)
  mcan --version

Options:
  -h --help                     Show this screen.
  -c PATH --config=PATH         Specifies the config file path.
  -u USER --user=USER           Specifies the meican user.
  -p PASSWD --password=PASSWD   Specifies the meican password.
  --appid=APPID                 Specifies the meican client_id.
  --appsecret=APPSECRET         Specifies the meican client_secret.
  --favourite=FAVOURITE         Specifies your favourite dishes.
  --version                     Show version.

See https://github.com/demokn/mcan for more information.

"""

from docopt import docopt
from datetime import date
from random import randint
import logging
try:
    import json
except ImportError:
    import simplejson as json

from . import __version__
from .core import McanApp
from .config import McanConf


logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
fmt = logging.Formatter('%(message)s')
sh.setFormatter(fmt)
logger.setLevel(logging.INFO)
logger.addHandler(sh)


class ConsoleFormat:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    AZURE = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    NORMAL = '\033[0m'

    @classmethod
    def black(cls, msg):
        return cls.BLACK + msg + cls.NORMAL

    @classmethod
    def red(cls, msg):
        return cls.RED + msg + cls.NORMAL

    @classmethod
    def green(cls, msg):
        return cls.GREEN + msg + cls.NORMAL

    @classmethod
    def yellow(cls, msg):
        return cls.YELLOW + msg + cls.NORMAL

    @classmethod
    def blue(cls, msg):
        return cls.BLUE + msg + cls.NORMAL

    @classmethod
    def purple(cls, msg):
        return cls.PURPLE + msg + cls.NORMAL

    @classmethod
    def azure(cls, msg):
        return cls.AZURE + msg + cls.NORMAL

    @classmethod
    def white(cls, msg):
        return cls.WHITE + msg + cls.NORMAL

    @classmethod
    def bold(cls, msg):
        return cls.BOLD + msg + cls.NORMAL


def json_decode(json_str):
    return json.loads(json_str.replace('\'', '"'))


def main():
    args = docopt(__doc__, version=__version__)

    config = {}
    if args['--config']:
        with open(args['--config']) as conf:
            config = json_decode(conf.read())
    if args['--user']:
        config['user'] = args['--user']
    if args['--password']:
        config['password'] = args['--password']
    if args['--appid']:
        config['appid'] = args['--appid']
    if args['--appsecret']:
        config['appsecret'] = args['--appsecret']
    if args['--favourite']:
        config['favourite'] = json_decode(args['--favourite'])

    if 'favourite' not in config:
        config['favourite'] = []
    if 'appid' not in config:
        config['appid'] = 'HRVmPZebY51X4mmhaKfAR2vhuISn1nR'
    if 'appsecret' not in config:
        config['appsecret'] = 'qTgaAN6h6MsKi6c76kNHUZVbujihwpd'

    conf = McanConf(
        client_id=config['appid'],
        client_secret=config['appsecret'],
        username=config['user'],
        password=config['password']
    )
    mcan = McanApp(conf)
    today = date.today().isoformat()

    logger.info(ConsoleFormat.yellow('获取用户信息...'))
    calendaritems_list = mcan.get_calendaritems_list(today, today)
    calendar_item = calendaritems_list['dateList'][0]['calendarItemList'][0]
    tab_uuid = calendar_item['userTab']['uniqueId']
    corp_addr_uuid = calendar_item['userTab']['corp']['addressList'][0]['uniqueId']
    tg_time = '{} {}'.format(today, calendar_item['openingTime']['closeTime'])

    logger.info(ConsoleFormat.yellow('获取推荐菜品...'))
    recommended_dishes = mcan.get_recommendations_dishes(tab_uuid, tg_time)
    dishes_list = recommended_dishes['othersRegularDishList']

    logger.info(ConsoleFormat.green('今日推荐:'))
    for dishes in dishes_list:
        logger.info('  ' + ConsoleFormat.white(dishes['name']))

    def select_dishes(favourite_list, dishes_list):
        for favourite in favourite_list:
            for dishes in dishes_list:
                if dishes['name'].find(favourite) != -1:
                    return dishes
        return None

    selected_dishes = select_dishes(config['favourite'], dishes_list)

    if selected_dishes is None:
        selected_dishes = dishes_list[randint(0, len(dishes_list) - 1)]
    logger.info(ConsoleFormat.green('已为您选择: ' + selected_dishes['name']))

    order_list = [{'count': 1, 'dishId': selected_dishes['id']}]
    logger.info(ConsoleFormat.yellow('正在为您下单...'))
    resp = mcan.orders_add(tab_uuid, corp_addr_uuid, tg_time, json.dumps(order_list))
    logger.info(ConsoleFormat.green('已成功下单: '))
    logger.info('  %s x %s' % (ConsoleFormat.white(selected_dishes['name']), ConsoleFormat.white(str(1))))
    logger.info('%s %s', ConsoleFormat.green('订单号:'), ConsoleFormat.red(resp['order']['uniqueId']))
