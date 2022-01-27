from constants import RequestCommand
from handlers_utils import parse_request
from schemas import Request


def test_request_without_body():
    user_request = 'УДОЛИ Иван Хмурый РКСОК/1.0\r\n\r\n'
    expected = Request(
        command=RequestCommand.DELETE,
        argument='Иван Хмурый',
        body=None
    )
    result = parse_request(user_request)
    assert result == expected


def test_request_with_body():
    user_request = 'ЗОПИШИ Иван Хмурый РКСОК/1.0\r\n89012345678\r\n\r\n'
    expected = Request(
        command=RequestCommand.WRITE,
        argument='Иван Хмурый',
        body='89012345678'
    )
    result = parse_request(user_request)
    assert result == expected


def test_request_with_multiline_body():
    user_request = 'ЗОПИШИ Иван Хмурый РКСОК/1.0\r\n89012345678 — мобильный\r\n02 — рабочий\r\n\r\n'
    expected = Request(
        command=RequestCommand.WRITE,
        argument='Иван Хмурый',
        body='89012345678 — мобильный\n02 — рабочий'
    )
    result = parse_request(user_request)
    assert result == expected



def test_incorrect_command():
    user_request = '12345 Иван Хмурый РКСОК/1.0\r\n\r\n'
    expected = None
    result = parse_request(user_request)
    assert result == expected


def test_forbidden_command():
    user_request = 'АМОЖНА? Иван Хмурый РКСОК/1.0\r\n\r\n'
    expected = None
    result = parse_request(user_request)
    assert result == expected


def test_broken_request():
    user_request = 'ОТДОВАЙИванов РКСОК/1.0\r\n\r\n'
    expected = None
    result = parse_request(user_request)
    assert result == expected


def test_no_request_argument():
    user_request = 'ОТДОВАЙ РКСОК/1.0\r\n\r\n'
    expected = None
    result = parse_request(user_request)
    assert result == expected


def test_too_long_name():
    name = 'a' * 31
    user_request = f'ОТДОВАЙ {name} РКСОК/1.0\r\n\r\n'
    expected = None
    result = parse_request(user_request)
    assert result == expected
