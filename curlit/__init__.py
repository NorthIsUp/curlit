# -*- coding: utf-8 -*-
from __future__ import absolute_import

from curlit.base import Curl

from .django import *
from .requests import *
from .urllib import *


def curlit(request, strify=True):
    c = Curl(request)
    if strify:
        c = str(c)
    return c
