# -*- coding: utf-8 -*-

from typing import List
import nonebot
from .base import ForwardBase
from .base import AsyncObject
from .subscribe_inst import SubscribeSystem
from ..renderer import StatsRender

render_inst = StatsRender(16)
bot = nonebot.get_bot()


class MatchForward(ForwardBase, AsyncObject):
    async def __init__(self):
        super().__init__()
        self.subscribe_inst = await SubscribeSystem()

    def customer_filter(self, inst: dict) -> bool:
        return True in [self.subscribe_inst.check_team_status(team['name']) for team in inst['teams']]

    async def generate_message(self) -> List[nonebot.Message]:
        message_list = []
        _validlist = await self.request_data(bot.config.API('/results'))
        for _valid in _validlist:
            _stats = await self.request_data(bot.config.API(f'/stats/?matchId={_valid["matchId"]}'))
            _b64bytes = await render_inst.draw(500, 1300, {'result': _valid, 'stats': _stats})
            message_list.append(nonebot.MessageSegment.image(f'base64://{_b64bytes.decode("utf-8")}'))
        return message_list


class NewsForward(ForwardBase):
    def customer_filter(self, inst: dict) -> bool:
        return super().customer_filter(inst)

    async def generate_message(self) -> List[nonebot.Message]:
        _validlist = await self.request_data(bot.config.API('/news'))
        return list(map(lambda x: f'【新闻速递】\n{x["title"]}\n\n{x["description"]}', _validlist))
