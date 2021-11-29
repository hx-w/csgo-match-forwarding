# nonebot相关配置
# 使用时需要将该配置文件复制到./configs下
from nonebot.default_config import *


# hltv的数据api地址，默认提供的api服务器在国外，之后会出自定义部署hltv api的方法
HLTV_API_ENDPOINT = 'https://selfhost-hltv-api.vercel.app/'

# 管理员的QQ 订阅战队需要有管理员权限
SUPERUSERS = {765892480}  # 多个管理员用英文逗号隔开

## === 不用更改 === ##
DEBUG = False
HOST = 'match-nonebot'
PORT = 9098
## =============== ##
