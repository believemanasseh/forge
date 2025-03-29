from typing import Any

from uagents import Model


class Request(Model):
    query: str


class Response(Model):
    status: str
    message: str
    data: dict[str, Any] = None
