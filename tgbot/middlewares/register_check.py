from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from datetime import datetime
from tgbot.models.models import UserManager, Periodicity, PeriodicityManager, NotificationManager


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
        periodicity = await periodicity_manager.create(name='One time an hour', interval=24*60)
        print(periodicity)

        notification_manager = NotificationManager(session=session)
        notification = await notification_manager.create(name='Go work', date='2023-02-10 22:00',
                                                         periodicity=periodicity, user=user)
        print(notification)
        return
