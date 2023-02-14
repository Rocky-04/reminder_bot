from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton

from tgbot.models.models import PeriodicityManager, NotificationManager


async def get_periodicity_keyboards(session) -> InlineKeyboardMarkup:
    """Returns an inline keyboard with all available periodicities."""
    keyboard = InlineKeyboardMarkup(row_width=1)
    manager = PeriodicityManager(session)
    periodicity = await manager.get_all()
    elements = []
    for elem in periodicity:
        elements.append(InlineKeyboardButton(text=elem.name, callback_data=str(elem.id)))

    keyboard.add(*elements)
    return keyboard


async def get_del_keyboards(session, user) -> InlineKeyboardMarkup:
    """Returns an inline keyboard with all the reminders for a given user."""
    keyboard = InlineKeyboardMarkup(row_width=1)
    manager = NotificationManager(session)
    notifications = await manager.get_users_all(user.id)
    elements = []
    for elem in notifications:
        elements.append(InlineKeyboardButton(text=elem.name, callback_data=str(elem.id)))

    if elements:
        keyboard.add(*elements)
        keyboard.add(InlineKeyboardButton(text='Main menu',
                                          callback_data='main_menu'))
    else:
        keyboard.add(InlineKeyboardButton(text='No active reminders | To the main menu',
                                          callback_data='main_menu'))
    return keyboard
