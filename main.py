import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers_matrix import router
import json

bot = Bot('7066267859:AAH-MwiMZYbs7FgeW-nbNohNlpd2tylH4P0')
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")