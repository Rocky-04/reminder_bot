from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from tgbot.filters.notifications import first_date_filter, name_filter, description_filter
from tgbot.keyboards.reply import get_keybpards_create_notifications, \
    get_keybpards_skip_description, get_periodicity_keyboard
from tgbot.models.models import NotificationManager


class CreateNotification(StatesGroup):
    name = State()
    description = State()
    first_date = State()
    periodicity = State()


async def create_notifications(message: types.Message):
    await CreateNotification.name.set()
    await message.answer("Введіть назву нагадування",
                         reply_markup=get_keybpards_create_notifications())


async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not await name_filter(message.text):
            await message.reply("Невірний формат назви. Повинен бути текст не більше 250 символів")
            return
        data['name'] = message.text

    await CreateNotification.next()
    await message.reply("Введіть опис нагадування",
                        reply_markup=get_keybpards_skip_description())


async def add_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not await description_filter(message.text):
            await message.reply("Невірний формат опису. Повинен бути текст не більше 1000 символів")
            return
        data['description'] = message.text

    await CreateNotification.next()
    await message.reply("Введіть першу дату та час нагадування в форматі: '2023-10-10 12:00'",
                        reply_markup=get_keybpards_create_notifications())


async def add_first_date(message: types.Message, state: FSMContext,  session: sessionmaker):
    async with state.proxy() as data:
        if not await first_date_filter(message.text):
            await message.reply(
                "Невірний формат дати та часу. Введіть дані в форматі: '2023-10-10 12:00'. "
                "Ця дата повинна бути в майбутньому")
            return

        data['first_date'] = message.text

    print(session)

    await CreateNotification.next()
    keyboard = await get_periodicity_keyboard(session)
    await message.reply("Введіть періодичнісь нагадування",
                        reply_markup=keyboard)


async def add_periodicity(message: types.Message, state: FSMContext, ):
    async with state.proxy() as data:
        data['periodicity'] = message.text

    await message.reply("Дукую!")

    async with state.proxy() as data:
        print(data)

    await state.finish()

async def periodicity_callback(callback: types.CallbackQuery, state: FSMContext, session: sessionmaker):
    print(callback.data)
    async with state.proxy() as data:
        data['periodicity'] = callback.data
        data['user'] = callback.from_user.id

    async with state.proxy() as data:
        print('---------------')
        print(data)  # FSMContextProxy state = 'CreateNotification:periodicity', data = {'name': '1', 'description': '2', 'first_date': '2023-10-10 12:00', 'periodicity': '1c374c9d-9daf-4ac5-8a76-df48de7ff7a3', 'user': 5517586660}

        name = data['name']
        description = data['description']
        date = data['first_date']
        periodicity = data['periodicity']
        user = data['user']
        manager = NotificationManager(session)
        await manager.create(name, description, date, periodicity, user)




    await callback.answer(text='Нагадування успішно створено')
    await state.finish()


async def cencel_create(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Створення відмінено")


async def back_create(message: types.Message, state: FSMContext):
    await CreateNotification.previous()
    await message.reply("Введіть попередній крок")


async def skip_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = None

    await CreateNotification.next()
    await message.reply("Опис пропущено. Введіть першу дату та час нагадування в форматі: '2023-10-10 12:00'")


async def test(message: types.Message,  session: sessionmaker):

    print(session)

    await CreateNotification.next()
    keyboard = await get_periodicity_keyboard(session)
    await message.reply("Введіть періодичнісь нагадування",
                        reply_markup=keyboard)




def register_notifications(dp: Dispatcher, bot,):
    print(dp)
    print(dir(dp))
    print(bot)
    print(bot['session_maker'])
    session = bot['session_maker']
    dp.register_message_handler(skip_description, lambda message: message.text == "skip_descriptions",
                                state=CreateNotification.description)
    dp.register_message_handler(back_create, lambda message: message.text == "back", state=CreateNotification)
    dp.register_message_handler(cencel_create, lambda message: message.text == "cancel", state=CreateNotification)
    dp.register_message_handler(add_name, state=CreateNotification.name)
    dp.register_message_handler(add_description, state=CreateNotification.description)
    # dp.register_message_handler(add_first_date, state=CreateNotification.first_date)
    dp.register_message_handler(add_periodicity, state=CreateNotification.periodicity)
    dp.register_message_handler(create_notifications, commands=["create"])

    dp.register_message_handler(
        lambda message, state, session=session: add_first_date(message, state, session), state=CreateNotification.first_date)

    dp.register_message_handler(
        lambda message, session=session: test(message, session), commands=["test"])

    dp.register_callback_query_handler(lambda callback, state, session=session: periodicity_callback(callback, state, session), state=CreateNotification.periodicity)

