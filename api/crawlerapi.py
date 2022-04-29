# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @File   : crawlerapi.py

import re
from json import loads
from urllib.request import Request
from urllib.request import urlopen
from ssl import _create_unverified_context
from urllib.parse import urlencode
import html
import time
# from urllib.parse import unquote, quote
# import base64
from exceptions import KeyExpireError, NoneValueError, IPError, ArticleHasBeenDeleteError
from settings import USER_AGENT, USER_AGENT_WECHAT


def _safe_api(lambda_api):
    def _api(*args, **kwargs):
        api_result = lambda_api(*args, **kwargs)
        if api_result.get("status", 500) == 200:
            return api_result
        raise KeyExpireError("key 已过期")

    return _api


def check_html_api(func):
    def __wrapper(*args, **kwargs):
        res_html = func(*args, **kwargs)
        if '该内容已被发布者删除' in res_html:
            raise ArticleHasBeenDeleteError('该文章链接已被删除')
        if '此内容因违规无法查看' in res_html:
            raise ArticleHasBeenDeleteError('该文章链接因违规无法查看')
        if '此内容被投诉且经审核涉嫌侵权' in res_html:
            raise ArticleHasBeenDeleteError('此内容被投诉且经审核涉嫌侵权，无法查看。')
        if '访问过于频繁，请用微信扫描二维码进行访问' in res_html:
            raise IPError('当前ip已无法访问')
        if '此内容因涉嫌违反相关法律法规' in res_html:
            raise ArticleHasBeenDeleteError('此内容因涉嫌违反相关法律法规，无法查看。')
        if '相关的内容无法进行查看' in res_html:
            raise ArticleHasBeenDeleteError('此内容被多人投诉，相关的内容无法进行查看。')
        return res_html

    return __wrapper


@check_html_api
def get_html_api(article_url: str, use_key: bool = False, **kwargs):
    """
    :param article_url: 带参数的历史文章链接
    :param use_key: 是否使用key
    :param kwargs: key && uin
    :return:
    """
    if use_key:
        article_url = article_url + '&key={key}&ascene=1&uin={uin}'.format(**kwargs)
    request = Request(article_url, headers={
        "User-Agent": USER_AGENT_WECHAT,
    })
    req_resp = urlopen(request, context=_create_unverified_context())
    return html.unescape(req_resp.read().decode())


def get_platform_info_from_url(info_uri: str):
    request = Request(info_uri, headers={
        "User-Agent": USER_AGENT_WECHAT,
    })
    req_resp = urlopen(request, context=_create_unverified_context())
    html_content = html.unescape(req_resp.read().decode())
    meta_values = re.findall(r"<span class=\"profile_meta_value\">(.*?)</span>", html_content)
    wx_id_unique = re.search(r"user_name = \"([\w-]+)\";", html_content).group(1)
    #wx_bizs = re.search(r"var biz = \"([\w=]*)\"\|\|\"([\w=]*)\";", html_content).groups()
    wx_bizs = re.search(r"var biz = \"([\w=]*)\" \|\| \"([\w=]*)\";", html_content).groups()
    return {
        "account_name": re.search(r"nickname = \"([\w-]+)\"", html_content).group(1),
        "account_id": meta_values[0] if meta_values[0] else wx_id_unique,
        "account_biz": wx_bizs[0] if wx_bizs[0] else wx_bizs[1],
        "account_id_unique": wx_id_unique,
        "account_logo": re.search(r"head_?img = \"(https?:\/\/wx.qlogo.cn/mmhead/[\w\/]+)\"", html_content).group(1),
        "account_desc": meta_values[1],
        "account_url": info_uri,
        "created": f"{int(time.time())}",
    }


def get_article_comment_id_api(article_url: str):
    request = Request(article_url, headers={
        "User-Agent": USER_AGENT_WECHAT,
    })
    req_resp = urlopen(request, context=_create_unverified_context())
    html_content = req_resp.read().decode()
    try:
        _comment_id = re.search(r"comment_id = \"(\d*)\"", html_content).group(1)
    except AttributeError as e:
        print(e.args)
        raise NoneValueError('正则匹配错误')
    return _comment_id


@_safe_api
def get_history_api(**kwargs):
    """
    获取公众号历史文章的 api 接口
    :param biz: 公众号的识别码
    :param uin: 登陆的微信账号的识别码
    :param key: 获取历史信息必要的 key
    :param offset: 偏移量
    :param count: 历史图文发布的次数，一次是多图文，最大值10，即获取偏移量后最近10次发布的所有图文消息
    :return: 解析好的json格式字典
    """

    def match_item_info(item_dict, article_publish_time):
        """
        文章详情获取
        :param item_dict: 包含单个文章信息的字典
        :return: 结构化的文章信息
        """
        article_title = item_dict.get('title', '')
        article_author = item_dict.get("author", "")
        article_digest = item_dict.get("digest", "")
        article_content_url = item_dict.get("content_url", "").replace("&amp;", "&")
        article_cover_url = item_dict.get("cover", "").replace("&amp;", "&")
        article_source_url = item_dict.get("source_url", "").replace("&amp;", "&")
        copyright_stat = item_dict.get("copyright_stat", 0)
        copy_right = 1 if copyright_stat == 11 else 0
        return {
            "article_title": article_title,  # 文章标题
            "article_author": article_author,  # 文章作者
            "article_publish_time": article_publish_time,  # 文章发布时间
            "article_digest": article_digest,  # 文章摘要
            "article_content_url": article_content_url,  # 文章详情链接
            "article_cover_url": article_cover_url,  # 封面图片链接
            "article_source_url": article_source_url,  # 源文链接
            "article_copy_right": copy_right,  # 原创
        }

    uri_api = "http://mp.weixin.qq.com/mp/profile_ext"
    form_data = {
        "action": "getmsg",
        "__biz": kwargs["biz"],
        "offset": kwargs["offset"],
        "count": kwargs.get("count", 10),
        "uin": kwargs["uin"],
        "key": kwargs["key"],
        "f": "json",
    }
    request = Request(uri_api, data=urlencode(form_data).encode(), headers={
        "User-Agent": USER_AGENT,
    })
    resp_json = loads(urlopen(request, context=_create_unverified_context()).read().decode(), encoding="utf-8")
    article_infos = []
    next_offset = h_offset = kwargs["offset"]
    ending = False
    status = 200 if resp_json.get("errmsg", "") == "ok" else 500
    if status == 200:
        next_offset = resp_json.get("next_offset", -1)
        if next_offset == h_offset:
            ending = True
        if next_offset == -1:
            next_offset = h_offset
            status = 500
        general_msg_list = resp_json.get("general_msg_list", "")
        if general_msg_list and status == 200:
            general_msg_list = loads(general_msg_list, encoding="utf-8").get('list', [])
            for general_msg in general_msg_list:
                publish_time = general_msg["comm_msg_info"].get("datetime", 0)
                app_msg_ext_info = general_msg.get("app_msg_ext_info", {})
                article_infos.append(match_item_info(app_msg_ext_info, publish_time))

                item_list = app_msg_ext_info.get('multi_app_msg_item_list', [])
                for each_item in item_list:
                    article_infos.append(match_item_info(each_item, publish_time))

        else:
            status = 500
            next_offset = h_offset

    return {
        "status": status,  # api使用状态
        "biz": kwargs["biz"],  # 公众号__biz标识
        "uin": kwargs["uin"],  # app登录用户的必要uin参数
        "cur_offset": h_offset,  # 当前请求的偏移量
        "next_offset": next_offset,  # 下一次请求的偏移量offset
        "key": kwargs["key"],  # api必备的app key
        "results": {
            "article_count": len(article_infos),  # 获取的文章数量
            "article_infos": article_infos,  # 获取的全部文章
        },
        "ending": ending  # 是否历史文章爬取完毕，依据offset
    }


@_safe_api
def get_article_comments_api(**kwargs):
    uri_api = "https://mp.weixin.qq.com/mp/appmsg_comment"
    form_data = {
        "action": "getcomment",
        "__biz": kwargs["biz"],
        # "appmsgid": kwargs.get("msg_id", ""),
        #"idx": kwargs.get("idx", ""),
        "pass_ticket":kwargs.get("pass_ticket",""),
        "comment_id": kwargs["comment_id"],
        "offset": kwargs.get("limit", 0),
        "limit": kwargs.get("limit", 100),
        "uin": kwargs["uin"],
        "key": kwargs["key"],
        "f": "json",
    }

    """
    if not form_data.get("appmsgid", ""):
        form_data.pop("appmsgid")
    if not form_data.get("idx", ""):
        form_data.pop("idx")
    """
    request = Request(uri_api + "?" + urlencode(form_data), headers={
        "User-Agent": USER_AGENT,
    })
    resp_json = loads(urlopen(request, context=_create_unverified_context()).read().decode(), encoding="utf-8")

    comments = []
    status = 200 if resp_json.get('base_resp', {}).get("errmsg", "") == "ok" else 500
    if status == 200:
        for elected_comment in resp_json.get('elected_comment', []):
            comments.append({
                "_id": elected_comment.get("id", ""),
                "_my_id": elected_comment.get("my_id", ""),
                "user_name": elected_comment.get("nick_name", ""),
                "user_logo": elected_comment.get("logo_url", ""),
                "content": elected_comment.get("content", ""),
                "datetime": str(elected_comment.get("create_time", "")),
                "content_id": str(elected_comment.get("content_id", "")),
                "like_count": int(elected_comment.get("like_num", 0)),
                "reply_list": [
                    {
                        "reply_uin": reply.get("uin", ""),
                        "reply_to_uin": reply.get("to_uin", ""),
                        "reply_content": reply.get("content", ""),
                        "reply_datetime": str(reply.get("create_time", "")),
                        "reply_like_count": str(reply.get("reply_like_num", 0)),
                    } for reply in elected_comment.get("reply", {}).get("reply_list", [])
                ]
            })
    return {
        "status": status,  # api使用状态
        "biz": kwargs["biz"],  # 公众号__biz标识
        "msg_id": kwargs.get("msg_id", ""),  # 文章id
        "idx": kwargs.get("idx", ""),  # 文章所在图文位置
        "comment_id": kwargs["comment_id"],  # 评论id
        "uin": kwargs["uin"],  # app登录用户的必要uin参数
        "key": kwargs["key"],  # api必备的app key
        "results": {
            "comment_count": len(comments),  # 获取的文章数量
            "comments": comments,  # 获取的全部文章
        },
    }


@_safe_api
def get_article_read_like_api(**kwargs):
    uri_api = "https://mp.weixin.qq.com/mp/getappmsgext"
    request = Request(uri_api, data=urlencode({
        "uin": kwargs["uin"],
        "key": kwargs["key"],
        "__biz": kwargs["biz"],
        "mid": kwargs["mid"],
        "sn": kwargs["sn"],
        "idx": kwargs["idx"],
        "appmsg_type": "9",
        # "comment_id": kwargs["comment_id"],
        "is_only_read": "1",
        "f": "json",
    }).encode(), headers={
        "User-Agent": USER_AGENT_WECHAT,
    })
    resp_json = loads(urlopen(request, context=_create_unverified_context()).read().decode(), encoding="utf-8")
    status = 200 if resp_json.get("appmsgstat", "") else 500
    return {
        "status": status,  # api使用状态
        "results": {
            "read_count": int(resp_json.get("appmsgstat", {}).get("read_num", 0)),
            "like_count": int(resp_json.get("appmsgstat", {}).get("like_num", 0)),
        } if status == 200 else {}
    }


def split_article_url2mis(article_url: str):
    return {
        "mid": re.search(r"mid=(\d+)&?", article_url).group(1),
        "sn": re.search(r"sn=(\w+)&?", article_url).group(1),
        "idx": re.search(r"idx=(\d)&?", article_url).group(1),
    }


def get_qrcode_url_api(article_url="", **kwargs):
    """
    "mid": kwargs["mid"],
    "sn": kwargs["sn"],
    "idx": kwargs["idx"],
    """
    url_api = 'https://mp.weixin.qq.com/mp/qrcode?scene=10000005&'
    if article_url:
        return url_api + "&".join(k + "=" + v for k, v in split_article_url2mis(article_url).items())
    return url_api + "&".join(k + "=" + v for k, v in kwargs.items())


def get_access_key_api():
    #open_system_proxy("127.0.0.1:8888")
    #close_system_proxy()
    return


