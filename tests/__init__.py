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

        import inspect
        frames = inspect.stack()

        defined_in_class = (
            len(frames) > 2
            and frames[2][4][0].strip().startswith('class ')
        )

        if defined_in_class:
            def autoparam(self, request):
                return request.param
        else:
            def autoparam(request):
                return request.param

        return decorator_factory(autoparam)

    return decorator_factory


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
