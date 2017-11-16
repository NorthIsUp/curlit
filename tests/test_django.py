import os

from curlit.django import DjangoCurl
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from tests import BaseCurlTest, fixture


SECRET_KEY = 'hi'
CACHES = {}
ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('SSL_ON', '1')


class TestDjangoHttpRequestCurl(BaseCurlTest):

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)

    @fixture()
    def expected_class(self):
        return DjangoCurl

    @fixture()
    def req(self, scheme, method, netloc, path, query):
        secure = scheme == 'https'
        req = HttpRequest()
        req.method = method
        req.path = netloc + '/' + path
        req.META['QUERY_STRING'] = query
        req.META['SERVER_NAME'] = netloc
        req.META['SERVER_PORT'] = 443 if secure else 80
        req.META['SSL_ON'] = str(1 if secure else 0)
        return req


class TestDjangoWSGIRequestCurl(BaseCurlTest):

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)

    @fixture()
    def environ(self, scheme, method, netloc, path, query):
        return {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': query,
            'CONTENT_TYPE': '',
            'CONTENT_LENGTH': '',
            'SERVER_NAME': netloc,
            'SERVER_PORT': '',
            'SERVER_PROTOCOL': scheme,
            'wsgi.version': '',
            'wsgi.url_scheme': scheme,
            'wsgi.input': '',
            'wsgi.errors': '',
            'wsgi.multithread': '',
            'wsgi.multiprocess': '',
            'wsgi.run_once': '',
        }

    @fixture(scope='class')
    def expected_class(self):
        return DjangoCurl

    @fixture()
    def req(self, scheme, method, netloc, path, query, environ):
        secure = scheme == 'https'
        req = WSGIRequest(environ)
        req.method = method
        req.path = netloc + '/' + path
        req.META['QUERY_STRING'] = query
        req.META['SERVER_NAME'] = netloc
        req.META['SERVER_PORT'] = 443 if secure else 80
        req.META['SSL_ON'] = str(1 if secure else 0)
        return req
