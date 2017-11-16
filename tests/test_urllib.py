import six
from curlit.urllib import UrllibRequest
from tests import BaseCurlTest, fixture

Request = six.moves.urllib.request.Request


class TestRequestsCurl(BaseCurlTest):

    expected_class = fixture(UrllibRequest, scope='class', autoparam=True)

    @fixture()
    def req(self, method, url):
        data = None if method == 'GET' else method
        return Request(url, data=data)
