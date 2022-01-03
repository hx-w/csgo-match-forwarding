# -*- coding: utf-8 -*-

import nonebot
from nonebot.default_config import SUPERUSERS
from nonebot.permission import GROUP_ADMIN, SUPERUSER
from nonebot import on_command, on_startup, CommandSession

from . import forwarding

bot = nonebot.get_bot()

@on_startup
async def init_all():
    await forwarding.on_start_up()


@on_command('subscribe', aliases=('战队订阅', '订阅'), permission=GROUP_ADMIN | SUPERUSER)
async def handler_subscribe(session: CommandSession):
    await forwarding.command_subscribe(session)


@on_command('unsubscribe', aliases=('取消订阅'), permission=GROUP_ADMIN | SUPERUSER)
async def handler_unsubscribe(session: CommandSession):
    await forwarding.command_unsubscribe(session)


@on_command('subscribed_list', aliases=('订阅列表', '全部订阅'))
async def handler_teamlist(session: CommandSession):
    await forwarding.command_subscribed(session)


@on_command('match_list', aliases=('比赛预告'))
async def handlder_matchlist(session: CommandSession):
    pass

@on_command('forward_test', aliases=('战报测试'), permission=SUPERUSER)
async def handler_test(session: CommandSession):
    await forwarding.command_test(session)

@nonebot.scheduler.scheduled_job('interval', seconds=bot.config.MATCH_RESULT_CHECK_PERIOD)
async def handler_forwarding():
    await forwarding.handler_forwarding()
