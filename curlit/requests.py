from __future__ import absolute_import

from curlit import Curl

try:
    from requests.models import Response, Request, PreparedRequest
except ImportError:
    pass
else:
    class RequestsCurl(Curl):

        SUPPORTED_TYPES = (Request, PreparedRequest)

        @property
        def headers(self):
            return (self.request.headers or {}).items()

        @property
        def method(self):
            return self.request.method

        @property
        def absolute_uri(self):
            return self.request.url

        @property
        def data(self):
            if hasattr(self.request, 'body'):
                return self.request.body
            if hasattr(self.request, 'data'):
                return self.request.data

    RequestsCurl.register()

    class RequestsResponseCurl(RequestsCurl):

        SUPPORTED_TYPES = Response

        def __init__(self, *args, **kwargs):
            super(RequestsResponseCurl, self).__init__(*args, **kwargs)
            self.request = self.request.request

    RequestsResponseCurl.register()
