# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @File   : apiexceptions.py


class OffsetError(ValueError):
    def __init__(self, *args):
        super(OffsetError, self).__init__(*args)


class RequestError(ValueError):
    def __init__(self, *args):
        super(RequestError, self).__init__(*args)


class KeyExpireError(Exception):
    def __init__(self, *args):
        super(KeyExpireError, self).__init__(*args)


class StatusError(ValueError):
    def __init__(self, *args):
        super(StatusError, self).__init__(*args)


class NoneValueError(ValueError):
    def __init__(self, *args):
        super(NoneValueError, self).__init__(*args)


class ArticleHasBeenDeleteError(ValueError):
    def __init__(self, *args):
        super(ArticleHasBeenDeleteError, self).__init__(*args)


class IPError(ValueError):
    def __init__(self, *args):
        super(IPError, self).__init__(*args)
