from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from tgbot.filters.notifications import first_date_filter, name_filter, description_filter
from tgbot.keyboards.inline import get_periodicity_keyboards
from tgbot.keyboards.reply import get_create_keyboards, \
    get_skip_description_keyboards, get_main_keyboards
from tgbot.models.models import NotificationManager


class CustomState(State):
    def __init__(self, description: str = "", **kwargs):
        super().__init__(**kwargs)
        self.description = description


class CreateNotification(StatesGroup):
    name = State("Enter the name of the notification")
    description = State("Enter the description of the notification")
    first_date = State("Enter the first date and time of the notification")
    periodicity = State("Select the periodicity of the notification")


async def create_notifications(message: types.Message) -> None:
    """
    Handler to start the creation of a new notification. Sets the name state and sends a
    message to request the name.
    """
    await CreateNotification.name.set()
    await message.answer("Enter the name of the notification",
                         reply_markup=get_create_keyboards())


async def add_name(message: types.Message, state: FSMContext) -> None:
    """
    Handler to set the name of the notification. Validates the name and sets the description state.
    """
    async with state.proxy() as data:
        if not await name_filter(message.text):
            await message.reply("Invalid name format. Must be text no more than 250 characters.")
            return
        data['name'] = message.text

    await CreateNotification.next()
    await message.reply("Enter the description of the notification",
                        reply_markup=get_skip_description_keyboards())


async def add_description(message: types.Message, state: FSMContext) -> None:
    """
    Handler to set the description of the notification. Validates the description and sets
    the first_date state.
    """
    async with state.proxy() as data:
        if not await description_filter(message.text):
            await message.reply("Invalid description format. Must be text no more than 1000 "
                                "characters.")
            return
        data['description'] = message.text

    await CreateNotification.next()
    await message.reply(("Enter the first date and time of the notification in the format:\n\n "
                         " <b>2023-02-20 10:00</b>"),
                        reply_markup=get_create_keyboards())


async def add_first_date(message: types.Message, state: FSMContext, session: sessionmaker) -> None:
    """
    Handler to set the first date of the notification. Validates the first date and sets
    the periodicity state.
    """
    async with state.proxy() as data:
        if not await first_date_filter(message.text):
            await message.reply(
                "Invalid date and time format. Enter the data in the format:\n\n "
                "<b>2023-02-20 10:00</b>. \n This date must be in the future.")
            return

        data['first_date'] = message.text

    await CreateNotification.next()
    keyboard = await get_periodicity_keyboards(session)
    await message.reply("Select the periodicity of the notification",
                        reply_markup=keyboard)


async def periodicity_callback(callback: types.CallbackQuery, state: FSMContext,
                               session: sessionmaker, bot: Bot) -> None:
    """
    Creates a notification with the user-selected periodicity and stores it in the database.
    :param callback: The callback query generated by the user's action.
    :param state: The current state of the finite state machine.
    :param session: The session factory used to access the database.
    :param bot: The bot used to communicate with the user.
    :return: None
    """
    async with state.proxy() as data:
        user = callback.from_user

        manager = NotificationManager(session)
        await manager.create(name=data['name'],
                             description=data['description'],
                             date=data['first_date'],
                             periodicity_id=callback.data,
                             user=user.id)

    await callback.message.delete_reply_markup()
    await bot.send_message(chat_id=user.id, text='Notification created successfully!',
                           reply_markup=get_main_keyboards())
    await state.finish()


async def cancel_create(message: types.Message, state: FSMContext) -> None:
    """
    Cancels the creation of a notification and returns to the main menu.
    """
    await state.finish()
    await message.reply("Notification creation cancelled", reply_markup=get_main_keyboards())


async def back_create(message: types.Message, state: FSMContext) -> None:
    """
    Goes back to the previous step in the notification creation process.
    """
    previous_state = await CreateNotification.previous()
    if previous_state is None:
        await state.finish()
        await message.reply("Notification creation cancelled", reply_markup=get_main_keyboards())
        return
    await message.reply(previous_state)


async def skip_description(message: types.Message, state: FSMContext) -> None:
    """
    Skips the description step in the notification creation process.
    """
    async with state.proxy() as data:
        data['description'] = ''

    await CreateNotification.next()
    await message.reply(
        ("Description skipped.\n Enter the data in the format:\n\n "
         "<b>2023-02-20 10:00</b>. \n This date must be in the future."))


def register_create(dp: Dispatcher, bot: Bot) -> None:
    session = bot['db']
    dp.register_message_handler(cancel_create,
                                lambda message: message.text in ("Cancel", "/Cancel"),
                                state=CreateNotification)

    dp.register_message_handler(back_create,
                                lambda message: message.text in ("Back", "/Back"),
                                state=CreateNotification)

    dp.register_message_handler(skip_description,
                                lambda message: message.text in (
                                    "skip description", "Skip_Descriptions", "Skip Descriptions",),
                                state=CreateNotification.description)

    dp.register_message_handler(create_notifications,
                                lambda message: message.text in ("create", "/create",
                                                                 "New Reminder"))

    dp.register_message_handler(add_name, state=CreateNotification.name)
    dp.register_message_handler(add_description, state=CreateNotification.description)
    dp.register_message_handler(
        lambda message, state, session=session: add_first_date(message, state, session),
        state=CreateNotification.first_date)

    dp.register_callback_query_handler(
        lambda callback, state, session=session, bot=bot: periodicity_callback(
            callback, state, session, bot),
        state=CreateNotification.periodicity)
