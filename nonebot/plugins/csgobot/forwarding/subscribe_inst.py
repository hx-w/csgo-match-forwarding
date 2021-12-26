# -*- coding: utf-8 -*-
import json

from .base import AsyncObject

class SubscribeSystem(AsyncObject):
    async def __init__(self):
        self._subscribed_path = '/var/lib/match-nonebot/__subscribed.json'
        # self._cached_teamlist = []
        await self.init_if_not_exist()

    async def __init_cached_teamlist(self):
        '''
        top10 teams default
        '''
        self._cached_teamlist = []

    async def init_if_not_exist(self):
        try:
            with open(self._subscribed_path, 'r', encoding='utf-8') as iFile:
                self._cached_teamlist = json.load(iFile)
        except:
            await self.__init_cached_teamlist()
            with open(self._subscribed_path, 'w', encoding='utf-8') as oFile:
                json.dump(self._cached_teamlist, oFile)

    async def __sync_cache2file(self):
        with open(self._subscribed_path, 'w', encoding='utf-8') as oFile:
            json.dump(self._cached_teamlist, oFile)

    async def get_subscribed_list(self) -> list:
        return self._cached_teamlist

    async def subscribe(self, teamname: str) -> bool:
        '''
        @return True => new added
                False => duplicated
        '''
        teamname = teamname.lower()
        if teamname in self._cached_teamlist:
            return False
        self._cached_teamlist.append(teamname)
        await self.__sync_cache2file()
        return True

    async def unsubscribe(self, teamname: str) -> bool:
        '''
        @return True => operating succeed
                False => not found
        '''
        teamname = teamname.lower()
        if teamname in self._cached_teamlist:
            self._cached_teamlist.remove(teamname)
            await self.__sync_cache2file()
            return True
        return False

    def check_team_status(self, teamname: str) -> bool:
        '''
        @return True => team is subscribed
                False => team is not subscribed
        '''
        return teamname.lower() in self._cached_teamlist
