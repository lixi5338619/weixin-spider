# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @File   : models.py

import time
from sqlalchemy.databases import mysql
from webapp import db


class Account(db.Model):
    __tablename__ = "wx_account"
    __table_args__ = {
        "useexisting": True,
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(50))  # 公众号名称
    account_id = db.Column(db.String(30), unique=True)  # 公众号唯一id
    account_biz = db.Column(db.String(20), unique=True)  # 公众号__biz
    account_id_unique = db.Column(db.String(30), unique=True)  # 公众号唯一id
    account_logo = db.Column(db.String(300), unique=True)  # 公众号头像
    account_desc = db.Column(db.String(300))  # 公众号描述
    account_url = db.Column(db.String(500), unique=True)  # 公众号解析链接

    created = db.Column(db.String(20), default=str(int(time.time())))  # 公众号添加时间

    status = db.Column(db.Integer, default=0)  # 状态0-未运行，1-等待中，2-运行中，3-已暂停
    offset = db.Column(db.Integer, default=0)  # 公众号偏移量
    counts = db.Column(db.Integer, default=0)  # 公众号获取的文章数量
    end = db.Column(db.Boolean, default=False)  # 公众号爬取是否完毕
    fail = db.Column(db.Boolean, default=False)  # 公众号有效性

    update = db.Column(db.String(20), default="1356969600")  # 公众号更新时间

    articles = db.relationship("Article", backref="wx_account")

    def __repr__(self):
        return "<Account: %s %s %s %s>" % (self.account_name, self.account_id, self.offset, self.end)


class Article(db.Model):
    __tablename__ = "wx_article"
    __table_args__ = {
        "useexisting": True,
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(200))
    article_author = db.Column(db.String(50))
    article_publish_time = db.Column(db.String(20))
    article_copy_right = db.Column(db.Boolean)
    article_digest = db.Column(db.String(300))
    article_html = db.Column(mysql.MSMediumText)

    article_content_url = db.Column(db.String(500), unique=True)
    article_cover_url = db.Column(db.String(500))
    article_source_url = db.Column(db.String(500))
    article_fail = db.Column(db.Boolean, default=False)  # 文章有效性
    article_done = db.Column(db.Boolean, default=False)  # 文章内容是否抓取
    article_comment_id = db.Column(db.String(20))
    comment_update = db.Column(db.String(20), default="1356969600")  # 公众号更新时间
    read_like_update = db.Column(db.String(20), default="1356969600")  # 公众号更新时间
    read_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)

    comment_count = db.Column(db.Integer, default=0)
    comments = db.relationship("Comment", backref="wx_article")
    account_id = db.Column(db.Integer, db.ForeignKey("wx_account.id"))  # 公众号唯一id

    def __repr__(self):
        return "<Article: id: %s, title: %r, comment_count: %s, read_count: %s, like_count: %s>" % (
            self.id,
            self.article_title,
            self.comment_count,
            self.read_count,
            self.like_count,
        )


class Comment(db.Model):
    __tablename__ = "wx_comment"
    __table_args__ = {
        "useexisting": True,
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, primary_key=True)

    user_name = db.Column(db.String(50))
    user_logo = db.Column(db.String(300))

    content = db.Column(db.String(800))
    datetime = db.Column(db.String(20))

    content_id = db.Column(db.String(30), unique=True)
    like_count = db.Column(db.Integer)

    article_id = db.Column(db.Integer, db.ForeignKey("wx_article.id"))
    reply_list = db.relationship("CommentReply", backref="wx_comment")


class CommentReply(db.Model):
    __tablename__ = "wx_comment_reply"
    __table_args__ = {
        "useexisting": True,
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, primary_key=True)
    reply_uin = db.Column(db.String(20))
    reply_to_uin = db.Column(db.String(20))

    reply_content = db.Column(db.String(300))
    reply_like_count = db.Column(db.Integer)

    reply_datetime = db.Column(db.String(20))
    comment_id = db.Column(db.Integer, db.ForeignKey("wx_comment.id"))


if __name__ == '__main__':
    #db.create_all()
    pass
