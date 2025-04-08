from typing import Optional

from uagents import Model


class ActionArgs(Model):
    project_name: str
    template: Optional[str] = None
    package_manager: Optional[str] = None


class Data(Model):
    thought: str
    action: Optional[str] = None
    action_args: Optional[ActionArgs] = None
    result: Optional[str] = None
    response: Optional[str] = None


class Request(Model):
    query: str


class Response(Model):
    status: str
    message: str
    data: Optional[Data] = None
