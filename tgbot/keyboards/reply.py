from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons = [
    'View My Reminders',
    'New Reminder',
    'Delete Reminder',
    'Get Help',
]


def get_main_keyboards() -> ReplyKeyboardMarkup:
    """Returns a reply keyboard with the given buttons."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    elements = []
    for elem in buttons:
        elements.append(KeyboardButton(text=elem))
    return keyboard.add(*elements)


def get_create_keyboards() -> ReplyKeyboardMarkup:
    """Returns a reply keyboard for creating new reminders."""
    return ReplyKeyboardMarkup(resize_keyboard=True).add((KeyboardButton('Cancel')),
                                                         KeyboardButton('Back'))


def get_skip_description_keyboards() -> ReplyKeyboardMarkup:
    """Returns a reply keyboard for skipping reminder descriptions."""
    return ReplyKeyboardMarkup(resize_keyboard=True).add((KeyboardButton('Skip Descriptions'))).add(
        (KeyboardButton('Cancel')), KeyboardButton('Back'))
