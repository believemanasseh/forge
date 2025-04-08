# Forge

A lightweight, autonomous agent built using uAgents to facilitate intelligent project scaffolding/initialisation and automation.

[![tag : innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)](https://innovationlab.fetch.ai/)
![tag:domain/dev tool](https://img.shields.io/badge/domain-colorcode)
[![Live](https://img.shields.io/badge/Live-8A2BE2?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik0yLjI1IDcuNUMxIDcuNSAwIDYuNSAwIDUuMjVDMCA0LjI4MTI1IDAuNjI1IDMuNDM3NSAxLjUgMy4xNDA2MkMxLjUgMy4wOTM3NSAxLjUgMy4wNDY4OCAxLjUgM0MxLjUgMS42MjUgMi42MDkzOCAwLjUgNCAwLjVDNC45MjE4OCAwLjUgNS43MzQzOCAxLjAxNTYyIDYuMTU2MjUgMS43NjU2MkM2LjM5MDYyIDEuNTkzNzUgNi42ODc1IDEuNSA3IDEuNUM3LjgyODEyIDEuNSA4LjUgMi4xNzE4OCA4LjUgM0M4LjUgMy4yMDMxMiA4LjQ1MzEyIDMuMzc1IDguMzkwNjIgMy41NDY4OEM5LjMxMjUgMy43MzQzOCAxMCA0LjU0Njg4IDEwIDUuNUMxMCA2LjYwOTM4IDkuMDkzNzUgNy41IDggNy41SDIuMjVaTTYuNzY1NjIgMy43NjU2MkM2LjkwNjI1IDMuNjI1IDYuOTA2MjUgMy4zOTA2MiA2Ljc2NTYyIDMuMjVDNi42MDkzOCAzLjA5Mzc1IDYuMzc1IDMuMDkzNzUgNi4yMzQzOCAzLjI1TDQuNSA0Ljk4NDM4TDMuNzY1NjIgNC4yNUMzLjYwOTM4IDQuMDkzNzUgMy4zNzUgNC4wOTM3NSAzLjIzNDM4IDQuMjVDMy4wNzgxMiA0LjM5MDYyIDMuMDc4MTIgNC42MjUgMy4yMzQzOCA0Ljc2NTYyTDQuMjM0MzggNS43NjU2MkM0LjM3NSA1LjkyMTg4IDQuNjA5MzggNS45MjE4OCA0Ljc2NTYyIDUuNzY1NjJMNi43NjU2MiAzLjc2NTYyWiIgZmlsbD0id2hpdGUiLz4KPC9zdmc%2BCg%3D%3D)](https://forge.daimones.xyz)
[![Built with uAgents](https://img.shields.io/badge/Built%20with-uAgents-blue)](https://github.com/fetch-ai/uAgents)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.x-blue)](https://reactjs.org/)
[![Django](https://img.shields.io/badge/Django-green?logo=django)](https://www.djangoproject.com/)
[![Svelte](https://img.shields.io/badge/Svelte-orange?logo=svelte)](https://svelte.dev/)
[![Preact](https://img.shields.io/badge/Preact-673AB8?logo=preact)](https://preactjs.com/)
[![Lit](https://img.shields.io/badge/Lit-324FFF?logo=lit)](https://lit.dev/)
[![Solid](https://img.shields.io/badge/Solid-2C4F7C?logo=solid)](https://www.solidjs.com/)
[![Qwik](https://img.shields.io/badge/Qwik-blue?logo=qwik)](https://qwik.builder.io/)
[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)

![Forge](docs/assets/forge.jpg)

## 🚀 Features

- 🤖 Natural language project creation
- 🎯 Supports multiple projects:
  - Django
  - React
  - Svelte
  - Preact
  - Vanilla JS/TS
  - Lit
  - Solid
  - Qwik
  - Vue.js
- ⚙️ Smart configuration handling
- 📦 Automated dependency management
- 🔄 Best practices templates

## Agentverse

- Forge Agent Address: [agent1q255rqw6shtmnwytv4jr2jlcak54s9f25059fpj9st3y4z9ltmywvvvqwgv](https://agentverse.ai/agents/details/agent1q255rqw6shtmnwytv4jr2jlcak54s9f25059fpj9st3y4z9ltmywvvvqwgv)

## Data Models

### Input Data Model

```py
class Request(Model):
    query: str
```

### Output Data Model

```py
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


class Response(Model):
    status: str
    message: str
    data: Optional[Data] = None
```

## Development Setup

### Agent

Install dependencies

```bash
cd agent
pipenv install
```

Run Forge

```bash
pipenv run python -m src.forge
```

Run Assistant

```bash
pipenv run python -m src.assistant
```

### UI

Install dependencies

```bash
cd ui
npm install
```

Run dev server

```bash
npm run dev
```

## 🌐 Architecture

![Sequence diagram](docs/assets/sequence-diagram.jpg)

## 📝 Example Usage

```bash
# Chat with Forge
"Create a new Django project named chapy"
"Scaffold a React app with TypeScript and SWC"
"Initialize a Vue.js project"
```
