# uAgents Hack

A lightweight, autonomous agent built using uAgents to facilitate intelligent project scaffolding/initialisation and automation.

[![Built with uAgents](https://img.shields.io/badge/Built%20with-uAgents-blue)](https://github.com/fetch-ai/uAgents)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.x-blue)](https://reactjs.org/)

![Forge Logo](assets/forge.png)

## 🚀 Features

- 🤖 Natural language project creation
- 🎯 Supports multiple frameworks:
  - Django
  - React (Vite/CRA)
  - Vue.js
- ⚙️ Smart configuration handling
- 📦 Automated dependency management
- 🔄 Best practices templates

## Development Setup

### uAgents

Install dependencies

```bash
cd agent
pipenv install
```

Run agent

```bash
pipenv run python -m src.agent
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

![Forge Logo](assets/sequence-diagram.jpg)

## 📝 Example Usage

```bash
# Chat with Forge
"Create a new Django project named chapy"
"Scaffold a React app with TypeScript and SWC"
"Initialize a Vue.js project"
```
