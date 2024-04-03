from functools import partial
from typing import Any, List, Optional

import uprock_sdk.telegram_bots
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from redis.asyncio.client import Redis


class TelegramDispatcher(Dispatcher):
    def __init__(self, token: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.bot = Bot(token=token, parse_mode="HTML")

    def run(self, **kwargs: Any) -> None:
        super().run_polling(self.bot, **kwargs)

    async def start(self, **kwargs: Any) -> None:
        await super().start_polling(self.bot, **kwargs)


async def commands_on_startup(bot: Bot, commands: List[BotCommand]) -> None:
    await bot.set_my_commands(commands)


async def create_app(id_: int, router: Router, commands: Optional[List[BotCommand]] = None) -> TelegramDispatcher:
    telegram_bot = await uprock_sdk.telegram_bots.get(id_)

    storage = RedisStorage(Redis.from_url(str(telegram_bot.redis_uri)))

    dispatcher = TelegramDispatcher(token=telegram_bot.token, storage=storage)
    dispatcher.include_router(router)

    # Register startup hook to initialize webhook
    if commands:
        dispatcher.startup.register(partial(commands_on_startup, commands=commands))

    return dispatcher
