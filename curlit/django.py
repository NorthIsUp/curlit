from __future__ import absolute_import

from curlit import Curl

try:
    from django.http.request import HttpRequest
except ImportError:
    pass
else:
    class DjangoCurl(Curl):

        SUPPORTED_TYPES = HttpRequest

        @property
        def headers(self):
            headers = self.request.META.items()
            return (
                (name[5:].replace('_', ' ').title().replace(' ', '-'), value)
                for name, value
                in headers
                if name.startswith('HTTP_')
            )

        @property
        def method(self):
            return self.request.method

        @property
        def absolute_uri(self):
            return self.request.build_absolute_uri()

    DjangoCurl.register()
