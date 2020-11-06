# -*- coding: utf-8 -*-
# @File    : keys.py
import hashlib
import json
import time
import redis

from exceptions import NoneKeyUinError
from settings import WX_REDIS_CONFIG
from tools.handle import WeChatWnd
from settings import WX_CHAT_WND_NAME


def delete_key_uin(account_biz):
    redis_server = redis.StrictRedis(connection_pool=redis.ConnectionPool(**WX_REDIS_CONFIG))
    hash_key = hashlib.md5(account_biz.encode("utf-8")).hexdigest()
    redis_server.delete(hash_key)


def _get_key_uin(account_biz):
    redis_server = redis.StrictRedis(connection_pool=redis.ConnectionPool(**WX_REDIS_CONFIG))
    hash_key = hashlib.md5(account_biz.encode("utf-8")).hexdigest()
    return redis_server.get(hash_key)


def get_key_uin(account_biz):
    key_uin = _get_key_uin(account_biz)
    if not key_uin:
        raise NoneKeyUinError("NoneKeyUinError")
    return json.loads(key_uin, encoding="utf-8")


def get_pass_key_and_uin(article_url: str, account_biz: str):
    wx_chat = WeChatWnd(WX_CHAT_WND_NAME)
    key_uin = _get_key_uin(account_biz)

    while not key_uin:
        try:
            wx_chat.send_msg(article_url)
            #wx_chat.click_last_msg()
        except Exception as e:
            print(e.args)
            time.sleep(0.2)
        finally:
            wx_chat.close_web()
            time.sleep(2)
            key_uin = _get_key_uin(account_biz)

    return json.loads(key_uin, encoding="utf-8")


if __name__ == "__main__":
    pass
