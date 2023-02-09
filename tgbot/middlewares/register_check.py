from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models.models import UserManager, Periodicity, PeriodicityManager


class RegisterCheck(BaseMiddleware):
    def __init__(self, bot, **kwargs):
        super().__init__()
        self.bot = bot
        self.kwargs = kwargs

    async def on_process_update(self, update: types.Update, data: dict):
        user = update.message.from_user
        session = self.bot['session_maker']

        user_manager = UserManager(session=session)
        user  = await user_manager.get_or_create_user(id=user.id, name=user.first_name)
        print(user)

        periodicity_manager = PeriodicityManager(session=session)
        periodicity = await periodicity_manager.create(name='TEST_TEST', interval=3600)
        print(periodicity)
        return
