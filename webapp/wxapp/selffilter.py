# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @File   : selffilter.py

import re
import time
from pyquery import PyQuery
from base64 import b64decode
from webapp import app

self_env = app.jinja_env


def dot_string(string, max_len: int = 15):
    return string[:max_len] + ".." if len(string) > max_len else string


def biz_to_short(biz):
    return str(b64decode(biz), encoding="utf-8")


def timestamp2time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))


def data_src(html):
    html = html.replace("visibility: hidden;", "")
    dom = PyQuery(html)
    for img in dom("img"):
        url = img.get('data-src', "")
        if not url:
            url = img.get('src', "")
        if url:
            img.set("src", "/wx_images/?&url=" + url)
    # content_html = re.sub(r'data-src="https?://mmbiz', 'src="https://mmbiz', content_html)
    # return re.sub(r"src=\"", "src=\"/wx/wx_images/?&url=", content_html)
    return dom


def time2timestamp(date_time):
    return int(time.mktime(date_time.timetuple()))


self_env.filters["timestamp2time"] = timestamp2time
self_env.filters["dot_string"] = dot_string
self_env.filters["biz_to_short"] = biz_to_short
self_env.filters["data_src"] = data_src

