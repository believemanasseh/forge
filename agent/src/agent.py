import os

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from dotenv import load_dotenv
from uagents import Agent, Context, Model

load_dotenv()

NAME = os.getenv("NAME", "doki")
PORT = os.getenv("PORT", "8000")
ENDPOINT = os.getenv("ENDPOINT", "http://localhost:8000/submit")
MAILBOX = os.getenv("MAILBOX", False)

agent = Agent(name=NAME, port=PORT, endpoint=ENDPOINT, mailbox=MAILBOX)


class Message(Model):
    text: str


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


@agent.on_message(model=Message)
async def receive_sender_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.text}")


if __name__ == "__main__":
    agent.run()
