import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot

from tgbot.models.models import NotificationManager

logger = logging.getLogger(__name__)


async def remind(bot: Bot) -> None:
    """
     The function to remind the user of their scheduled reminders.

    :param bot: The bot instance.
    :return:
    """
    session = bot['session_maker']
    while True:
        notification_manager = NotificationManager(session=session)
        reminders = await notification_manager.get_all()
        for reminder in reminders:
            if reminder.next_data <= datetime.now():
                next_data = reminder.next_data + timedelta(minutes=reminder.periodicity.interval)
                if next_data < datetime.now():
                    while next_data < datetime.now():
                        next_data += timedelta(minutes=reminder.periodicity.interval)
                await notification_manager.update_next_data(reminder.id, next_data)

                text = (f'<b>{reminder.name}</b>\n\n<u>{reminder.description}</u>\n'
                        f'Next remind: {next_data}"')
                if datetime.now() - reminder.next_data > timedelta(minutes=2):
                    text = f'Notification was missed {reminder.next_data} : \n' + text

                try:
                    await bot.send_message(chat_id=reminder.user, text=text)
                except Exception as e:
                    logger.error("Error sending reminder: %s", e)

        await asyncio.sleep(10)
