# -*- coding: utf-8 -*-
# @Author  : xzkzdx
# @File    : momitorexceptions.py


class NoneKeyUinError(ValueError):
    def __init__(self, *args):
        super(NoneKeyUinError, self).__init__(*args)


