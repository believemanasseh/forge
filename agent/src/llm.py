from typing import Any

from openai import AsyncOpenAI, OpenAIError
from uagents import Context

from src.config import get_config

config = get_config()


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
        OpenAIError: If the OpenAI API request fails.
        Exception: For any other unexpected errors.

    Example:
                >>> response = await call_llm("Create a new Flask project")
                >>> print(response.choices[0].message.content)
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
        client = AsyncOpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_API_URL)
        response = await client.chat.completions.create(
            model=data["model"],
            messages=data["messages"],
            stream=False,
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        ctx.logger.error(f"OpenAI API request failed: {str(e)}")
        raise
    except Exception as e:
        ctx.logger.error(f"Unexpected error: {str(e)}")
        raise
