# -*- coding: utf-8 -*-

import json
import copy
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


def check_team(teamname: str) -> bool:
    return teamname.lower() in __hotlist
