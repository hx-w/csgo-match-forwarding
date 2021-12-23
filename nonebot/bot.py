# Nonebot v1
from os import path
import sys

import nonebot
sys.path.append('/var/lib/match-nonebot')
try:
    import nonebot_config as config
except:
    raise Exception('配置文件路径错误')

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()
