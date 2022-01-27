from enum import Enum

PROTOCOL = 'РКСОК/1.0'
REQUESTS_ENCODING = 'UTF-8'


class RequestCommand(Enum):
    """Commands specified in RKSOK specs for requests"""
    GET = 'ОТДОВАЙ'
    WRITE = 'ЗОПИШИ'
    DELETE = 'УДОЛИ'
    ASK_PERMISSION = 'АМОЖНА?'


class ResponseStatus(Enum):
    """Response statuses specified in RKSOK specs for responses"""
    OK = 'НОРМАЛДЫКС'
    APPROVED = 'МОЖНА'
    NOT_FOUND = 'НИНАШОЛ'
    NOT_APPROVED = 'НИЛЬЗЯ'
    INCORRECT_REQUEST = 'НИПОНЯЛ'
