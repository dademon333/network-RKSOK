import re
from asyncio import StreamWriter

from constants import PROTOCOL, REQUESTS_ENCODING, RequestCommand
from schemas import Request, Response

_LINE_BREAK_REGEX = re.compile(r'(?<!\r)\n')
# Regex template of valid user request
_REQUEST_REGEX = re.compile(r'(?P<command>[А-Я]+) (?P<argument>.+) РКСОК/1\.0(?:\r\n(?P<body>[\s\S]*))?\r\n\r\n')


def parse_request(request: str) -> Request | None:
    """Parses request to Request model
    Returns Request if request is valid, else - None
    """
    allowed_commands = [
        RequestCommand.GET.value,
        RequestCommand.WRITE.value,
        RequestCommand.DELETE.value
    ]
    match = _REQUEST_REGEX.fullmatch(request)

    if match is None:
        return None
    else:
        match = match.groupdict()

    if len(match['argument']) > 30:
        return None
    if match['command'] not in allowed_commands:
        return None

    if match['body'] is not None:
        match['body'] = match['body'].replace('\r\n', '\n')
    return Request.parse_obj(match)


def format_response(response: Response) -> bytes:
    """Returns server response in valid RKSOK form"""
    if response.body is None:
        return f'{response.status.value} {PROTOCOL}\r\n\r\n'.encode(REQUESTS_ENCODING)
    else:
        body = _LINE_BREAK_REGEX.sub('\r\n', response.body)
        return f'{response.status.value} {PROTOCOL}\r\n{body}\r\n\r\n'.encode(REQUESTS_ENCODING)


async def return_response(response: Response, writer: StreamWriter) -> None:
    """Returns server response to user and close writer"""
    writer.write(format_response(response))
    await writer.drain()
    writer.close()
