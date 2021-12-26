# -*- coding: utf-8 -*-

from . import forward_inst
from . import subscribe_inst


async def init_insts_dict():
    return {
        'match_inst': forward_inst.MatchForward(),
        'news_inst': forward_inst.NewsForward(),
        'subscribe_inst': await subscribe_inst.SubscribeSystem()
    }
