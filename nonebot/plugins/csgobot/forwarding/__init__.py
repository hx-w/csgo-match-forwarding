# -*- coding: utf-8 -*-

import nonebot

from .insts import init_insts_dict
from ..renderer import StatsRender

from ..async_req import req_inst


bot = nonebot.get_bot()
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
    async def get_mvp_playerinfo(stats: dict) -> dict:
        try:
            _0, _1 = stats['teams'][0]['players'][0], stats['teams'][1]['players'][0]
            mvp_id = [_0['id'], _1['id']][_0['rating'] < _1['rating']]
            mvp_info = (await req_inst.request([bot.config.API(f'/player/?playerId={mvp_id}')]))[0]
            return mvp_info
        except:
            return {}

    _jsons = (await req_inst.request([bot.config.API('/results')]))[0]
    _json = {}
    for _ in _jsons:
        if insts_dict['match_inst'].subscribe_inst.check_team_status(_['teams'][0]['name']) \
            or insts_dict['match_inst'].subscribe_inst.check_team_status(_['teams'][1]['name']):
            _json = _
            break
    if len(_json) == 0:
        await session.send('没有符合条件的比赛')
        return
    _stats = (await req_inst.request(
        [bot.config.API(f'/stats/?matchId={_json["matchId"]}')]))[0]
    _mvp_info = await get_mvp_playerinfo(_stats)
    _b64bytes = await render_inst.draw(500, 1300, {'result': _json, 'stats': _stats, 'mvp': _mvp_info})
    await session.send(nonebot.MessageSegment.image(f'base64://{_b64bytes.decode("utf-8")}'))


async def handler_forwarding():
    await insts_dict['match_inst'].broadcast()
    await insts_dict['news_inst'].broadcast()


__all__ = [
    'on_start_up',
    'command_subscribe',
    'command_unsubscribe',
    'command_subscribed',
    'command_test',
    'handler_forwarding',
]
