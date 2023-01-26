from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

"""
message.from_user.id


id: 446541718
is_bot: False
first_name: Oleg
username: Rocky_0013
language_code: ru
"""


async def bot_echo(message: types.Message):
    text = [
        "<em>Эхо без состояния.",
        "<b>Сообщение:</b></em>",
        message.text
    ]

    await message.answer('\n'.join(text), parse_mode="HTML")


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Эхо в состоянии {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))

async def on_startгp(_):
    print('Бот почав працювати!')


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
