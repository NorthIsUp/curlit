from tests import fixture
import six

urlunsplit = six.moves.urllib_parse.urlunsplit

method = fixture(GET='GET', POST='POST', NOPE='NOPE', autoparam=True)
scheme = fixture(http='http', https='https', autoparam=True)
netloc = fixture(one='onehost.com', two='twohost.net', autoparam=True)
path = fixture('some/path', autoparam=True)
query = fixture('query=string', autoparam=True)


@fixture()
def url(scheme, netloc, path, query, fragment=None):
    return urlunsplit((scheme, netloc, path, query, fragment))