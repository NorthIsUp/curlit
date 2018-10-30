from tests import fixture
import six

urlunsplit = six.moves.urllib_parse.urlunsplit

method = fixture(GET='GET', POST='POST', NOPE='NOPE', autoparam=True)
scheme = fixture(http='http', https='https', autoparam=True)
netloc = fixture(one='onehost.com', two='twohost.net', autoparam=True)
path = fixture('some/path', autoparam=True)
query = fixture('query=string', autoparam=True)
headers = fixture(
    none={},
    some={
        'Authorization': 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==',
        'Cache-Control': 'no-cache',
        'Content-MD5': 'Q2hlY2sgSW50ZWdyaXR5IQ==',
        'Host': 'en.wikipedia.org:8080',
    },
    alot={
        'A-IM': 'feed',
        'Accept': 'text/html',
        'Accept-Charset': 'utf-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'Accept-Datetime': 'Thu, 31 May 2007 20:35:00 GMT',
        'Access-Control-Request-Method': 'GET',
        'Authorization': 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '348',
        'Content-MD5': 'Q2hlY2sgSW50ZWdyaXR5IQ==',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '$Version=1; Skin=new;',
        'Date': 'Tue, 15 Nov 1994 08:12:31 GMT',
        'Expect': '100-continue',
        'Forwarded': 'for=192.0.2.60;proto=http;by=203.0.113.43',
        'From': 'user@example.com',
        'Host': 'en.wikipedia.org:8080',
        'If-Match': '"737060cd8c284d8af7ad3082f209582d"',
        'If-Modified-Since': 'Sat, 29 Oct 1994 19:43:31 GMT',
        'If-None-Match': '"737060cd8c284d8af7ad3082f209582d"',
        'If-Range': '"737060cd8c284d8af7ad3082f209582d"',
        'If-Unmodified-Since': 'Sat, 29 Oct 1994 19:43:31 GMT',
        'Max-Forwards': '10',
        'Origin': '<nowiki>http://www.example-social-network.com</nowiki>',
        'Proxy-Authorization': 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==',
        'Range': 'bytes=500-999',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
        'Upgrade': 'h2c, HTTPS/1.3, IRC/6.9, RTA/x11, websocket',
        'Via': '1.0 fred, 1.1 example.com (Apache/1.1)',
        'Warning': '199 Miscellaneous warning',
    },
    autoparam=True
)
@fixture()
def url(scheme, netloc, path, query, fragment=None):
    return urlunsplit((scheme, netloc, path, query, fragment))
