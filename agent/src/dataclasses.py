from dataclasses import dataclass
from typing import Callable, Literal


@dataclass
class Action:
    name: str
    description: str
    function: Callable


@dataclass
class ReactConfig:
    project_name: str = "myproject"
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
    package_manager: Literal["npm", "yarn", "pnpm"]
    framework: Literal["vite", "cra"]
    styling: Literal["css", "scss", "tailwind"]
