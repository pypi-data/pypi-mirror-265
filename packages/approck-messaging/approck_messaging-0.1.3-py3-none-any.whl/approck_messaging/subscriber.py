from typing import Callable, Any

from faststream import context
from faststream.broker.types import P_HandlerParams, T_HandlerReturn
from faststream.broker.wrapper import HandlerCallWrapper
from faststream.redis import RedisBroker


class Subscriber:
    def __init__(self, broker: RedisBroker, **kwargs) -> None:
        self.broker = broker

        for key, value in kwargs.items():
            context.set_global(key, value)

    @classmethod
    def from_uri(cls, redis_uri: str, **kwargs) -> "Subscriber":
        return cls(broker=RedisBroker(redis_uri), **kwargs)

    def message(
        self, stream: str
    ) -> Callable[
        [Callable[P_HandlerParams, T_HandlerReturn]],
        HandlerCallWrapper[Any, P_HandlerParams, T_HandlerReturn],
    ]:
        return self.broker.subscriber(stream=stream)
