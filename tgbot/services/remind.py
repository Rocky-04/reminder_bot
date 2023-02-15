import asyncio
import logging
from datetime import datetime, timedelta
from typing import Union

from aiogram import Bot

from tgbot.models.models import NotificationManager, Notification

logger = logging.getLogger(__name__)


async def remind(bot: Bot) -> None:
    """
     The function to remind the user of their scheduled reminders.

    :param bot: The bot instance.
    :return: None
    """
    session = bot['session_maker']
    while True:
        notification_manager = NotificationManager(session=session)
        reminders = await notification_manager.get_all()
        for reminder in reminders:
            if reminder.next_data <= datetime.now():
                next_data = await update_next_data(manager=notification_manager, reminder=reminder)
                text = (f'<b>{reminder.name}</b>\n\n<u>{reminder.description}</u>\n'
                        f'Next remind: {next_data}"')
                if datetime.now() - reminder.next_data > timedelta(minutes=2):
                    text = f'Notification was missed {reminder.next_data} : \n' + text

                try:
                    await bot.send_message(chat_id=reminder.user, text=text)
                except Exception as error:
                    logger.error("Error sending reminder: %s", error)

        await asyncio.sleep(60)


async def update_next_data(manager: NotificationManager,
                           reminder: Notification) -> Union[str, datetime]:
    """
    Update the next_data field of a reminder and return the new value.
    If the reminder does not repeat, it is deleted and the function returns 'Repeated only once'.

    :param manager: The notification manager to use for database access.
    :param reminder: The reminder to update.
    :return: The new value of the next_data field, or 'Repeated only once' if the reminder does
        not repeat.
    """
    if reminder.periodicity.interval == 0:
        await manager.delete(id=reminder.id, user_id=reminder.user)
        return 'Repeated only once'

    # Calculate the new value for the next_data field.
    next_data = reminder.next_data + timedelta(minutes=reminder.periodicity.interval)
    if next_data < datetime.now():
        while next_data < datetime.now():
            next_data += timedelta(minutes=reminder.periodicity.interval)
    await manager.update_next_data(reminder.id, next_data)
    return next_data
