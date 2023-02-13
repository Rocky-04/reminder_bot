from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models.models import UserManager, PeriodicityManager, NotificationManager


class RegisterCheck(BaseMiddleware):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_process_update(self, update: types.Update, data: dict):
        # print('****************************')
        # print(update)
        # print(update['message'])
        # print(update['callback_query'])
        # print(update.message)
        # print(update.callback_query)
        # print(user)
        # print(user.id)
        # print(user.first_name)
        # print('****************************')
        # user =  update.message['from']
        # user_id = update.message['from']['id']
        # user_name = update.message['from']['first_name']
        # print(user_id, user_name)
        # print('-------------------')

        user = update.message['from'] if update.message else update.callback_query['from']
        session = self.bot['session_maker']
        user_manager = UserManager(session=session)
        await user_manager.get_or_create_user(id=user.id, name=user.first_name)
        return

