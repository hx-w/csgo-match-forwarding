# nonebot相关配置
# 使用时需要将该配置文件复制到./configs下
from nonebot.default_config import *


### --------------- 插件核心配置 -------------------

# hltv的数据api地址，默认提供的api服务器在国外，之后会出自定义部署hltv api的方法
HLTV_API_ENDPOINT = 'https://hltv-api.netlify.app/.netlify/functions'
# HLTV_API_ENDPOINT = 'https://service-ban7exd9-1256946954.cd.apigw.tencentcs.com/release'

# 启用bot的qq群号，多个群号用英文逗号分隔
BROADCAST_GROUP_LIST = []

# 比赛战报更新检查周期 单位秒
MATCH_RESULT_CHECK_PERIOD = 180

### ------------------- END -------------------

# 管理员的QQ 订阅战队需要有管理员权限
SUPERUSERS = {765892480}  # 多个管理员用英文逗号隔开

## ==== 不用更改 ==== ##
DEBUG = False
HOST = 'match-nonebot'
PORT = 9098
COMMAND_START = {''}
NICKNAME = {''}

def API(api: str) -> str:
    return f'{HLTV_API_ENDPOINT}{api}'
## ================= ##
