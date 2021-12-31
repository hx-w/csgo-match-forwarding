# -*- coding: utf-8 -*-
import base64
import asyncio
from renderer import StatsRender

render_inst = StatsRender()

loop = asyncio.get_event_loop()
b64bytes = loop.run_until_complete(render_inst.draw(800, 600, {}))
loop.close()
img = base64.b64decode(b64bytes)
with open('test.png', 'wb') as ofile:
    ofile.write(img)