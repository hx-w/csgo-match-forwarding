# -*- coding: utf-8 -*-
'''
A Match Result Renderer
'''

from PIL import Image
from .base import RenderBase
from .async_req import req_inst


class StatsRender(RenderBase):
    async def __blend_teamlogo(self, urls: list):
        logos = await req_inst.request(urls, True)
        logo_images = [await self.get_image_from_binary(logos[0]), await self.get_image_from_binary(logos[1])]
        logo_images = list(map(lambda x: x.resize((50, 50), Image.ANTIALIAS) if x else None, logo_images))
        if logo_images[0]:
            await self.paste_image(logo_images[0], (10, 3))
        if logo_images[1]:
            await self.paste_image(logo_images[1], (self._w - 60, 3))

    async def __render_map_info(self, map_info: dict, idx: int = 0):
        _line = ['{:<10}'.format(map_info['name']), '{}'.format('上半场'), '{}'.format('下半场'), '总计']
        self.draw_text_grid(idx * 80 + 115, _line, grids=[1.5, 1, 1, 1], padding = 40)
        _line = [
            '{:<10}'.format(map_info['teams'][0]['name']),
            '{}({})'.format(map_info['teams'][0]['result']['first']['rounds'], map_info['teams'][0]['result']['first']['side'].upper()), 
            '{}({})'.format(map_info['teams'][0]['result']['second']['rounds'], map_info['teams'][0]['result']['second']['side'].upper()),
            map_info['teams'][0]['result']['first']['rounds'] + map_info['teams'][0]['result']['second']['rounds']
        ]
        self.draw_text_grid(idx * 80 + 135, _line, grids=[1.5, 1, 1, 1], padding = 40)        
        _line = [
            '{:<10}'.format(map_info['teams'][1]['name']),
            '{}({})'.format(map_info['teams'][1]['result']['first']['rounds'], map_info['teams'][1]['result']['first']['side'].upper()), 
            '{}({})'.format(map_info['teams'][1]['result']['second']['rounds'], map_info['teams'][1]['result']['second']['side'].upper()),
            map_info['teams'][1]['result']['first']['rounds'] + map_info['teams'][1]['result']['second']['rounds']
        ]
        self.draw_text_grid(idx * 80 + 155, _line, grids=[1.5, 1, 1, 1], padding = 40)        

    async def __render_players(self, yindex: int, players: list, teamname: str):
        for idx, player in enumerate(players):
            _line = [
                '{:<15}'.format(player['nickname']),
                '{:<5}'.format(player['kills']),
                '{:<6}'.format(player['deaths']),
                '{:<5}'.format(player['kast']),
                '{:<6}'.format(player['rating'])
            ]
            self.draw_text_grid(yindex + idx * 30, _line, padding=40, grids=[1.5, 1, 1, 1, 1])


    async def generate_image(self, content: dict):
        res, stats = content['result'], content['stats']
        await self.__blend_teamlogo([res['teams'][0]['logo'], res['teams'][1]['logo']])
        # L01
        self.draw_text_center(10, ['比赛战报'], [25])
        # L02
        _line = ['{:>15}'.format(res['teams'][0]['name']), ' 对阵 ', '{:<15}'.format(res['teams'][1]['name'])]
        self.draw_text_center(45, _line, fontsizes=[22, 16, 22], fills=['#536FF7', '#000000', '#ED6E6B'], pivot=1)
        # L03
        _line = [res['teams'][0]['result'], f'  {res["maps"]}  ', res['teams'][1]['result']]
        _fills = ['green', 'black', 'red'] if res['teams'][0]['result'] > res['teams'][1]['result'] else ['red', 'black', 'green']
        self.draw_text_center(73, _line, fills=_fills, fontsizes=[25, 18, 25], pivot=1)
        # L04 divider
        self.draw_divider(108)
        # L05
        stats['maps'] = list(filter(lambda x: x['name'] != 'Default', stats['maps']))
        for idx, map_info in enumerate(stats['maps']):
            await self.__render_map_info(map_info, idx)
        # L06
        self.draw_divider(len(stats['maps']) * 80 + 108)
        yindex = len(stats['maps']) * 80 + 120
        _line = [
            '{:<15}'.format('选手'),
            '{:<5}'.format('kills'),
            '{:<6}'.format('deaths'),
            '{:<5}'.format('kast'),
            '{:<6}'.format('rating')
        ]
        self.draw_text_grid(yindex, _line, padding=40, grids=[1.5, 1, 1, 1, 1])
        await self.__render_players(yindex + 30, stats['teams'][0]['players'], stats['teams'][0]['name'])
        await self.__render_players(yindex + 30 + len(stats['teams'][0]['players']) * 30, stats['teams'][1]['players'], stats['teams'][1]['name'])
