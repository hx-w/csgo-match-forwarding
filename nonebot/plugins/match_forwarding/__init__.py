# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot
from nonebot.permission import GROUP_ADMIN, SUPERUSER

from . import subscribe
from . import forwarding
from . import utils

match_bot: nonebot.NoneBot = nonebot.get_bot()


@nonebot.on_websocket_connect
async def connect(event: aiocqhttp.Event):
    await utils.create_if_not_exist()


@nonebot.on_command("订阅", aliases=("战队订阅"), permission=GROUP_ADMIN | SUPERUSER)
async def handler_subscribe(session: nonebot.CommandSession):
    await subscribe.command_subscribe(session)


@nonebot.on_command("取消订阅", permission=GROUP_ADMIN | SUPERUSER)
async def handler_unsubscribe(session: nonebot.CommandSession):
    print('?????????????')
    await subscribe.command_unsubscribe(session)


@nonebot.on_command("订阅列表", aliases=("全部订阅"))
async def handler_teamlist(session: nonebot.CommandSession):
    await subscribe.command_teamlist(session)


@nonebot.scheduler.scheduled_job('cron', minute='*')
async def handler_spider():
    await forwarding.handler_forwarding(match_bot)
