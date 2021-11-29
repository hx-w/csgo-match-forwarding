# -*- coding: utf-8 -*-

import json
import copy

TEAMLIST_PATH = '/var/lib/match-nonebot/__subscribed.json'

DEFAULT_LIST = [
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

HOT_LIST = []


async def create_if_not_exist():
    global HOT_LIST
    try:
        with open(TEAMLIST_PATH, 'r', encoding='utf-8') as iFile:
            HOT_LIST = json.load(iFile)
            return True
    except:
        with open(TEAMLIST_PATH, 'w', encoding='utf-8') as oFile:
            json.dump(DEFAULT_LIST, oFile)
            HOT_LIST = copy.deepcopy(DEFAULT_LIST)
        return False


async def get_all_list() -> list:
    global HOT_LIST
    with open(TEAMLIST_PATH, 'r') as iFile:
        HOT_LIST = json.load(iFile)
    return HOT_LIST


# return 0 error
#        1 success
#        2 duplicate
async def set_team(teamname: str) -> bool:
    global HOT_LIST
    teamname = teamname.lower()
    if teamname in HOT_LIST:
        return 2
    HOT_LIST.append(teamname)
    try:
        with open(TEAMLIST_PATH, 'w') as oFile:
            json.dump(HOT_LIST, oFile)
        return 1
    except Exception as ept:
        print(f'[ERROR] {ept}')
        return 0


async def del_team(teamname: str) -> bool:
    global HOT_LIST
    teamname = teamname.lower()
    if teamname in HOT_LIST:
        HOT_LIST.remove(teamname)
        with open(TEAMLIST_PATH, 'w') as oFile:
            json.dump(HOT_LIST, oFile)
        return 1
    return 0


async def check_team(teamname: str) -> bool:
    return teamname.lower() in HOT_LIST
