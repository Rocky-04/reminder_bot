from aiogram import Dispatcher
from aiogram.types import Message


async def admin_start(message: Message) -> None:
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher) -> None:
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
