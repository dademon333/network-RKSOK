from constants import REQUESTS_ENCODING, PROTOCOL, ResponseStatus
from handlers_utils import format_response
from schemas import Response


def test_without_body():
    expected = f'{ResponseStatus.OK.value} {PROTOCOL}\r\n\r\n'.encode(REQUESTS_ENCODING)
    result = format_response(Response(status=ResponseStatus.OK))
    assert expected == result


def test_with_body():
    body = '89012345678'
    expected = f'{ResponseStatus.OK.value} {PROTOCOL}\r\n{body}\r\n\r\n'.encode(REQUESTS_ENCODING)
    result = format_response(Response(status=ResponseStatus.OK, body=body))
    assert expected == result
