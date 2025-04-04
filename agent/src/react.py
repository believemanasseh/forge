import json
from typing import Any

from src.agent import Context
from src.dataclasses import Action, ViteConfig
from src.llm import call_llm
from src.tools import scaffold_django, scaffold_vite

ACTIONS = {
    "scaffold_django": Action(
        name="scaffold_django",
        description="Create a new Django project scaffold",
        function=scaffold_django,
    ),
    "scaffold_vite": Action(
        name="scaffold_vite",
        description="Create a new React, Vue, Svelte, Preact, Solid, Svelte, Qwik, Lit and Vanilla JavaScript/TypeScript scaffold",
        function=scaffold_vite,
    ),
}

PROMPT = """You are a project scaffolding assistant. Given the user's request, think through the steps needed and take appropriate actions.

Available actions:
{actions}

Configuration Options:
1. Frontend Templates:
   - React: ["react", "react-ts", "react-swc", "react-swc-ts"]
   - Vue: ["vue", "vue-ts"]
   - Others: ["svelte", "svelte-ts", "preact", "preact-ts", "lit", "lit-ts", "solid", "solid-ts", "qwik", "qwik-ts"]
   - Basic: ["vanilla", "vanilla-ts"]

2. Package Managers: ["npx", "npm", "yarn", "pnpm"]

When scaffolding a frontend project, you must include both template and package manager in your response.

If the user's request requires project scaffolding, use one of the actions above.
If the user is asking a question or needs information, respond conversationally without using actions.

Think through this step-by-step:
1) What is the user requesting?
2) Does this require project scaffolding or just information?
3) Choose appropriate response format

Respond in ONE of these formats:

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

User: "Set up a Vue project using pnpm"
Thought: User wants a Vue.js project using pnpm package manager
Action: scaffold_vite
Action Args: {{"project_name": "my-vue-app", "template": "vue", "package_manager": "pnpm"}}

User: "Create a Svelte TypeScript project with Yarn"
Thought: User wants a Svelte project with TypeScript and Yarn
Action: scaffold_vite
Action Args: {{"project_name": "my-svelte-app", "template": "svelte-ts", "package_manager": "yarn"}}


User: "What's the difference between Django and Flask?"
Thought: User is asking for information about web frameworks
Response: Django and Flask are both Python web frameworks but have different philosophies. Django is a full-featured framework that provides many built-in features like admin interface, ORM, and authentication. Flask is a lightweight framework that gives you more flexibility in choosing your tools and architecture...

Current conversation:
User: {input}

Remember to:
1. Respond with Thought/Action/Action Args or Thought/Response.
2. For frontend projects, infer template type from user request (default to Vanilla JavaScript if not specified)
3. For frontend projects, use specified package manager or default to npm
"""


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
                result["action_args"] = json.loads(line[13:].strip())
                result["project_name"] = result["action_args"].get("project_name")
                result["template"] = result["action_args"].get("template")
                result["package_manager"] = result["action_args"].get("package_manager")
            except json.JSONDecodeError:
                result["action_args"] = {}
                result["project_name"] = "myproject"
                result["template"] = "vanilla"
                result["package_manager"] = "npm"
        elif line.startswith("Response:"):
            result["response"] = line[9:].strip()

    return result


async def begin_react_loop(
    ctx: Context, user_input: str, max_steps: int = 3
) -> dict[str, str]:
    """Execute the reason-action (ReAct) loop to process user input and perform actions.

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
        ctx.logger.info("Querying LLM")
        response = await call_llm(
            PROMPT.format(actions=action_descriptions, input=user_input)
        )

        ctx.logger.info("Parsing LLM response")
        decision = parse_llm_response(response["choices"][0]["message"]["content"])

        ctx.logger.info(f"Thought: {decision.get('thought')}")

        # Execute action if chosen
        action_name = decision.get("action")
        if action_name and action_name in ACTIONS:
            action = ACTIONS[action_name]
            try:
                if action_name == "scaffold_django":
                    result = action.function(
                        ctx=ctx, project_name=decision.get("project_name")
                    )
                elif action_name == "scaffold_vite":
                    config = ViteConfig(
                        template=decision.get("template"),
                        project_name=decision.get("project_name"),
                        package_manager=decision.get("package_manager"),
                    )
                    result = action.function(ctx=ctx, config=config)

                if result:
                    break
            except Exception as e:
                ctx.logger.error(f"Action failed: {str(e)}")

        step += 1

    return {
        "thought": decision.get("thought"),
        "action": action_name,
        "action_args": decision.get("action_args"),
        "result": result,
        "response": decision.get("response"),
    }
