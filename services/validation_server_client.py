import asyncio
import re

from constants import PROTOCOL, REQUESTS_ENCODING, RequestCommand
from schemas import ApprovalServerResponse


class ApprovalServerClient:
    """Client for sending requests to RKSOK approval server"""
    _RESPONSE_REGEX = re.compile(r'(?P<status>[А-Я]+) РКСОК/1\.0(?:\r\n(?P<body>[\s\S]*))?\r\n\r\n')

    def __init__(self, request: str):
        self._domain = 'vragi-vezde.to.digital'
        self._port = 51624
        self._raw_request = request

        self._raw_response = None

    @property
    def raw_request(self) -> str:
        return self._raw_request

    @property
    def raw_response(self) -> str | None:
        return self._raw_response

    async def ask_permission_to_handle_request(self) -> ApprovalServerResponse:
        """Asks approval server for permission to handle request
        Returns response in parsed form
        """
        response = await self._send_request()
        return self.parse_response(response)

    def parse_response(self, response: str) -> ApprovalServerResponse | None:
        """Parses server response and returns in ApprovalServerResponse form"""
        match = self._RESPONSE_REGEX.fullmatch(response)
        if match is None:
            return None
        else:
            match = match.groupdict()

        if match['body'] is not None:
            match['body'] = match['body'].replace('\r\n', '\n')
        return ApprovalServerResponse.parse_obj(match)

    def _format_request(self) -> bytes:
        """Returns raw request in valid RKSOK form"""
        return f'{RequestCommand.ASK_PERMISSION} {PROTOCOL}\r\n{self._raw_request}\r\n\r\n'.encode(REQUESTS_ENCODING)

    async def _send_request(self) -> str:
        """Sends request to approval server and returns response in raw form"""
        reader, writer = await asyncio.open_connection(self._domain, self._port)
        writer.write(self._format_request())
        await writer.drain()

        response = await reader.read(2 ** 20)
        response = response.decode(REQUESTS_ENCODING)
        self._raw_response = response
        return response
