from uagents import Model


class ActionArgs(Model):
    project_name: str
    template: str
    package_manager: str


class Data(Model):
    thought: str
    action: str
    action_args: ActionArgs
    result: str
    response: str


class Request(Model):
    query: str


class Response(Model):
    status: str
    message: str
    data: Data = None
