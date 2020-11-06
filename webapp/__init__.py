# -*- coding: utf-8 -*-
# @Author  : xzkzdx
# @File    : __init__.py.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from settings import MYSQL_CONFIG


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

app.debug = True

from webapp.wxapp import wx_app as wx_app_blueprint
app.register_blueprint(wx_app_blueprint)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.errorhandler(400)
def page_400(error):
    return render_template("400.html"), 400


@app.errorhandler(401)
def page_401(error):
    return render_template("401.html"), 401


@app.errorhandler(403)
def page_403(error):
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_404(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_500(error):
    return render_template("500.html"), 500


@app.errorhandler(503)
def page_503(error):
    return render_template("503.html"), 503
