from dataclasses import dataclass
from typing import Callable


@dataclass
class Action:
    name: str
    description: str
    function: Callable
