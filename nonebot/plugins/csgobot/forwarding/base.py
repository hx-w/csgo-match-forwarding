# -*- coding: utf-8 -*-

import abc
import datetime
from typing import List

import nonebot
from ..async_req import req_inst

bot = nonebot.get_bot()


class AsyncObject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass


class ForwardBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self._utc_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        self._time_region = +8
        self._period = bot.config.MATCH_RESULT_CHECK_PERIOD  # seconds for sheduler check
        self.__sync_clock()

    def __sync_clock(self):
        self._now_timestamp = int(datetime.datetime.now().timestamp())

    def utc2timestamp(self, utc_time: str) -> int:
        ctime = datetime.datetime.strptime(utc_time, self._utc_format)
        localtime = ctime + datetime.timedelta(hours=self._time_region)
        return int(localtime.timestamp())

    def time_filter(self, inst: dict) -> bool:
        local_timestamp = self.utc2timestamp(inst['time'])
        return (self._now_timestamp - local_timestamp) < bot.config.MATCH_RESULT_CHECK_PERIOD

    @abc.abstractmethod
    def customer_filter(self, inst: dict) -> bool:
        '''
        determine wether saving this instance or not after time_filter
        '''
        return True

    def __filter_handler(self, all_res: list) -> list:
        self.__sync_clock()
        return list(filter(lambda x: self.time_filter(x) and self.customer_filter(x), all_res))

    async def request_data(self, url: str) -> list:
        _all = (await req_inst.request([url]))[0]
        return self.__filter_handler(_all)

    @abc.abstractmethod
    async def generate_message(self) -> List[nonebot.Message]:
        '''
        request api and generate message list for broadcast
        '''
        return []

    async def broadcast(self):
        message_list = await self.generate_message()
        for qgid in bot.config.BROADCAST_GROUP_LIST:
            for message in message_list:
                await bot.send_group_msg(group_id=qgid, message=message)
