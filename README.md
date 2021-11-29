# csgo-match-forwarding
Forwarding csgo pro match record by qq bot


## 特性 | Feature

- [x] 自定义订阅战队
- [x] QQ机器人转发战报
- [x] 基于nonebot v1，方便插件移植
- [x] docker部署，易于上手

## 部署 | Deploy

支持两种方式的部署：**docker部署**和**手动部署**

> 如果你不熟悉nonebot或现有nonebot项目不是v1版本，可以考虑docker部署；
> 
> 如果你已有nonebot v1项目，可以只移植插件文件和配置文件；

### 基于docker的部署

该部分包含了QQ机器人的容器部署，如果你已有可用的机器人，考虑使用手动部署的方式。

1. 【**安装docker和docker-compose**】 参考[**csgowiki文档库**](https://docs.csgowiki.top/message-channel/quick_start/#%E5%AE%89%E8%A3%85docker%E5%92%8Cdocker-compose)
2. 【**拉取仓库**】 
    ```bash
    git clone https://github.com/hx-w/csgo-match-forwarding.git
    ```
3. 【**修改配置**】
    ```bash
    # 进入工作目录
    cd csgo-match-forwarding/

    # 拷贝配置模板到configs文件夹下，接下来的配置都在configs下更改
    cp -r configs_template/ configs/

    # 更改configs/go-cqhttp.yml       将qq机器人的账号填入uid即可
    # 更改configs/nonebot_config.py   按文件中的注释修改
    # 其他文件不必要修改
    ```
4. 【**启动容器并验证**】
    ```bash
    # 在工作目录下启动容器组，如果出现权限错误，请使用管理员权限启动
    docker-compose up -d

    # 查看`match-gocq`容器的日志，如果出现二维码请用对应账号扫码登录qq机器人
    docker logs -f match-gocq

    # 按CTRL-C退出日志
    ```


### 手动部署

## 使用方法 | Usage

## 反馈 | Feedback