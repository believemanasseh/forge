from uagents import Model


class Request(Model):
    query: str


class Response(Model):
    id: str
    object: str
    created: int
    model: str
    choices: list
    usage: dict
