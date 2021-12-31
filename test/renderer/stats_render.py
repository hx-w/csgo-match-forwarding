# -*- coding: utf-8 -*-
'''
A Match Result Renderer
'''

from .base import RenderBase


class StatsRender(RenderBase):
    async def generate_image(self, content: dict):
        return await super().generate_image(content)