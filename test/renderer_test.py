# -*- coding: utf-8 -*-
import json
import base64
import asyncio
import requests
from renderer import StatsRender

def fetch_data_new():
    # ENDPOINT = 'https://service-ban7exd9-1256946954.cd.apigw.tencentcs.com/release'
    ENDPOINT = 'https://hltv-api.netlify.app/.netlify/functions'
    result = json.loads(requests.get(ENDPOINT + '/results').content.decode('utf-8'))[0]
    stats = json.loads(requests.get(ENDPOINT + '/stats/?matchId=' + str(result['matchId'])).content.decode('utf-8'))
    with open('result.json', 'w') as wfile:
        json.dump(result, wfile)
    with open('stats.json', 'w') as wfile:
        json.dump(stats, wfile)
    return {'result': result, 'stats': stats}

def fetch_data_cache():
    res = {}
    with open('result.json', 'r') as rfile:
        res['result'] = json.load(rfile)
    with open('stats.json', 'r') as rfile:
        res['stats'] = json.load(rfile)
    return res

render_inst = StatsRender(16)

loop = asyncio.get_event_loop()
b64bytes = loop.run_until_complete(render_inst.draw(500, 880, fetch_data_new()))
loop.close()

img = base64.b64decode(b64bytes)
with open('test.png', 'wb') as ofile:
    ofile.write(img)