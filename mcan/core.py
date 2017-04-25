# -*- coding: utf-8 -*-

import io
import requests

from .request import McanRequest


class McanApp(object):
    __user = {}

    """ 美餐基本功能类 """
    def __init__(self, conf=None):
        self.__conf = conf

        self.__request = McanRequest(conf=self.__conf)

    @property
    def conf(self):
        """ 获取当前 McanConf 配置实例 """
        return self.__conf

    @conf.setter
    def conf(self, conf):
        """ 设置当前 McanConf 实例  """
        self.__conf = conf
        self.__request = McanRequest(conf=self.__conf)

    @property
    def request(self):
        """ 获取当前 McanRequest 配置实例 """
        return self.__request

    @request.setter
    def request(self, request):
        """ 设置当前 McanRequest 实例  """
        self.__request = request

    @property
    def user(self):
        """ 获取当前 USER """
        if not self.__user:
            self.__user = self.accounts_show()

        return self.__user

    def get_calendaritems_list(self, bg_date, ed_date, with_order_detail=False):
        """
{
    "startDate": "2017-03-16",
    "endDate": "2017-03-16",
    "dateList": [
        {
            "date": "2017-03-16",
            "calendarItemList": [
                {
                    "targetTime": 1489631400000,
                    "title": "钱升钱午餐",
                    "userTab": {
                        "corp": {
                            "uniqueId": "563338",
                            "useCloset": false,
                            "name": "钱升钱",
                            "namespace": "563338",
                            "priceVisible": false,
                            "showPrice": false,
                            "priceLimit": 15,
                            "priceLimitInCent": 1500,
                            "acceptCashPaymentToMeican": false,
                            "alwaysOpen": false,
                            "addressList": [
                                {
                                    "uniqueId": "9d8f231ddfba",
                                    "address": "上海市长宁区淞虹路207号明基商务广场C座2楼",
                                    "pickUpLocation": "上海市长宁区淞虹路207号明基商务广场C座2楼"
                                }
                            ],
                            "isAdmin": false
                        },
                        "latitude": null,
                        "longitude": null,
                        "name": "钱升钱",
                        "lastUsedTime": 1459908501000,
                        "uniqueId": "34a49575-bd52-4741-a6d6-9dc6e5fbf0bc"
                    },
                    "openingTime": {
                        "uniqueId": "b1ac5f168125",
                        "name": "午餐",
                        "openTime": "09:00",
                        "closeTime": "10:30",
                        "defaultAlarmTime": "10:00",
                        "postboxOpenTime": "12:30"
                    },
                    "corpOrderUser": {
                        "restaurantItemList": [
                            {
                                "uniqueId": "96662d",
                                "dishItemList": [
                                    {
                                        "dish": {
                                            "name": "皮蛋豆腐(配米饭/钱升钱专供)",
                                            "priceInCent": 1300,
                                            "priceString": "13",
                                            "originalPriceInCent": 1300,
                                            "isSection": false,
                                            "actionRequiredLevel": "NO_ACTION_REQUIRED",
                                            "actionRequiredReason": "NULL",
                                            "id": 68357157
                                        },
                                        "count": 1
                                    }
                                ]
                            }
                        ],
                        "corp": {
                            "openingTimeList": [
                                {
                                    "uniqueId": "b1ac5f168125",
                                    "name": "午餐",
                                    "openTime": "09:00",
                                    "closeTime": "10:30",
                                    "defaultAlarmTime": "10:00",
                                    "postboxOpenTime": "12:30"
                                }
                            ],
                            "hasMealPointGroup": false,
                            "mealPointList": [],
                            "alwaysOpen": false,
                            "namespace": "563338",
                            "useCloset": false,
                            "name": "钱升钱",
                            "excludedPayments": []
                        },
                        "readyToDelete": true,
                        "actionRequiredLevel": "NO_ACTION_REQUIRED",
                        "corpOrderStatus": "NEW_ORDER",
                        "showPrice": false,
                        "unpaidUserToMeicanPrice": "0.00",
                        "unpaidUserToMeicanPriceInCent": 0,
                        "paidUserToMeicanPrice": "0.00",
                        "paidUserToMeicanPriceInCent": 0,
                        "timestamp": 1489627418000,
                        "uniqueId": "7b43340d1ae0"
                    },
                    "status": "ORDER",
                    "reason": ""
                }
            ]
        }
    ]
}
        :param bg_date:
        :param ed_date:
        :param with_order_detail:
        :return:
        """
        return self.request.get(
            self.conf.url('/calendaritems/list'),
            params={
                'beginDate': bg_date,
                'endDate': ed_date,
                'withOrderDetail': 'false' if not with_order_detail else 'true',
            }
        )

    def get_recommendations_dishes(self, tab_uuid, tg_time):
        """
{
    "myRegularDishList": [
        {
            "name": "蛋骨大虾仁(配米饭/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "胖子肉蟹煲",
                "available": true,
                "uniqueId": "96662d"
            },
            "id": 68357144
        },
        {
            "name": "香辣鱼块(微辣/配米饭/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "胖子肉蟹煲",
                "available": true,
                "uniqueId": "96662d"
            },
            "id": 68357147
        }
    ],
    "othersRegularDishListSource": "TODAY_ORDER",
    "othersRegularDishList": [
        {
            "name": "鲍菇牛肉(配米饭/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "聚福园",
                "available": true,
                "uniqueId": "d4e9de"
            },
            "id": 68343337
        },
        {
            "name": "刀豆土豆(配米饭/钱升钱专供)",
            "priceInCent": 1300,
            "priceString": "13",
            "originalPriceInCent": 1300,
            "isSection": false,
            "restaurant": {
                "name": "聚福园",
                "available": true,
                "uniqueId": "d4e9de"
            },
            "id": 68343320
        },
        {
            "name": "营养套餐(配米饭&大荤&小荤&素菜/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "聚福园",
                "available": true,
                "uniqueId": "d4e9de"
            },
            "id": 68343315
        },
        {
            "name": "酸菜鱼片(配米饭/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "聚福园",
                "available": true,
                "uniqueId": "d4e9de"
            },
            "id": 68343318
        },
        {
            "name": "蒜苗腊肉(配米饭/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "聚福园",
                "available": true,
                "uniqueId": "d4e9de"
            },
            "id": 68343322
        },
        {
            "name": "小炒粉条(配米饭/钱升钱专供)",
            "priceInCent": 1300,
            "priceString": "13",
            "originalPriceInCent": 1300,
            "isSection": false,
            "restaurant": {
                "name": "胖子肉蟹煲",
                "available": true,
                "uniqueId": "96662d"
            },
            "id": 68357164
        },
        {
            "name": "黄豆芽烧牛肚(配米饭/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "胖子肉蟹煲",
                "available": true,
                "uniqueId": "96662d"
            },
            "id": 68357149
        },
        {
            "name": "皮蛋豆腐(配米饭/钱升钱专供)",
            "priceInCent": 1300,
            "priceString": "13",
            "originalPriceInCent": 1300,
            "isSection": false,
            "restaurant": {
                "name": "胖子肉蟹煲",
                "available": true,
                "uniqueId": "96662d"
            },
            "id": 68357157
        },
        {
            "name": "金针菇拌豆苗(配米饭/钱升钱专供)",
            "priceInCent": 1300,
            "priceString": "13",
            "originalPriceInCent": 1300,
            "isSection": false,
            "restaurant": {
                "name": "胖子肉蟹煲",
                "available": true,
                "uniqueId": "96662d"
            },
            "id": 68357159
        },
        {
            "name": "鸡米花(配米饭/钱升钱专供)",
            "priceInCent": 1500,
            "priceString": "15",
            "originalPriceInCent": 1500,
            "isSection": false,
            "restaurant": {
                "name": "胖子肉蟹煲",
                "available": true,
                "uniqueId": "96662d"
            },
            "id": 68357148
        }
    ],
    "showPrice": false
}
        :param tab_uuid:
        :param tg_time:
        :return:
        """
        return self.request.get(
            self.conf.url('/recommendations/dishes'),
            params={
                'tabUniqueId': tab_uuid,
                'targetTime': tg_time,
            }
        )

    def orders_add(self, tab_uuid, corp_addr_uuid, tg_time, order):
        """
{
    "message": "",
    "order": {
        "uniqueId": "7b43340d1ae0"
    },
    "status": "SUCCESSFUL"
}
        :param tab_uuid:
        :param corp_addr_uuid:
        :param tg_time:
        :param order:
        :return:
        """
        return self.request.post(
            self.conf.url('/orders/add'),
            data={
                'tabUniqueId': tab_uuid,
                'corpAddressUniqueId': corp_addr_uuid,
                'targetTime': tg_time,
                'order': order,
            }
        )

    def accounts_show(self):
        """
        {
            "username": "测试",
            "nameForShow": "test@test.com",
            "mobileAccount": {
                "mobileNumber": "12345678901",
                "verified": false
            },
            "nameForEcard": "测试",
            "emailForEcard": "t*t@t*.com",
            "balanceInCent": null,
            "uniqueId": "3a5f85dea4cd",
            "internal": false,
            "corpList": [
                {
                    "useCloset": false,
                    "namespace": "563338",
                    "excludedPayments": []
                },
                {
                    "useCloset": false,
                    "namespace": "665987",
                    "excludedPayments": []
                }
            ],
            "userType": "CORP",
            "needResetPassword": false
        }
        :return:
        """
        return self.request.get(self.conf.url('/accounts/show'))
