# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @File   : views.py

from . import wx_app
from webapp.models import Account, Article, Comment
from webapp import db

from urllib.request import urlopen

from flask import render_template, request, redirect, url_for, make_response

from api import get_platform_info_from_url


@wx_app.route("/", methods=['GET'])
def wx_index():
    page = int(request.args.to_dict().get("page", 1))
    page_data = Account.query.order_by(
        Account.created.desc()
    ).paginate(page=page, per_page=5)
    return render_template("wx-index.html", page_data=page_data)


@wx_app.route("/add/", methods=["GET"])
def wx_add():
    wx_uri = request.values.to_dict().get("wx_uri")
    wx_info = get_platform_info_from_url(wx_uri)
    print(wx_info)
    account_count = Account.query.filter_by(account_id_unique=wx_info['account_id_unique']).count()
    if account_count == 1:
        return redirect(url_for("wx_app.wx_index"))
    account = Account(**wx_info)
    db.session.add(account)
    db.session.commit()
    return redirect(url_for("wx_app.wx_index"))


@wx_app.route("/account/", methods=["GET"])
def wx_account():
    account_id = int(request.args.to_dict().get("id", 0))
    page = int(request.args.to_dict().get("page", 1))
    if account_id <= 0:
        return redirect(url_for("wx_app.wx_index"))
    account = Account.query.get(account_id)
    articles = Article.query.filter_by(
        account_id=account_id
    ).order_by(
        Article.article_publish_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template("wx-account.html", account=account, articles=articles)


@wx_app.route("/article/", methods=["GET"])
def wx_article():
    article_id = int(request.args.to_dict().get("id", 0))
    article = Article.query.get(article_id)
    comments = Comment.query.filter_by(
        article_id=article_id
    ).all()
    if article_id <= 0:
        return redirect(url_for("wx_app.wx_index"))
    return render_template("wx-article.html", article=article, comments=comments)


@wx_app.route("/operate/", methods=["GET"])
def wx_operate():
    account_id = int(request.args.to_dict().get("id", 0))
    account_count = Account.query.filter_by(id=account_id).count()
    if account_count != 1:
        return redirect(url_for("wx_app.wx_index"))
    account = Account.query.get(account_id)
    operate = request.args.to_dict().get("operate", "")
    if operate in ["0", "1", "2", "3", "4"]:
        account.status = int(operate)
        db.session.add(account)
        db.session.commit()
    return redirect(url_for("wx_app.wx_index"))


@wx_app.route("/wx_article/", methods=["GET"])
def wx_article_iframe():
    article_id = int(request.args.to_dict().get("id", 0))
    if article_id <= 0:
        return ""
    article = Article.query.get(article_id)
    return article.article_html


@wx_app.route("/wx_images/", methods=["GET"])
def wx_images():
    from ssl import _create_unverified_context
    url = request.args.to_dict().get("url", "")
    img = urlopen(url, context=_create_unverified_context())
    resp = make_response(img.read())
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


