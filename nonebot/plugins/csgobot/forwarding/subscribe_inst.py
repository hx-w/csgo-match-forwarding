# -*- coding: utf-8 -*-
import abc
import json

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


class SubscribeSystem(AsyncObject):
    async def __init__(self):
        self._subscribed_path = '/var/lib/match-nonebot/__subscribed.json'
        await self.__init_cached_teamlist()

    async def __init_cached_teamlist(self):
        self._cached_teamlist = []

    async def init_if_not_exist(self) -> bool:
        try:
            with open(self._subscribed_path, 'r', encoding='utf-8') as iFile:
                self._cached_teamlist = json.load(iFile)
            return True
        except:
            with open(self._subscribed_path, 'w', encoding='utf-8') as oFile:
                json.dump(self._cached_teamlist, oFile)
            return False

    async def __sync_cache2file(self):
        with open(self._subscribed_path, 'w', encoding='utf-8') as oFile:
            json.dump(self._cached_teamlist, oFile)
    
    async def get_subscribed_list(self) -> list:
        return self._cached_teamlist
    
    async def subscribe(self, teamname: str) -> bool:
        pass