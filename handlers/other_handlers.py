from aiogram import Router, F, Bot
from aiogram.types import Message, File
from lexicon.lexicon import LEXICON
# from external_services.bitrix import upload_file, open_file_from_disk
import typing
router = Router()


# @router.message(F.photo)
# async def process_photo(message: Message, bot: Bot, url_hook):
#     # Получаем список фотографий в сообщении
#     p_file = await bot.get_file(message.photo[-1].file_id)
#     print(p_file.file_path)
#     await message.answer('Photo received')
#     await bot.download(p_file.file_id, p_file.file_path)
#     await message.answer('Photo saved')
#     uploaded_file = upload_file(url_hook, str(217925), p_file.file_path)
#     await message.answer(f'File load with code: {uploaded_file.status_code}')
#     print(uploaded_file.json())


@router.message()
async def undefined_msg(message: Message):
    await message.answer(text=LEXICON.get('undefined'))



