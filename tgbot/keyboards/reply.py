from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from tgbot.models.models import PeriodicityManager, NotificationManager

from sqlalchemy.orm import sessionmaker

buttons = [
    'View My Reminders',
    'New Reminder',
    'Delete Reminder',
    'Get Help',
]


def get_main_keyboards() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    elements = []
    for elem in buttons:
        elements.append(KeyboardButton(text=elem))
    return keyboard.add(*elements)


def get_create_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add((KeyboardButton('cancel')), KeyboardButton('back'))


def get_skip_description_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add((KeyboardButton('skip_descriptions'))).add((KeyboardButton('cancel')), KeyboardButton('back'))


async def get_periodicity_keyboards(session) -> ReplyKeyboardMarkup:
    # keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard = InlineKeyboardMarkup(row_width=1)
    manager = PeriodicityManager(session)
    periodicity = await manager.get_all()
    print(periodicity)
    elements = []
    for elem in periodicity:
        print(elem.name)
        elements.append(InlineKeyboardButton(text=elem.name, callback_data=str(elem.id)))

    keyboard.add(*elements)

    return keyboard


async def get_del_keyboards(session, user) -> ReplyKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    manager = NotificationManager(session)
    notifications = await manager.get_users_all(user.id)
    elements = []
    for elem in notifications:
        print(elem.id)
        elements.append(InlineKeyboardButton(text=elem.name, callback_data=str(elem.id)))

    if elements:
        keyboard.add(*elements)
        keyboard.add(InlineKeyboardButton(text='Main menu',
                                          callback_data='main_menu'))
    else:
        keyboard.add(InlineKeyboardButton(text='No active reminders | To the main menu',
                                          callback_data='main_menu'))

    return keyboard