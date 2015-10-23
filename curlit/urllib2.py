# -*- coding: utf-8 -*-

from __future__ import absolute_import


from curlit import Curl

try:
    from urllib2 import Request
except ImportError:
    pass
else:
    class Urllib2Request(Curl):

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

    Urllib2Request.register()
