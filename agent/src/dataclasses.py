from dataclasses import dataclass
from typing import Callable, Literal


@dataclass
class Action:
    name: str
    description: str
    function: Callable


@dataclass
class ViteConfig:
    template: Literal[
        "vanilla",
        "vanilla-ts",
        "vue",
        "vue-ts",
        "react",
        "react-ts",
        "react-swc",
        "react-swc-ts",
        "preact",
        "preact-ts",
        "lit",
        "lit-ts",
        "svelte",
        "svelte-ts",
        "solid",
        "solid-ts",
        "qwik",
        "qwik-ts",
    ]
    project_name: str = "myproject"
    package_manager: Literal["npx", "npm", "yarn", "pnpm"] = "npm"
