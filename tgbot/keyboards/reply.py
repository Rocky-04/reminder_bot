from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from tgbot.models.models import PeriodicityManager

from sqlalchemy.orm import sessionmaker

def get_keybpards_create_notifications() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add((KeyboardButton('cancel')), KeyboardButton('back'))


def get_keybpards_skip_description() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add((KeyboardButton('skip_descriptions'))).add((KeyboardButton('cancel')), KeyboardButton('back'))


async def get_periodicity_keyboard(session) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard = InlineKeyboardMarkup(row_width=1)
    manager = PeriodicityManager(session)
    periodicity = await manager.get_all()
    print(periodicity)
    elements = []
    for elem in periodicity:
        print(elem.name)
        # elements.append(InlineKeyboardButton(text=elem.name, callback_data="random_value"))
        elements.append(InlineKeyboardButton(text=elem.name, callback_data=str(elem.id)))

    keyboard.add(*elements)

    return keyboard