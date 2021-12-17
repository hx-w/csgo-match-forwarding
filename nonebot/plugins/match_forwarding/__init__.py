# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot
from nonebot.permission import GROUP_ADMIN, SUPERUSER
from nonebot import on_command, on_websocket_connect, CommandSession

from . import subscribe
from . import forwarding
from . import utils


@on_websocket_connect
async def connect(event: aiocqhttp.Event):
    print('connected!')
    await utils.create_if_not_exist()


@on_command('subscribe', aliases=('战队订阅', '订阅'), permission=GROUP_ADMIN | SUPERUSER)
async def handler_subscribe(session: CommandSession):
    print('subscribed!')
    await subscribe.command_subscribe(session)


@on_command('unsubscribe', aliases=('取消订阅'), permission=GROUP_ADMIN | SUPERUSER)
async def handler_unsubscribe(session: CommandSession):
    await subscribe.command_unsubscribe(session)


@on_command('subscribed_list', aliases=('订阅列表', '全部订阅'))
async def handler_teamlist(session: CommandSession):
    await subscribe.command_teamlist(session)


@on_command('match_list', aliases=('比赛预告'))
async def handlder_matchlist(session: CommandSession):
    pass


@nonebot.scheduler.scheduled_job('cron', minute='*')
async def handler_spider():
    await forwarding.handler_forwarding()
