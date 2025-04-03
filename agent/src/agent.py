from cosmpy.aerial.client import LedgerClient, NetworkConfig
from uagents import Agent, Context

from src.config import get_config
from src.schemas import Request, Response

config = get_config()


agent = Agent(
    name=config.NAME,
    port=config.PORT,
    seed=config.SEED,
    endpoint=config.ENDPOINT,
    mailbox=config.MAILBOX,
    store_message_history=True,
)


@agent.on_event("startup")
async def handle_startup(ctx: Context) -> None:
    """
    Startup event handler that initialises the agent

    Args:
        ctx (Context): The agent context object

    Returns:
        None: This function doesn't return anything
    """
    ctx.logger.info(
        f"Hello, I'm agent {agent.name} and my address is {agent.address}. My wallet address is {agent.wallet.address()}"
    )
    ledger_client = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    address = agent.wallet.address()
    balances = ledger_client.query_bank_all_balances(address)
    ctx.logger.info(f"Wallet balance: {balances}")


@agent.on_rest_post("/chat", Request, Response)
async def handle_post(ctx: Context, req: Request) -> Response:
    """
    Handles POST requests to the /chat endpoint.

    Args:
        ctx (Context): The agent context object
        req (Request): The incoming request containing the query

    Returns:
        Response: Contains status, response message, and ReAct loop result
    """
    from src.react import begin_react_loop

    ctx.logger.info(f"Query: {req.query}")
    ctx.logger.info(f"{ctx.session_history()} histories")
    data = await begin_react_loop(ctx, req.query)
    return Response(
        status="success", message="Project scaffolded successfully", data=data
    )


if __name__ == "__main__":
    agent.run()
