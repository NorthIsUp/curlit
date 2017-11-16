# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six
from curlit import Curl

Request = six.moves.urllib.request.Request


class UrllibRequest(Curl):

    SUPPORTED_TYPES = Request

    @property
    def headers(self):
        return self.request.headers.items()

    @property
    def method(self):
        return self.request.get_method()

    @property
    def absolute_uri(self):
        return self.request.get_full_url()


UrllibRequest.register()
