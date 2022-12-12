# -*- coding: utf-8 -*-
'''
A Match Result Renderer
'''

from PIL import Image
from .base import RenderBase
from ..async_req import req_inst


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
        logos = [req_inst.request_sync(urls[0]), req_inst.request_sync(urls[1])]
        # logos = await req_inst.request(urls, True)
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
        
        async def __render_team_info(y: int, team_info: dict, winner: str, picker: str):
            _line = [
                '{:<10}'.format(team_info['name'] + ['', '(选)'][team_info['name'] == picker]),
                '{}({})'.format(team_info['result']['first']['rounds'], team_info['result']['first']['side'].upper()),
                '{}({})'.format(team_info['result']['second']['rounds'], team_info['result']['second']['side'].upper()),
                '{}'.format(team_info['result']['first']['rounds'] + team_info['result']['second']['rounds'] + team_info['result']['ext'])
            ]
            if team_info['result']['ext']:
                _line[-1] += '(+{})'.format(team_info['result']['ext'])
            _fontcolors = [
                '#626778',
                self._COLORS['CT/T'][team_info['result']['first']['side'] == 'ct'],
                self._COLORS['CT/T'][team_info['result']['second']['side'] == 'ct'],
                'darkgreen' if team_info['name'] == winner else 'red'
            ]
            self.draw_text_grid(y, _line, grids=[1.5, 1, 1, 1], padding=40, fills=_fontcolors)
        
        async def __map_winner(teams_info: list) -> str:
            tscores = list(map(lambda x: sum([x['result']['first']['rounds'], x['result']['second']['rounds'], x['result']['ext']]), teams_info))
            return teams_info[int(tscores[0] < tscores[1])]['name']
        
        _winner = await __map_winner(map_info['teams'])
        
        await __render_team_info(idx * 80 + 137, map_info['teams'][0], _winner, map_info['pick'])
        await __render_team_info(idx * 80 + 157, map_info['teams'][1], _winner, map_info['pick'])

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
                ['darkgreen', 'red'][int(_line[2]) < 0],
                '#4C596B',
                ['darkgreen', 'red'][float(_line[4]) < 1.0]
            ]
            self.draw_text_grid(yindex + (idx + 1) * 30, _line, padding=40, fills=_fontcolors, grids=[1.5, 1, 1, 1, 1])
    
    async def fetch_player_json(self, playerId: int) -> dict:
        ENDPOINT = 'https://hltv-api.netlify.app/.netlify/functions'
        player_info = (await req_inst.request([f'{ENDPOINT}/player/?playerId={playerId}']))[0]
        return player_info

    async def __render_player_card(self, yindex: int, playerId: int):
        self.draw_text_center(yindex, texts=['- MVP -'], fontsizes=[25], fills=['green'], strokes_width=[0])
        player_info = await self.fetch_player_json(playerId)
        _player_img_bin = req_inst.request_sync(player_info['image'])
        _player_img = (await self.get_image_from_binary(_player_img_bin)).resize((100, 100), Image.ANTIALIAS)
        await self.paste_image(_player_img, (40, yindex + 38))

        self.draw_box((150, yindex + 38, self._w - 40, yindex + 138), fill='#F3F5F7')
        self.draw_text_center(yindex + 38, texts=[player_info['nickname']], fontsizes=[18], fills=['black'], padding=100)
        _line = ['地图数', '爆头率', 'Impact', 'Rating']
        self.draw_text_grid(yindex + 67, texts=_line, grids=[1, 1, 1, 1], padding=160, fontsizes=[12, 12, 12, 12], fills=['#565C61'] * 4)
        _line = [
            player_info['mapsPlayed'],
            f'{player_info["headshots"]}%',
            '{:^4}'.format(player_info['impact']),
            '{:^4}'.format(player_info['rating'])
        ]
        self.draw_text_grid(yindex + 80, texts=_line, grids=[1, 1, 1, 1], padding=160, fontsizes=[12, 12, 12, 12])
        _line = ['回合击杀', '回合死亡', '回合伤害', 'KAST']
        self.draw_text_grid(yindex + 104, texts=_line, grids=[1, 1, 1, 1], padding=160, fontsizes=[12, 12, 12, 12], fills=['#565C61'] * 4)
        _line = [
            '{:^4}'.format(player_info['kpr']),
            '{:^4}'.format(player_info['dpr']),
            '{:^4}'.format(player_info['adr']),
            f'{player_info["kast"]}%'
        ]
        self.draw_text_grid(yindex + 117, texts=_line, grids=[1, 1, 1, 1], padding=160, fontsizes=[12, 12, 12, 12])



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
        _fills = ['green', 'black', 'red'] if res['teams'][0]['result'] > res['teams'][1]['result'] else ['red', 'black', 'darkgreen']
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
        # L08 divider
        yindex = yindex + 60 + (len(stats['teams'][0]['players']) + len(stats['teams'][1]['players'])) * 30
        self.draw_divider(yindex)
        # L09 highest rating player
        hightest_rating_player = [stats['teams'][0]['players'][0]['id'], stats['teams'][1]['players'][0]['id']][
            stats['teams'][0]['players'][0]['rating'] < stats['teams'][1]['players'][0]['rating']
        ]
        await self.__render_player_card(yindex, hightest_rating_player)

        # post process
        await self.crop(yindex + 160)
        del self._logo_images