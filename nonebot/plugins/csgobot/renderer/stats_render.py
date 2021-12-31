# -*- coding: utf-8 -*-
'''
A Match Result Renderer
'''

from .base import RenderBase


class StatsRender(RenderBase):
    def generate_image(self, content: dict):
        return super().generate_image(content)