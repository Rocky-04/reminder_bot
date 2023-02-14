from aiogram import types, Dispatcher, Bot
from sqlalchemy.orm import sessionmaker

from tgbot.keyboards.reply import get_del_keyboards, get_main_keyboards
from tgbot.models.models import NotificationManager
from tgbot.services.is_valid_uuid import is_valid_uuid


async def del_notifications(message: types.Message, session: sessionmaker) -> None:
    """
    Sends a message to the user with a keyboard to delete notifications.
    """
    user = message.from_user
    keyboard = await get_del_keyboards(session, user)
    await message.reply('Press the message you want to delete', reply_markup=keyboard)


async def del_callback(callback: types.CallbackQuery, session: sessionmaker) -> None:
    """
    Handles the user's request to delete a notification.
    :param callback: The callback query object.
    :param session: The database session.
    :return: None
    """
    id = callback.data
    user = callback.from_user
    manager = NotificationManager(session)
    result = await manager.delete(id, user_id=user.id)
    if result:
        await callback.answer('Done')
    else:
        await callback.answer('Error')
    keyboard = await get_del_keyboards(session, user)
    await callback.message.edit_reply_markup(reply_markup=keyboard)


async def del_callback_main_menu(callback: types.CallbackQuery, bot: Bot) -> None:
    user = callback.from_user
    await bot.send_message(chat_id=user.id, text='Виберіть що потрібно зробити',
                           reply_markup=get_main_keyboards())


def register_delete(dp: Dispatcher, bot: Bot) -> None:
    session = bot['session_maker']

    dp.register_message_handler(
        lambda message, session=session: del_notifications(message, session),
        lambda message: message.text in (
            "Delete Reminder", "/delete", "delete", "del_notifications"))

    dp.register_callback_query_handler(
        lambda callback, bot=bot: del_callback_main_menu(callback, bot),
        lambda callback: callback.data == "main_menu")

    dp.register_callback_query_handler(
        lambda callback, session=session: del_callback(callback, session),
        lambda callback: is_valid_uuid(callback.data))
