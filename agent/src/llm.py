from typing import Any

from ollama import AsyncClient, ChatResponse, ResponseError
from uagents import Context

from src.config import get_config

config = get_config()
client = AsyncClient()


async def call_llm(ctx: Context, content: str, role: str = "user") -> dict[str, Any]:
    """Makes an asynchronous API call to a large language model service.

    This function sends a request to a specified LLM API endpoint with messages containing
    a system prompt and user content. It handles the API communication and error cases.

    Args:
        ctx (Context): The agent context object.
        content (str): The message content to send to the LLM.
        role (str, optional): The role of the message sender. Defaults to "user".

    Returns:
        dict[str, Any]: The JSON response from the LLM API containing the model's output.

    Raises:
        ResponseError: If the request could not be fulfilled.

    Example:
        >>> response = await call_llm("Create a new Flask project")
        >>> print(response)
    """
    data = {
        "messages": [
            {
                "role": "system",
                "content": f"Your name is {config.NAME}! Incase the user asks what your name is, always respond. You are a project scaffolder agent. Your task is to help users create and set up new projects by providing templates, configurations, and best practices. Please keep the conversation focused on project scaffolding and boilerplate code generation. If the conversation starts to diverge into unrelated topics, respond with 'I'm not designed for that'.",
            },
            {
                "role": role,
                "content": content,
            },
        ],
        "model": config.MODEL,
    }

    try:
        response: ChatResponse = await client.chat(
            model=data["model"], messages=data["messages"]
        )
        return response.message.content
    except ResponseError as e:
        ctx.logger.error(f"LLM API call failed: {str(e)}")
        raise ResponseError(f"Error: Failed to get response from LLM - {str(e)}") from e
