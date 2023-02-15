from aiogram import types, Dispatcher, Bot
from sqlalchemy.orm import sessionmaker

from tgbot.keyboards.reply import get_main_keyboards
from tgbot.models.models import NotificationManager


async def get_notifications(message: types.Message, session: sessionmaker, bot: Bot) -> None:
    """
    This function retrieves all the reminders for the user and returns them in a formatted
    text message.
    """
    user = message['from']

    manager = NotificationManager(session)
    notifications = await manager.get_users_all(user.id)
    if not notifications:
        await message.reply('There are no active reminders')
        return
    text = ''
    for num, remind in enumerate(notifications, start=1):
        text += (f'<b>{num}) {remind.name}</b>\n<u>{remind.description}</u>\n'
                 f'Next remind: {remind.next_data}\nPeriodicity: {remind.periodicity}\n\n')
    if len(text) <= 4000:
        await message.reply(text)
    else:
        messages = []
        temp_text = ""
        for line in text.split("\n"):
            if len(temp_text) + len(line) + 1 > 4000:
                messages.append(temp_text)
                temp_text = line + "\n"
            else:
                temp_text += line + "\n"
        if temp_text:
            messages.append(temp_text)
        for msg in messages:
            await bot.send_message(chat_id=user.id, text=msg, reply_markup=get_main_keyboards())


def register_get(dp: Dispatcher, bot: Bot):
    session = bot['db']
    dp.register_message_handler(
        lambda message, session=session, bot=bot: get_notifications(message, session, bot),
        lambda message: message.text in ("get_notifications", "View My Reminders",
                                         '/get_notifications Help', 'get', '/get'))
