# -*- coding: utf-8 -*-

from . import forward_inst


async def init_insts_dict():
    return {
        'match_inst': await forward_inst.MatchForward(),
        'news_inst': forward_inst.NewsForward(),
    }
