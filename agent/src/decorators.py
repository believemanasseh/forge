from functools import wraps

from ratelimit import limits
from ratelimit.exception import RateLimitException
from uagents import Context

from src.config import get_config
from src.schemas import Request, Response

config = get_config()


def ratelimit(func):
    @limits(calls=config.RATE_LIMIT_CALLS, period=config.RATE_LIMIT_PERIOD)
    @wraps(func)
    async def wrapper(ctx: Context, req: Request) -> Response:
        try:
            return await func(ctx, req)
        except RateLimitException:
            ctx.logger.warning(
                f"Rate limit exceeded: {config.RATE_LIMIT_CALLS} calls per {config.RATE_LIMIT_PERIOD} seconds"
            )
            return Response(
                status="error",
                message=f"Rate limit exceeded. Please try again in {config.RATE_LIMIT_PERIOD} seconds.",
            )

    return wrapper
