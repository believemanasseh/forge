import os

import requests

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")
MODEL = os.getenv("MODEL", "mistral-large-latest")

if not LLM_API_KEY or not LLM_API_URL or not MODEL:
    raise ValueError("LLM_API_KEY and LLM_API_URL and MODEL must be set")


def call_llm(content: str, role: str = "user"):
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a project scaffolder agent. Your task is to help users create and set up new projects by providing templates, configurations, and best practices. Please keep the conversation focused on project scaffolding and boilerplate code generation. If the conversation starts to diverge into unrelated topics, respond with 'I'm not designed for that'.",
            },
            {
                "role": role,
                "content": content,
            },
        ],
        "model": MODEL,
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return response.json()
