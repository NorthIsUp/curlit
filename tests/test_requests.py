import os

import pytest
from curlit.requests import RequestsCurl, RequestsResponseCurl
from requests.models import Response, Request, PreparedRequest

from tests import BaseCurlTest
from tests import fixture

class TestRequestsCurl(BaseCurlTest):

    expected_class = fixture(RequestsCurl, scope='class', autoparam=True)
    request_class = fixture(Request, PreparedRequest, autoparam=True)

    @fixture()
    def req(self, request_class, method, url):
        r =  request_class()
        r.method = method
        r.url = url
        return r


class TestRequestsResponseCurl(TestRequestsCurl):

    expected_class = fixture(RequestsResponseCurl, scope='class', autoparam=True)
    request_class = fixture(Response, autoparam=True)

    @fixture()
    def req(self, request_class, method, url):

        r = Request()
        r.method = method
        r.url = url

        resp =  request_class()
        resp.request = r

        return resp
