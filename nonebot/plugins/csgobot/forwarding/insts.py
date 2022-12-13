# -*- coding: utf-8 -*-

from typing import Dict
from . import forward_inst


async def init_insts_dict() -> Dict[str, forward_inst.ForwardBase]:
    return {
        'match_inst': await forward_inst.MatchForward(),
        'news_inst': forward_inst.NewsForward(),
    }
