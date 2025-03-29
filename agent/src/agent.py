from cosmpy.aerial.client import LedgerClient, NetworkConfig
from uagents import Agent, Context

from src.config import get_config
from src.llm import call_llm
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
async def handle_startup(ctx: Context):
    ctx.logger.info(
        f"Hello, I'm agent {agent.name} and my address is {agent.address}. My wallet address is {agent.wallet.address()}"
    )
    ctx.logger.info(f"ASI network address: {agent.wallet.address()}")
    ledger_client = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    address = agent.wallet.address()
    balances = ledger_client.query_bank_all_balances(address)
    ctx.logger.info(f"Balance of addr: {balances}")


@agent.on_rest_post("/chat", Request, Response)
async def handle_post(ctx: Context, req: Request) -> Response:
    ctx.logger.info(f"Query: {req.query}")
    res = call_llm(req.query)
    ctx.logger.info(f"{ctx.session_history()} histories")
    return Response(
        status="success",
        message=res["choices"][0]["message"]["content"],
    )


if __name__ == "__main__":
    agent.run()
