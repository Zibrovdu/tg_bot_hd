import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import Config, load_config
from handlers import other_handlers, user_handlers, admin_handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    file_handler = TimedRotatingFileHandler(filename='bot.log', encoding='utf-8', when='midnight', backupCount=5)
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=[file_handler, console_out],
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config('.env')

    my_storage = MemoryStorage()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=my_storage)
    dp.workflow_data.update(
        db_conn=config.db,
        bitrix_conn=config.bitrix_db,
        url_hook=config.bitrix.url,
        admin_list=config.tg_bot.admin_list,
        resp_id=config.bitrix.resp_id,
        group_id=config.bitrix.group_id
    )

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
