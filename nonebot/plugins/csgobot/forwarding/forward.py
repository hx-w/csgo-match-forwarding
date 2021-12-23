# -*- coding: utf-8 -*-
import datetime
import nonebot

from . import utils

bot = nonebot.get_bot()


async def __handler_newinfo(api: str) -> list:
    respList = await utils.goreq(await bot.config.API(api))
    nowTime = datetime.datetime.now()
    newList = []
    for result in respList:
        resTime = await utils.convert_localtime(result['time'])
        if (resTime - nowTime).seconds >= bot.config.MATCH_RESULT_CHECK_PERIOD:
            break
        newList.append(result)
    return newList


async def handler_new_result():
    newList = await __handler_newinfo('/results')
    if len(newList) > 0:
        # RENDER DO
        matchIdList = list(x['matchId'] for x in newList)
        #
        await utils.broadcast(f'比赛战报\n{matchIdList}')


async def handler_new_news():
    newList = await __handler_newinfo('/news')
    for news in newList:
        await utils.broadcast(f'CSGO新闻速递\n{news["title"]}\n{news["description"]}')
