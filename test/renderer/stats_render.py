# -*- coding: utf-8 -*-
'''
A Match Result Renderer
'''

from .base import RenderBase


class StatsRender(RenderBase):
    async def generate_image(self, content: dict):
        res, stats = content['result'], content['stats']
        # L01
        self.draw_text_center(10, ['比赛战报'], [25], ['#BA026E'])
        # L02
        _line = [res['teams'][0]['name'], ' vs ', res['teams'][1]['name']]
        self.draw_text_center(48, _line, fontsizes=[20, 16, 20], fills=['#536FF7', '#000000', '#ED6E6B'], pivot=1)
        # L03
        _line = [res['teams'][0]['result'], f'  {res["maps"]}  ', res['teams'][1]['result']]
        self.draw_text_center(78, _line, pivot=1)