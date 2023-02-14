from aiogram import types, Dispatcher

from tgbot.config import AVAILABLE_COMMANDS


async def unknown_command_handler(message: types.Message):
    """
    This function handles an unknown command received in a Telegram chat using the Telegram Bot API.

    :param message: A message object representing the unknown command.
    :type message: telegram.types.Message
    :return: None
    """

    response = f"Unknown command '{message.text}'. Please choose one of the following commands:\n\n"
    response += "\n".join(AVAILABLE_COMMANDS)

    await message.answer(response)


def register_unknown(dp: Dispatcher):
    dp.register_message_handler(unknown_command_handler, content_types=types.ContentTypes.ANY)