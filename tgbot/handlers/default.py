from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.reply import get_main_keyboards


async def get_start(message: Message) -> None:
    """
    Sends a welcome message to the user and provides them with the main keyboard.
    """
    user = message['from']
    await message.reply(f"Hello, {user.first_name}!", reply_markup=get_main_keyboards())


async def get_help(message: Message) -> None:
    """
    Provides the user with an introduction to the bot and invites them to contact the creator
    with suggestions for improvements.
    """
    text = ("Welcome to our Telegram bot! We help you remember important events and tasks with "
            "custom reminders. Use our simple interface to set up and manage reminders, and get "
            "notified when it's time to take action. If you have any questions, type 'help' "
            "to access our support resources. \n\n We're always looking for ways to improve our "
            "bot and offer more helpful features. If you have any suggestions for new repeat "
            "intervals or ideas for improving our bot, please don't hesitate to reach out to "
            "the creator at {@Rocky_0013}. Your feedback is important to us and will help us "
            "make our bot even better for you.")
    await message.reply(text, reply_markup=get_main_keyboards())


def register_default(dp: Dispatcher) -> None:
    dp.register_message_handler(get_start,
                                lambda message: message.text in ("start", "/start"),
                                state="*")
    dp.register_message_handler(get_help,
                                lambda message: message.text in ("help", "/help", 'Get Help'),
                                state="*")
