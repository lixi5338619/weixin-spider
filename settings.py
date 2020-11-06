# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2020/11/15 11:15
# @File   : settings.py

MONITOR_ERROR = False  # wx_monitor.py容错控制

SLEEP_TIME = 15  # 调用时建议使用的睡眠时间，以免账号被限制，大于等于10
UPDATE_DELAY = 3  # 数据更新速度，不宜过快，建议2秒
UPDATE_STOP = 60  # 数据暂停更新时间

USER_AGENT_WECHAT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"

# autocommit=true  连接断开后，事务没有回滚，残留的锁导致后续的查询报错.
MYSQL_CONFIG =  "mysql://root:lx123#@localhost:3306/weixin_spider?charset=utf8mb4&autocommit=true"


WX_REDIS_CONFIG = {             # \tools\addons.py 中的 WX_REDIS_CONFIG 也需要修改
    'host': '106.53.236.37',
    'password': 'lx123456',
    'port': 6379,
    'db': 0,
    'decode_responses': True,
}

WX_UPDATE_TIME = 60 * 60 * 24 * 1  # 对文章数据更新的频次， 默认一天更新一轮
WX_NOT_UPDATE_TIME = 60 * 60 * 24 * 3  # 停止文章数据更新的最大时间期限， 默认更新三天内的数据

WX_CHAT_WND_NAME = "文件传输助手"  # 微信PC版消息发送窗口
