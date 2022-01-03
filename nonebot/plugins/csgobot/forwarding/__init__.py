# -*- coding: utf-8 -*-

import nonebot

from .insts import init_insts_dict
from ..renderer import StatsRender

from ..async_req import req_inst

render_inst = StatsRender(16)

async def on_start_up():
    global insts_dict
    insts_dict = await init_insts_dict()


async def command_subscribe(session: nonebot.CommandSession):
    team = (await session.aget(prompt="输入想要订阅的战队名称")).strip()
    while not team:
        team = (await session.aget(prompt="输入的战队名不能为空，请重新输入")).strip()
    if await insts_dict['match_inst'].subscribe_inst.subscribe(team):
        await session.send(f'已订阅【{team}】的比赛')
    else:
        await session.send(f'【{team}】已在订阅列表中，输入【订阅列表】查看全部订阅')


async def command_subscribed(session: nonebot.CommandSession):
    teamlist = await insts_dict['match_inst'].subscribe_inst.get_subscribed_list()
    ret = "全部战队订阅(小写)：\n" + "\n".join(teamlist)

    await session.send(ret)


async def command_unsubscribe(session: nonebot.CommandSession):
    team = (await session.aget(prompt="输入想要取消订阅的战队名称")).strip()
    while not team:
        team = (await session.aget(prompt="输入的战队名不能为空，请重新输入")).strip()
    if await insts_dict['match_inst'].subscribe_inst.unsubscribe(team):
        await session.send(f'已取消订阅【{team}】的比赛')
    else:
        await session.send(f'未订阅【{team}】的比赛，取消订阅失败')

async def command_test(session: nonebot.CommandSession):
    _json = (await req_inst.request(['https://hltv-api.netlify.app/.netlify/functions/results']))[0][0]
    _stats = (await req_inst.request([f'https://hltv-api.netlify.app/.netlify/functions/stats/?matchId={_json["matchId"]}']))[0]
    _b64bytes = await render_inst.draw(500, 1300, {'result': _json, 'stats': _stats})
    await session.send(nonebot.MessageSegment.image(f'base64://{_b64bytes.decode("utf-8")}'))


async def handler_forwarding():
    await insts_dict['match_inst'].broadcast()
    await insts_dict['news_inst'].broadcast()


__all__ = [
    on_start_up,
    command_subscribe,
    command_unsubscribe,
    command_subscribed,
    command_test,
    handler_forwarding,
]
