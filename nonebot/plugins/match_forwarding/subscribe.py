# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot


async def handler_subscribe(bot: nonebot.NoneBot, event: aiocqhttp.Event):
    print('handled')
