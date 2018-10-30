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

        if is_inside_class():
            def autoparam(self, request):
                return request.param
        else:
            def autoparam(request):
                return request.param

        return decorator_factory(autoparam)

    return decorator_factory


def is_inside_class():
    """

    Returns: Class name of encapsulating class or None

    """
    import inspect
    frames = inspect.stack()

    for frame in frames[1:]:
        if frame[3] == "<module>":
            # At module level, go no further
            return
        elif '__module__' in frame[0].f_code.co_names:
            # found the encapsulating class, go no further
            return frame[0].f_code.co_name


class BaseCurlTest(object):

    @fixture()
    def curl_obj(self, req, expected_class):
        c = curlit(req, strify=False)
        assert isinstance(c, expected_class)
        return c

    @pytest.mark.parametrize('indent', [False, True, 0, 2])
    @pytest.mark.parametrize('strify', [False, True])
    def test_curlit_helper(self, indent, strify, expected_class, scheme, netloc, path, query, url, req):
        curl = curlit(req, strify=strify, indent=indent)

        if strify:
            assert url in curl
            assert curl.startswith('curl')
            if indent:
                indentation = ' ' * indent
                for segment in curl.split('--')[:-1]:
                    assert segment.endswith('\\\n' + indentation), '__{}__ does not end with "\\n\\t"'.format(segment)
            else:
                assert '\n' not in curl
        else:
            assert isinstance(curl, expected_class)

    @pytest.mark.parametrize('indent', [0, False, True, 1, 2, 4, 8])
    def test_curlit_obj_indent(self, indent, curl_obj, scheme, netloc, path, query, url, req):
        curl = curl_obj.curl(indent=indent)

        assert url in curl
        assert curl.startswith('curl')

        if indent:
            indentation = ' ' * indent
            for segment in curl.split('--')[:-1]:
                assert segment.endswith('\\\n' + indentation), '__{}__ does not end with "\\n\\t"'.format(segment)
        else:
            assert '\n' not in curl

    def test_Curl_class(self, req, expected_class):
        c = Curl(req)
        assert isinstance(c, expected_class)

    def test_subclass_directly(self, req, expected_class):
        c = expected_class(req)
        assert isinstance(c, expected_class)
