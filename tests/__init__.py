# -*- coding: utf-8 -*-
from curlit import curlit, Curl
import pytest


def fixture(*args, **kwargs):
    def decorator_factory(func):
        fixture_kwargs = {}
        if 'scope' in kwargs:
            fixture_kwargs['scope'] = kwargs.pop('scope')

        if 'autouse' in kwargs:
            fixture_kwargs['autouse'] = kwargs.pop('autouse')

        if 'params' in kwargs:
            fixture_kwargs['params'] = list(kwargs.pop('params'))

        if 'ids' in kwargs:
            fixture_kwargs['ids'] = list(kwargs.pop('ids'))

        if kwargs:
            fixture_kwargs.setdefault('params', []).extend(kwargs.values())
            fixture_kwargs.setdefault('ids', []).extend(kwargs.keys())

        if args:
            fixture_kwargs.setdefault('params', []).extend(args)

        return pytest.fixture(**fixture_kwargs)(func)

    if kwargs.pop('autoparam', False):

        def autoparam(self, request):
            # self exits just to eat the self argument if autoparam is used
            # inside a class. It will be provided by the self fixture in other cases
            return request.param
        return decorator_factory(autoparam)

    return decorator_factory


@fixture()
def self():
    # to allow autoparam to
    pass

class BaseCurlTest(object):

    @fixture()
    def curl_obj(self, req, expected_class):
        c = curlit(req, strify=False)
        assert isinstance(c.wrapper, expected_class)
        return c

    def test_curlit_helper(self, curl_obj, scheme, netloc, path, query, url):
        curl = str(curl_obj)
        assert url in curl
        assert curl.startswith('curl')

    def test_Curl_class(self, req, expected_class):
        c = Curl(req)
        assert isinstance(c.wrapper, expected_class)

    def test_subclass_directly(self, req, expected_class):
        c = expected_class(req)
        assert isinstance(c, expected_class)