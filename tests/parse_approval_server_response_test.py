from constants import ResponseStatus
from schemas import ApprovalServerResponse
from services.validation_server_client import ApprovalServerClient


def test_response_without_body():
    response = 'МОЖНА РКСОК/1.0\r\n\r\n'
    expected = ApprovalServerResponse(
        status=ResponseStatus.APPROVED,
        body=None
    )
    result = ApprovalServerClient(...).parse_response(response)
    assert result == expected


def test_response_with_body():
    response = 'НИЛЬЗЯ РКСОК/1.0\r\nЧто ещё за Иван Хмурый такой? Он тебе зачем?\r\n\r\n'
    expected = ApprovalServerResponse(
        status=ResponseStatus.NOT_APPROVED,
        body='Что ещё за Иван Хмурый такой? Он тебе зачем?'
    )
    result = ApprovalServerClient(...).parse_response(response)
    assert result == expected
