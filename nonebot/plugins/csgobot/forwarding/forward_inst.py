# -*- coding: utf-8 -*-

from typing import List
import nonebot
from .base import ForwardBase
from .utils import check_team

bot = nonebot.get_bot()


class MatchForward(ForwardBase):
    def __init__(self):
        super().__init__(bot.config.MATCH_RESULT_CHECK_PERIOD)

    def customer_filter(self, inst: dict) -> bool:
        return True in [check_team(team) for team in inst['teams']]

    async def generate_message(self) -> List[nonebot.Message]:
        _validlist = await self.request_data(bot.config.API('/results'))
        return list(map(lambda x: f'{x}', _validlist))


class NewsForward(ForwardBase):
    def __init__(self):
        super().__init__(bot.config.MATCH_RESULT_CHECK_PERIOD)

    def customer_filter(self, inst: dict) -> bool:
        return super().customer_filter(inst)

    async def generate_message(self) -> List[nonebot.Message]:
        _validlist = await self.request_data(bot.config.API('/news'))
        return list(map(lambda x: f'{x}', _validlist))


forward_insts = (
    MatchForward(),
    NewsForward()
)
