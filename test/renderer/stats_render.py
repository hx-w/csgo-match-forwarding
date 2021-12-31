# -*- coding: utf-8 -*-
'''
A Match Result Renderer
'''

from PIL import Image, ImageDraw
from .base import RenderBase
from .async_req import req_inst


class StatsRender(RenderBase):
    async def __blend_teamlogo(self, urls: list):
        logos = await req_inst.request(urls, True)
        logo_images = [await self.get_image_from_binary(logos[0]), await self.get_image_from_binary(logos[1])]
        logo_images = list(map(lambda x: x.resize((50, 50), Image.ANTIALIAS) if x else None, logo_images))
        if logo_images[0]:
            await self.paste_image(logo_images[0], (10, 10))
        if logo_images[1]:
            await self.paste_image(logo_images[1], (self._w - 60, 10))

    async def generate_image(self, content: dict):
        res, stats = content['result'], content['stats']
        await self.__blend_teamlogo([res['teams'][0]['logo'], res['teams'][1]['logo']])
        # L01
        self.draw_text_center(10, ['比赛战报'], [25])
        # L02
        _line = [res['teams'][0]['name'], ' vs ', res['teams'][1]['name']]
        self.draw_text_center(45, _line, fontsizes=[22, 16, 22], fills=['#536FF7', '#000000', '#ED6E6B'], pivot=1)
        # L03
        _line = [res['teams'][0]['result'], f'  {res["maps"]}  ', res['teams'][1]['result']]
        _fills = ['green', 'black', 'red'] if res['teams'][0]['result'] > res['teams'][1]['result'] else ['red', 'black', 'green']
        self.draw_text_center(75, _line, fills=_fills, fontsizes=[20, 16, 20], pivot=1)
        # L04 divider
        self.draw_divider(108)
