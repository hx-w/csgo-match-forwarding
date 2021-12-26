# -*- coding: utf-8 -*-

from typing import List
import nonebot
from .base import ForwardBase
from .base import AsyncObject
from .subscribe_inst import SubscribeSystem

bot = nonebot.get_bot()


class MatchForward(ForwardBase, AsyncObject):
    async def __init__(self):
        super().__init__()
        self.subscribe_inst = await SubscribeSystem()

    def customer_filter(self, inst: dict) -> bool:
        return True in [self.subscribe_inst.check_team_status(team) for team in inst['teams']]

    async def generate_message(self) -> List[nonebot.Message]:
        _validlist = await self.request_data(bot.config.API('/results'))
        return list(map(lambda x: f'{x}', _validlist))


class NewsForward(ForwardBase):
    def customer_filter(self, inst: dict) -> bool:
        return super().customer_filter(inst)

    async def generate_message(self) -> List[nonebot.Message]:
        _validlist = await self.request_data(bot.config.API('/news'))
        return list(map(lambda x: f'{x}', _validlist))
