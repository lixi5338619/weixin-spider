# -*- coding: utf-8 -*-
# @File    : __init__.py.py
from flask import Blueprint

wx_app = Blueprint(
    "wx_app", __name__, url_prefix="/", template_folder="../templates/weixin/"
)

from webapp.wxapp import views
from webapp.wxapp import selffilter

