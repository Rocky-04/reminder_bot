import asyncio
import logging

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

logger = logging.getLogger(__name__)


async def create_test_data(bot):
    print('-----------------create_test_data---------------------------')

    session = bot['session_maker']

    user_manager = UserManager(session=session)
    user = await user_manager.get_or_create_user(id=1, name="OLEG_TEST")
    print(user)

    periodicity_manager = PeriodicityManager(session=session)
    periodicity = await periodicity_manager.create(name='One time an day', interval=24 * 60)
    print(periodicity)

    notification_manager = NotificationManager(session=session)
    notification = await notification_manager.create(name='Go work', description='', date='2023-02-10 22:00',
                                                     periodicity=periodicity.id, user=user.id)
    print(notification)

    periodicity = await periodicity_manager.create(name='One time an hour', interval=1 * 60)
    print(periodicity)

    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)
    periodicity = await periodicity_manager.create(name='One time an halfhour', interval=1 * 30)

    print(periodicity)

    periodicitys = await periodicity_manager.get_all()
    print(periodicitys)
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
    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
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

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
