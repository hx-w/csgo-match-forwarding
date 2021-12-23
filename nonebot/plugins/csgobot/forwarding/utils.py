# -*- coding: utf-8 -*-

import json
import copy
import datetime
import requests

import nonebot

bot = nonebot.get_bot()
__teamlist_path = '/var/lib/match-nonebot/__subscribed.json'

__default_teamlist = [
    "astralis",
    "natus vincere",
    "g2",
    "fnatic",
    "liquid",
    "funplus phoenix",
    "faze",
    "vitality",
    "virtus.pro",
    "og",
    "big",
    "gambit",
    "nip",
    "vici",
    "tyloo"
]

__hotlist = []


async def create_teamlist_if_not_exist():
    global __hotlist, __teamlist_path
    try:
        with open(__teamlist_path, 'r', encoding='utf-8') as iFile:
            __hotlist = json.load(iFile)
            return True
    except:
        with open(__teamlist_path, 'w', encoding='utf-8') as oFile:
            json.dump(__default_teamlist, oFile)
            __hotlist = copy.deepcopy(__default_teamlist)
        return False


async def get_all_list() -> list:
    global __hotlist, __teamlist_path
    with open(__teamlist_path, 'r') as iFile:
        __hotlist = json.load(iFile)
    return __hotlist


# return 0 error
#        1 success
#        2 duplicate
async def set_team(teamname: str) -> bool:
    global __hotlist, __teamlist_path
    teamname = teamname.lower()
    if teamname in __hotlist:
        return 2
    __hotlist.append(teamname)
    try:
        with open(__teamlist_path, 'w') as oFile:
            json.dump(__hotlist, oFile)
        return 1
    except Exception as ept:
        print(f'[ERROR] {ept}')
        return 0


async def del_team(teamname: str) -> bool:
    global __hotlist
    teamname = teamname.lower()
    if teamname in __hotlist:
        __hotlist.remove(teamname)
        with open(__teamlist_path, 'w') as oFile:
            json.dump(__hotlist, oFile)
        return 1
    return 0


async def check_team(teamname: str) -> bool:
    return teamname.lower() in __hotlist


async def convert_localtime(utcTime: str) -> datetime.datetime:
    utc_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    ctime = datetime.datetime.strptime(utcTime, utc_format)
    localtime = ctime + datetime.timedelta(hours=8)  # beijing
    return localtime


async def goreq(url: str) -> list:
    resp = requests.get(url)
    try:
        assert resp.status_code == 200
        return json.loads(resp.content.decode('utf-8'))
    except Exception as ept:
        for spid in bot.config.SUPERUSERS:
            await bot.send_private_msg(spid, message=f'请求错误\n[API] {url}\n[ERR] {ept}')
    return []


async def broadcast(message: nonebot.Message):
    for qgid in bot.config.BROADCAST_GROUP_LIST:
        await bot.send_group_msg(qgid, message=message)
