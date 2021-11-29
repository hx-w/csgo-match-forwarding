# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot

from . import subscribe
from . import forwarding

match_bot: nonebot.NoneBot = nonebot.get_bot()


@match_bot.on_message('group')
async def handler_group_message(event: aiocqhttp.Event):
    await subscribe.handler_subscribe(match_bot, event)


@nonebot.scheduler.scheduled_job('cron', minute='*')
async def handler_spider():
    await forwarding.handler_forwarding(match_bot)
