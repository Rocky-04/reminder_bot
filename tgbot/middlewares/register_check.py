from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models.models import UserManager, PeriodicityManager, NotificationManager


class RegisterCheck(BaseMiddleware):
    """
    Middleware that checks if the user is registered in the system,
    if not, it creates a new user instance.
    """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_process_update(self, update: types.Update, data: dict) -> None:
        """
        Event handler that checks if the user is registered in the system.
        If not, it creates a new user instance.

        :param update: The incoming update.
        :param data: The data dictionary.
        :return: None
        """
        user = update.message['from'] if update.message else update.callback_query['from']
        session = self.bot['session_maker']
        user_manager = UserManager(session=session)
        await user_manager.get_or_create_user(id=user.id, name=user.first_name)
        return

