import os

import pytest
from curlit.urllib2 import Urllib2Request
from urllib2 import Request

from tests import BaseCurlTest
from tests import fixture


class TestRequestsCurl(BaseCurlTest):

    expected_class = fixture(Urllib2Request, scope='class', autoparam=True)

    @fixture()
    def req(self, method, url):
        data = None if method == 'GET' else method
        return Request(url, data=data)
