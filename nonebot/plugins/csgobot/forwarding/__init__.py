# -*- coding: utf-8 -*-

import nonebot

from . import utils


async def command_subscribe(session: nonebot.CommandSession):
    team = (await session.aget(prompt="输入想要订阅的战队名称")).strip()
    while not team:
        team = (await session.aget(prompt="输入的战队名不能为空，请重新输入")).strip()
    retcode = await utils.set_team(team)
    if retcode == 1:
        await session.send(f'已订阅【{team}】的比赛')
    elif retcode == 2:
        await session.send(f'【{team}】已在订阅列表中，输入【订阅列表】查看全部订阅')
    else:
        await session.send(f'出现错误：{retcode}，请联系管理员修复')


async def command_subscribed(session: nonebot.CommandSession):
    teamlist = await utils.get_all_list()
    ret = "全部战队订阅(小写)：\n" + "\n".join(teamlist)
    await session.send(ret)


async def command_unsubscribe(session: nonebot.CommandSession):
    team = (await session.aget(prompt="输入想要取消订阅的战队名称")).strip()
    while not team:
        team = (await session.aget(prompt="输入的战队名不能为空，请重新输入")).strip()
    retcode = await utils.del_team(team)
    if retcode == 1:
        await session.send(f'已取消订阅【{team}】的比赛')
    else:
        await session.send(f'未订阅【{team}】的比赛，取消订阅失败')


async def handler_forwarding():
    pass


__all__ = [
    command_subscribe,
    command_unsubscribe,
    command_subscribed,
    handler_forwarding,
    utils
]
