import asyncio
import logging
from datetime import datetime

from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.notifications import register_notifications
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.register_check import RegisterCheck
from tgbot.models.models import Base, UserManager, PeriodicityManager, NotificationManager
from tgbot.services.remind import remind

logger = logging.getLogger(__name__)


async def create_test_data(bot):
    print('-----------------create_test_data---------------------------')

    session = bot['session_maker']

    user_manager = UserManager(session=session)
    user = await user_manager.get_or_create_user(id=5517586660, name="OLEG_TEST")
    print(user)

    periodicity_manager = PeriodicityManager(session=session)

    await periodicity_manager.create(name='Do not repeat', interval=0)
    periodicity = await periodicity_manager.create(name='One time per minute', interval=1)
    await periodicity_manager.create(name='One time per half hour', interval=30)
    await periodicity_manager.create(name='One time per hour"', interval=60)
    await periodicity_manager.create(name='One time per 3 hour', interval=3 * 60)
    await periodicity_manager.create(name='One time per 1 day ', interval=24 * 60)
    await periodicity_manager.create(name='One time per 3 days', interval=24*60*3)
    await periodicity_manager.create(name='One time per 7 days', interval=24*60*7)
    await periodicity_manager.create(name='One time per 30 day', interval=24*60*30)
    await periodicity_manager.create(name='One time per 90 day', interval=24*60*90)
    await periodicity_manager.create(name='One time per 180 day', interval=24*60*180)
    await periodicity_manager.create(name='One time per 365 day', interval=24*60*365)

    notification_manager = NotificationManager(session=session)
    notification = await notification_manager.create(name='Go work', description='Some descriptions', date='2023-02-13 17:00',
                                                     periodicity=periodicity, user=user.id)
    print(notification)

    print('-------------------------FINISH-----------------------------')
    return






def register_all_middlewares(dp, bot):
    dp.setup_middleware(EnvironmentMiddleware(bot=bot))
    dp.setup_middleware(RegisterCheck(bot=bot))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp, bot):
    register_notifications(dp, bot)
    register_admin(dp)
    register_user(dp)
    register_echo(dp)



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    engine = create_async_engine(
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}",
        future=True
    )
    async with engine.begin() as conn:
        # print(dir(Base.metadata))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    bot["db"] = async_sessionmaker
    bot['session_maker'] = async_sessionmaker
    bot['storage'] = storage

    register_all_middlewares(dp, bot)
    register_all_filters(dp)
    register_all_handlers(dp, bot)



    await create_test_data(bot)

    asyncio.create_task(remind(bot=bot))

    # start
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
