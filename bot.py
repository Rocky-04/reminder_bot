import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.create import register_create
from tgbot.handlers.default import register_default
from tgbot.handlers.delete import register_delete
from tgbot.handlers.get import register_get
from tgbot.handlers.unknown import register_unknown
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.register_check import RegisterCheck
from tgbot.models.models import Base
from tgbot.services.default_data import get_default_data
from tgbot.services.remind import remind

logger = logging.getLogger(__name__)
CREATOR = '@Rocky_0013'


def register_all_middlewares(dp, bot):
    dp.setup_middleware(EnvironmentMiddleware(bot=bot))
    dp.setup_middleware(RegisterCheck(bot=bot))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp, bot):
    register_admin(dp)
    register_default(dp)
    register_get(dp, bot)
    register_create(dp, bot)
    register_delete(dp, bot)
    register_unknown(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2(host=config.redis.host,
                            port=config.redis.port) if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    engine = create_async_engine(
        (f"postgresql+asyncpg://{config.db.user}:{config.db.password}@"
         f"{config.db.host}/{config.db.database}"),
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    bot["db"] = async_sessionmaker
    bot['storage'] = storage

    register_all_middlewares(dp, bot)
    register_all_filters(dp)
    register_all_handlers(dp, bot)

    await get_default_data(bot)

    asyncio.create_task(remind(bot=bot))

    try:
        await dp.start_polling(dp)

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
