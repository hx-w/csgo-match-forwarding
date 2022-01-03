# -*- coding: utf-8 -*-

import gc
import abc
from typing import List, Tuple, Callable
import functools
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class RenderBase(metaclass=abc.ABCMeta):
    '''
    @abstractmethod for self.__generate_image
    '''

    def __init__(self, fontsize: int = 32) -> None:
        self._fonttype = self.__get_fonttype(fontsize)
        self._image: Image = None
        self._drawtable: ImageDraw = None
        self._w, self._h = 0, 0
        self._fontsize = fontsize

    def __get_fonttype(self, fontsize) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype('../static/font/YaHeiConsolas.ttf', fontsize)

    async def __image2base64(self) -> bytes:
        _buffer = BytesIO()
        self._image.save(_buffer, format='PNG')
        return base64.b64encode(_buffer.getvalue())

    async def __allocate(self, width: int, height: int):
        self._w, self._h = width, height
        self._image = Image.new('RGB', (width, height), 'white')
        self._drawtable = ImageDraw.Draw(im=self._image)

    async def __free(self):
        del self._image, self._drawtable
        gc.collect()
    
    async def get_image_from_binary(self, bytes_: bytes) -> Image:
        try:
            im = Image.open(BytesIO(bytes_)).convert('RGBA')
            imp = Image.new('RGBA', im.size, (255, 255, 255))
            imp.paste(im, (0, 0, *im.size), im)
            return imp
        except:
            return None
    
    async def paste_image(self, image_: Image, box: Tuple[int]):
        self._image.paste(image_, box=box)
    
    def draw_valid_required(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            if not self._drawtable:
                return
            return func(self, *args, **kw)
        return wrapper
    
    def crop(self, y: int):
        self._image = self._image.crop((0, 0, 500, y))

    @draw_valid_required
    def draw_text(self, xy: tuple, text: str, fontsize: int = 0, fill: str = '#000000', stroke_width = 0):
        _font = self.__get_fonttype(fontsize) if fontsize and fontsize != self._fontsize else self._fonttype
        self._drawtable.text(xy=xy, text=text, fill=fill, font=_font, stroke_width=stroke_width)

    @draw_valid_required
    def draw_divider(self, y: int, percent: float = 0.9, fill: str = 'gray'):
        _padding = self._w * ((1 - percent) / 2)
        self._drawtable.line([(_padding, y), (self._w - _padding, y)], fill=fill)
    
    @draw_valid_required
    def draw_box(self, xy: Tuple[int], fill: str = 'gray', radius: int = 8):
        self._drawtable.rounded_rectangle(xy, fill=fill, radius=radius)

    def __calc_texts_center_index(self, texts: List[str], fontsizes: List[int], pivot: int, padding: int) -> List[int]:
        def _(c: str) -> float:
            return 1 if '\u4e00' <= c and c <= '\u9fa5' else 0.55
        real_sizes = []
        for idx, text in enumerate(texts):
            real_sizes.append(sum(list(map(lambda x: _(x) * fontsizes[idx], text))))
        totalsize = sum(real_sizes)
        heads = [0] * len(texts)
        if pivot == -1:
            heads = [padding + (self._w - totalsize - padding) / 2]
            for rsize in real_sizes[:-1]:
                heads.append(heads[-1] + rsize)
        else: # valid pivot
            heads[pivot] = padding + (self._w - real_sizes[pivot] - padding) / 2
            for front_idx in range(1, pivot + 1):
                heads[pivot - front_idx] = heads[pivot - front_idx + 1] - real_sizes[pivot - front_idx]
            for back_idx in range(pivot + 1, len(texts)):
                heads[back_idx] = heads[back_idx - 1] + real_sizes[back_idx - 1]
        return heads

    @draw_valid_required
    def draw_text_center(self, y: int, texts: List[str], fontsizes: List[int] = [], fills: List[str] = [], pivot: int = -1, strokes_width: List[int] = [], padding: int = 0):
        texts = list(map(str, texts))
        if len(fontsizes) == 0:
            fontsizes = [self._fontsize] * len(texts)
        if len(fills) == 0:
            fills = ['#000000'] * len(texts)
        if len(strokes_width) == 0:
            strokes_width = [0] * len(texts)
        maxsize = max(fontsizes)
        ydiffs = list(map(lambda x: maxsize - x, fontsizes))
        heads = self.__calc_texts_center_index(texts, fontsizes, pivot, padding)
        for idx, text in enumerate(texts):
            self.draw_text((heads[idx], y + ydiffs[idx]), text, fontsizes[idx], fills[idx], strokes_width[idx])
    
    @draw_valid_required
    def draw_text_grid(self, y: int, texts: List[str], fontsizes: List[int] = [], fills: List[str] = [], grids: List[int] = [], padding: int = 0, strokes_width: List[int] = []):
        texts = list(map(str, texts))
        if len(fontsizes) == 0:
            fontsizes = [self._fontsize] * len(texts)
        if len(fills) == 0:
            fills = ['#000000'] * len(texts)
        if len(grids) == 0:
            grids = [1] * len(texts)
        if len(strokes_width) == 0:
            strokes_width = [0] * len(texts)
        maxsize = max(fontsizes)
        ydiffs = list(map(lambda x: maxsize - x, fontsizes))
        total_grid = sum(grids)
        heads = []
        for idx in range(len(grids)):
            heads.append(padding if idx == 0 else heads[-1] + (self._w - padding) * (grids[idx - 1] / total_grid))
        for idx, text in enumerate(texts):
            self.draw_text((heads[idx], y + ydiffs[idx]), text, fontsizes[idx], fills[idx], strokes_width[idx])

    @abc.abstractmethod
    async def generate_image(self, content: dict):
        '''
        different methods in different scenario
        use self.draw_text to draw text on image
        '''

    async def draw(self, width: int, height: int, content: dict) -> bytes:
        await self.__allocate(width, height)
        await self.generate_image(content)

        _b64bytes = await self.__image2base64()
        await self.__free()
        return _b64bytes
