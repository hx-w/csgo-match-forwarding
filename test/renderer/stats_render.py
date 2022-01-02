# -*- coding: utf-8 -*-
'''
A Match Result Renderer
'''

from PIL import Image
from .base import RenderBase
from .async_req import req_inst


class StatsRender(RenderBase):
    def __init__(self, fontsize: int = 32) -> None:
        self._COLORS = {
            'TEAMS': ['#0F659E', '#9E691C'],
            'CT/T': ['#E0A42D', '#2C6EA4'],
            'MAPS': {
                'Vertigo': '#1C9580',
                'Inferno': '#15488E',
                'Overpass': '#BD6225',
                'Mirage': '#773BC9',
                'Nuke': '#952021',
                'Dust2': '#D7C64C',
                'Ancient': '#134632',
                'Train': '#368911',
                'Cache': '#3999CD'
            }
        }
        self._logo_images = []
        super().__init__(fontsize=fontsize)
    
    async def __blend_teamlogo(self, urls: list):
        logos = await req_inst.request(urls, True)
        self._logo_images = [await self.get_image_from_binary(logos[0]), await self.get_image_from_binary(logos[1])]
        self._logo_images = list(map(lambda x: x.resize((50, 50), Image.ANTIALIAS) if x else None, self._logo_images))
        if self._logo_images[0]:
            await self.paste_image(self._logo_images[0], (10, 3))
        if self._logo_images[1]:
            await self.paste_image(self._logo_images[1], (self._w - 60, 3))

    async def __render_map_info(self, map_info: dict, idx: int = 0):
        # draw badge
        _map_color = 'gray'
        if map_info['name'] in self._COLORS['MAPS'].keys():
            _map_color = self._COLORS['MAPS'][map_info['name']]
        self.draw_box((38, idx * 80 + 115, 125, idx * 80 + 138), _map_color, radius=10)
        _line = [' ' + '{:<10}'.format(map_info['name']), '{}'.format('上半场'), '{}'.format('下半场'), '总计']
        self.draw_text_grid(idx * 80 + 115, _line, grids=[1.5, 1, 1, 1], fills=['white', 'black', 'black', 'black'], padding = 40)
        
        async def __render_team_info(y: int, team_info: dict, winner: str):
            _line = [
                '{:<10}'.format(team_info['name']),
                '{}({})'.format(team_info['result']['first']['rounds'], team_info['result']['first']['side'].upper()),
                '{}({})'.format(team_info['result']['second']['rounds'], team_info['result']['second']['side'].upper()),
                '{}'.format(team_info['result']['first']['rounds'] + team_info['result']['second']['rounds'] + team_info['result']['ext'])
            ]
            if team_info['result']['ext']:
                _line[-1] += '(+{})'.format(team_info['result']['ext'])
            _fontcolors = [
                'black',
                self._COLORS['CT/T'][team_info['result']['first']['side'] == 'ct'],
                self._COLORS['CT/T'][team_info['result']['second']['side'] == 'ct'],
                'green' if team_info['name'] == winner else 'red'
            ]
            self.draw_text_grid(y, _line, grids=[1.5, 1, 1, 1], padding=40, fills=_fontcolors)
        
        async def __map_winner(teams_info: list) -> str:
            tscores = list(map(lambda x: sum([x['result']['first']['rounds'], x['result']['second']['rounds'], x['result']['ext']]), teams_info))
            return teams_info[int(tscores[0] < tscores[1])]['name']
        
        _winner = await __map_winner(map_info['teams'])
        
        await __render_team_info(idx * 80 + 137, map_info['teams'][0], _winner)
        await __render_team_info(idx * 80 + 157, map_info['teams'][1], _winner)

    async def __render_players(self, yindex: int, players: list, teamname: str, teamidx: int):
        # draw box
        self.draw_box((25, yindex, self._w - 25, yindex + 26), fill='#96A5AB')
        self._logo_images = list(map(lambda x: x.resize((30, 30), Image.ANTIALIAS) if x else None, self._logo_images))
        _line = [
            '{:<15}'.format(teamname),
            '{:<6}'.format('K-D'),
            '{:<3}'.format('+/-'),
            '{:<5}'.format('KAST'),
            '{:<6}'.format('Rating')
        ]
        _fontcolors = [self._COLORS['TEAMS'][teamidx], 'black', 'black', 'black', 'black']
        self.draw_text_grid(yindex, _line, padding=40, fills=_fontcolors, grids=[1.5, 1, 1, 1, 1])
        for idx, player in enumerate(players):
            _line = [
                '{:<15}'.format(player['nickname']),
                '{:<6}'.format(f'{player["kills"]}-{player["deaths"]}'),
                '{:<3}'.format(player["kills"] - player["deaths"]),
                '{:<5}'.format(f'{player["kast"]}%'),
                '{:<6}'.format(player['rating'])
            ]
            if int(_line[2]) > 0:
                _line[2] = '+' + _line[2]
            _fontcolors = [
                'black',
                '#4C596B',
                ['green', 'red'][int(_line[2]) < 0],
                '#4C596B',
                ['green', 'red'][float(_line[4]) < 1.0]
            ]
            self.draw_text_grid(yindex + (idx + 1) * 30, _line, padding=40, fills=_fontcolors, grids=[1.5, 1, 1, 1, 1])
        # # paste logo
        # if self._logo_images[teamidx]:
        #     await self.paste_image(self._logo_images[teamidx], (40, yindex))

    async def generate_image(self, content: dict):
        res, stats = content['result'], content['stats']
        await self.__blend_teamlogo([res['teams'][0]['logo'], res['teams'][1]['logo']])
        # L01
        self.draw_text_center(10, ['比赛战报'], [25])
        # L02
        _line = ['{:>15}'.format(res['teams'][0]['name']), ' 对阵 ', '{:<15}'.format(res['teams'][1]['name'])]
        self.draw_text_center(
            45,
            _line,
            fontsizes=[25, 16, 25],
            fills=[self._COLORS['TEAMS'][0], 'black', self._COLORS['TEAMS'][1]],
            pivot=1
        )
        # L03
        _line = [res['teams'][0]['result'], f'  {res["maps"]}  ', res['teams'][1]['result']]
        _fills = ['green', 'black', 'red'] if res['teams'][0]['result'] > res['teams'][1]['result'] else ['red', 'black', 'green']
        self.draw_text_center(73, _line, fills=_fills, fontsizes=[25, 18, 25], strokes_width=[1, 0, 1], pivot=1)
        # L04 divider
        self.draw_divider(108)
        # L05
        stats['maps'] = list(filter(
            lambda x: x['name'] != 'Default' and x['teams'][0]['result']['first']['rounds'] + x['teams'][0]['result']['second']['rounds'] != 0,
            stats['maps']
        ))
        for idx, map_info in enumerate(stats['maps']):
            await self.__render_map_info(map_info, idx)
        # L06 divider
        self.draw_divider(len(stats['maps']) * 80 + 108)
        # L07
        yindex = len(stats['maps']) * 80 + 120
        await self.__render_players(yindex, stats['teams'][0]['players'], stats['teams'][0]['name'], 0)
        await self.__render_players(yindex + 30 + len(stats['teams'][0]['players']) * 30, stats['teams'][1]['players'], stats['teams'][1]['name'], 1)

        del self._logo_images