from http.client import OK
from typing import Any

import aiohttp

from src.config import get_config

config = get_config()


async def call_llm(content: str, role: str = "user") -> dict[str, Any]:
    """Makes an asynchronous API call to a large language model service.

    This function sends a request to a specified LLM API endpoint with messages containing
    a system prompt and user content. It handles the API communication and error cases.

    Args:
        content (str): The message content to send to the LLM.
        role (str, optional): The role of the message sender. Defaults to "user".

    Returns:
        dict[str, Any]: The JSON response from the LLM API containing the model's output.

    Raises:
        SystemExit: If the API request fails due to connection or response errors.
        aiohttp.ClientResponseError: If the API returns a non-200 status code.

    Example:
        >>> response = await call_llm("Create a new Flask project")
        >>> print(response['choices'][0]['message']['content'])
    """
    headers = {
        "Authorization": f"Bearer {config.LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": f"Your name is {config.NAME}! You are a project scaffolder agent. Your task is to help users create and set up new projects by providing templates, configurations, and best practices. Please keep the conversation focused on project scaffolding and boilerplate code generation. If the conversation starts to diverge into unrelated topics, respond with 'I'm not designed for that'.",
            },
            {
                "role": role,
                "content": content,
            },
        ],
        "model": config.MODEL,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                config.LLM_API_URL, headers=headers, json=data
            ) as response:
                if response.status != OK:
                    error_text = await response.text()
                    raise aiohttp.ClientResponseError(
                        response.request_info,
                        response.history,
                        status=response.status,
                        message=error_text,
                    )
                return await response.json()
    except aiohttp.ClientError as e:
        raise SystemExit(f"API request failed: {str(e)}")
