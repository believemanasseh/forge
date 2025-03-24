import os

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from dotenv import load_dotenv
from uagents import Agent, Context, Model

from src.llm import call_llm

load_dotenv()

NAME = os.getenv("NAME", "doki")
PORT = os.getenv("PORT", "8000")
ENDPOINT = os.getenv("ENDPOINT", "http://localhost:8000/submit")
MAILBOX = os.getenv("MAILBOX", False)
SEED = os.getenv("SEED", None)

agent = Agent(
    name=NAME,
    port=PORT,
    seed=SEED,
    endpoint=ENDPOINT,
    mailbox=MAILBOX,
    store_message_history=True,
)


class Request(Model):
    query: str


class Response(Model):
    id: str
    object: str
    created: int
    model: str
    choices: list
    usage: dict


@agent.on_event("startup")
async def introduce_receiver(ctx: Context):
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
        id=res["id"],
        object=res["object"],
        created=res["created"],
        model=res["model"],
        choices=res["choices"],
        usage=res["usage"],
    )


if __name__ == "__main__":
    agent.run()
