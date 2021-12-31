# -*- coding: utf-8 -*-

import gc
import abc
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class RenderBase(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._fonttype = ImageFont.truetype(
            '../static/font/YaHeiConsolas.ttf')
        self._image: Image = None
        self._drawtable: ImageDraw = None

    async def __image2base64(self) -> bytes:
        _buffer = BytesIO()
        self._image.save(_buffer, format='PNG')
        return base64.b64encode(_buffer.getvalue())

    async def __allocate(self, width: int, height: int):
        self._image = Image.new('RGB', (width, height), 'white')
        self._drawtable = ImageDraw.Draw(im=self._image)

    async def __free(self):
        del self._image, self._drawtable
        gc.collect()

    async def draw_text(self, xy: tuple, text: str, fill: str = '#000000'):
        if self._drawtable:
            self._drawtable.text(
                xy=xy, text=text, fill=fill, font=self._fonttype)

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
