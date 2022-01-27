from pydantic import BaseModel

from constants import RequestCommand, ResponseStatus


class Request(BaseModel):
    """User request model"""
    command: RequestCommand
    argument: str
    body: str | None


class Response(BaseModel):
    """Server response model"""
    status: ResponseStatus
    body: str | None = None


class ApprovalServerResponse(BaseModel):
    """RKSOK approval server response model"""
    status: ResponseStatus
    body: str | None
