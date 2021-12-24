# -*- coding: utf-8 -*-
import datetime
import nonebot

from . import utils
from ..renderer import AsyncRequest

bot = nonebot.get_bot()
req_inst = AsyncRequest([
    bot.config.API('/results'),
    bot.config.API('/news')
])


async def __check_new(reslist: list):
    nowTime = datetime.datetime.now()
    newList = []
    for result in reslist:
        resTime = await utils.convert_localtime(result['time'])
        if (resTime - nowTime).seconds >= bot.config.MATCH_RESULT_CHECK_PERIOD:
            break
        newList.append(result)
    return newList


async def __handler_results(results_all: list):
    list_new = await __check_new(results_all)
    if len(list_new) > 0:
        # RENDER DO
        matchIdList = list(x['matchId'] for x in list_new)
        #
        await utils.broadcast(f'比赛战报\n{matchIdList}')


async def __handler_news(news_all: list):
    list_new = await __check_new(news_all)
    for news in list_new:
        await utils.broadcast(f'CSGO新闻速递\n{news["title"]}\n{news["description"]}')


async def handler_forward_all():
    resptuple = await req_inst.request()
    await __handler_results(resptuple[0])
    await __handler_news(resptuple[1])
