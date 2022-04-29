import asyncio
from aiogram import Bot, Dispatcher, types
import os
import socket

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BROADCAST_RANGE = os.environ.get("BROADCAST_RANGE", "255.255.255.255")
MAC_ADDRESS = os.environ.get("MAC_ADDRESS", "00:00:00:00:00:00")
OWNER_ID = int(os.environ.get("USER_ID", ""))

def create_magic_packet(macaddress: str) -> bytes:
    if len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, "")
    elif len(macaddress) != 12:
        raise ValueError("Incorrect MAC address format")

    return bytes.fromhex("F" * 12 + macaddress * 16)

def send_magic_packet():
    packet = create_magic_packet(MAC_ADDRESS)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.connect((BROADCAST_RANGE, 9))
        sock.send(packet)

async def start_handler(event: types.Message):
    if event.from_user.id == OWNER_ID:
        await event.answer("im fine, totally!")

async def boot_handler(event: types.Message):
    if event.from_user.id != OWNER_ID:
        return

    try:
        send_magic_packet()
        await event.answer(f"Waking up the machine with MAC `{MAC_ADDRESS}`\!😎", parse_mode="MarkdownV2")
    except Exception as e:
        await event.answer(f"Something bad happend: `{str(e)}`", parse_mode="MarkdownV2")

    return

async def main():
    bot = Bot(token=BOT_TOKEN)

    try:
        me = await bot.get_me()
        print(f"🤖 Hello, I'm {me.first_name}.\nHave a nice Day!")
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start", "status"})
        disp.register_message_handler(boot_handler, commands={"boot"})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())