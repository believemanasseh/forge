import json
from typing import Any

from src.agent import Context
from src.dataclasses import Action
from src.llm import call_llm
from src.tools import scaffold_django, scaffold_react, scaffold_vue

ACTIONS = {
    "scaffold_django": Action(
        name="scaffold_django",
        description="Create a new Django project scaffold",
        function=scaffold_django,
        args=["project_name"],
    ),
    "scaffold_react": Action(
        name="scaffold_react",
        description="Create a new React project scaffold",
        function=scaffold_react,
        args=["project_name"],
    ),
    "scaffold_vue": Action(
        name="scaffold_vue",
        description="Create a new Vue.js project scaffold",
        function=scaffold_vue,
        args=["project_name"],
    ),
}

PROMPT = """You are a project scaffolding assistant. Given the user's request, think through the steps needed and take appropriate actions.

Available actions:
{actions}

If the user's request requires project scaffolding, use one of the actions above.
If the user is asking a question or needs information, respond conversationally without using actions.

Think through this step-by-step:
1) What is the user requesting?
2) Does this require project scaffolding or just information?
3) Choose appropriate response format

Respond in ONE of these two formats:

For project scaffolding:
Thought: [your reasoning]
Action: [action_name]
Action Args: [parameters as JSON]

For information/conversation:
Thought: [your reasoning]
Response: [your helpful response]

Examples:
User: "Create a new Django project called myblog"
Thought: User wants a Django project scaffold with name 'myblog'
Action: scaffold_django
Action Args: {{"project_name": "myblog"}}

User: "What's the difference between Django and Flask?"
Thought: User is asking for information about web frameworks
Response: Django and Flask are both Python web frameworks but have different philosophies. Django is a full-featured framework that provides many built-in features like admin interface, ORM, and authentication. Flask is a lightweight framework that gives you more flexibility in choosing your tools and architecture...

Current conversation:
User: {input}

Remember to respond with Thought/Action/Action Args."""


def parse_llm_response(response: str) -> dict[str, Any]:
    """Parse the LLM's response into a structured dictionary.

    Args:
        response (str): Raw response string from the LLM containing thought, action, and arguments.

    Returns:
        dict[str, Any]: Dictionary containing parsed elements:
            - thought: The reasoning provided by the LLM
            - action: The chosen action name (if any)
            - action_args: Arguments for the action as a dictionary (if any)
            - response: Direct response text (if any)
    """
    lines = response.strip().split("\n")
    result = {}

    for line in lines:
        if line.startswith("Thought:"):
            result["thought"] = line[8:].strip()
        elif line.startswith("Action:"):
            result["action"] = line[7:].strip()
        elif line.startswith("Action Args:"):
            try:
                result["action_args"] = json.loads(line[11:].strip())
            except json.JSONDecodeError:
                result["action_args"] = {}
        elif line.startswith("Response:"):
            result["response"] = line[9:].strip()

    return result


async def begin_react_loop(
    ctx: Context, user_input: str, max_steps: int = 3
) -> dict[str, Any]:
    """Execute the ReAct loop to process user input and perform actions.

    Args:
        ctx (Context): The agent context object
        user_input (str): The user's input text to process
        max_steps (int, optional): Maximum number of iterations. Defaults to 3.

    Returns:
        dict[str, Any]: Dictionary containing:
            - thought: The AI's reasoning about the request
            - action: Name of the action executed, if any
            - result: Result of the executed action, if any
            - response: Text response for informational queries
    """
    step = 0
    result = None

    action_descriptions = "\n".join(
        f"- {action.name}: {action.description}" for action in ACTIONS.values()
    )

    while step < max_steps:
        response = await call_llm(
            PROMPT.format(actions=action_descriptions, input=user_input)
        )

        decision = parse_llm_response(response["choices"][0]["message"]["content"])

        ctx.logger.info(f"Thought: {decision.get('thought')}")

        # Execute action if chosen
        action_name = decision.get("action")
        if action_name and action_name in ACTIONS:
            action = ACTIONS[action_name]
            try:
                result = action.function(ctx=ctx, **decision.get("action_args", {}))
                if result:
                    break
            except Exception as e:
                ctx.logger.error(f"Action failed: {str(e)}")

        step += 1

    return {
        "thought": decision.get("thought"),
        "action": action_name,
        "result": result,
        "response": decision.get("response"),
    }
