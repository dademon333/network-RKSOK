import asyncio
from asyncio import StreamReader, StreamWriter

from constants import ResponseStatus, RequestCommand, REQUESTS_ENCODING
from handlers_utils import parse_request, return_response
from schemas import Response, Request
from services.postgresql import get_psql_cursor
from services.validation_server_client import ApprovalServerClient


async def process_request(reader: StreamReader, writer: StreamWriter) -> None:
    """Reads request, calls its handling and returns response to user
    Entry point of user request handling
    """
    raw_request = await reader.read(2 ** 20)
    raw_request = raw_request.decode(REQUESTS_ENCODING)

    while not raw_request.endswith('\r\n\r\n'):
        try:
            raw_request += (
                await asyncio.wait_for(reader.read(2 ** 20), timeout=10)
            ).decode(REQUESTS_ENCODING)
        except TimeoutError:
            await return_response(
                Response(status=ResponseStatus.INCORRECT_REQUEST),
                writer
            )
            return

    response = await handle_request(raw_request)
    await return_response(response, writer)


async def handle_request(raw_request: str) -> Response:
    """Validates request and routes it to right handler"""
    if (parsed_request := parse_request(raw_request)) is None:
        return Response(status=ResponseStatus.INCORRECT_REQUEST)

    approval_server_response = await ApprovalServerClient(raw_request)\
        .ask_permission_to_handle_request()
    if approval_server_response.status == ResponseStatus.NOT_APPROVED:
        return Response(status=approval_server_response.status, body=approval_server_response.body)

    if parsed_request.command == RequestCommand.GET:
        return await handle_get_request(parsed_request)
    elif parsed_request.command == RequestCommand.WRITE:
        return await handle_write_request(parsed_request)
    elif parsed_request.command == RequestCommand.DELETE:
        return await handle_delete_request(parsed_request)


async def handle_get_request(request: Request) -> Response:
    psql_cursor = get_psql_cursor()
    psql_cursor.execute(
        'SELECT phone FROM phone_numbers WHERE owner_name = %s',
        [request.argument]
    )

    if (number := psql_cursor.fetchone()) is not None:
        return Response(status=ResponseStatus.OK, body=number['phone'])
    else:
        return Response(status=ResponseStatus.NOT_FOUND)


async def handle_write_request(request: Request) -> Response:
    psql_cursor = get_psql_cursor()

    psql_cursor.execute(
        'DELETE FROM phone_numbers WHERE owner_name = %s',
        [request.argument]
    )
    psql_cursor.execute(
        'INSERT INTO phone_numbers (owner_name, phone) VALUES (%s, %s)',
        [request.argument, request.body]
    )
    return Response(status=ResponseStatus.OK)


async def handle_delete_request(request: Request) -> Response:
    psql_cursor = get_psql_cursor()
    psql_cursor.execute(
        'SELECT phone FROM phone_numbers WHERE owner_name = %s',
        [request.argument]
    )

    if psql_cursor.fetchone() is not None:
        psql_cursor.execute(
            'DELETE FROM phone_numbers WHERE owner_name = %s',
            [request.argument]
        )
        return Response(status=ResponseStatus.OK)
    else:
        return Response(status=ResponseStatus.NOT_FOUND)
