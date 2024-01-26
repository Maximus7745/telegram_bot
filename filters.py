from aiogram import types, Bot
from aiogram.filters import BaseFilter
from typing import Union, Dict, Any
from text import db

class IsAdminFilter(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery) -> Union[bool, Dict[str, Any]]:
        user_id = callback.message.chat.id
        return db.check_admin(user_id)




class IsPdfOrJpg(BaseFilter):
    async def __call__(self, message: types.message)-> Union[bool, Dict[str, Any]]:
        file_id = message.document.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        if(file_path.split(".")[len(file_path.split(".")) - 1] in ["jpg", "pdf"]) and file_info.file_size // 1024 < 15000:
            return True
        return False
class IsJpg(BaseFilter):
    async def __call__(self, message: types.message)-> Union[bool, Dict[str, Any]]:
        photo = message.photo[-1] 
        file_id = photo.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path

        return (file_path.split(".")[len(file_path.split(".")) - 1] in ["jpg"]) and file_info.file_size // 1024 < 15000


class IsJpeg(BaseFilter):
    async def __call__(self, message: types.message)-> Union[bool, Dict[str, Any]]:
        file_id = message.document.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        if(file_path.split(".")[len(file_path.split(".")) - 1] == "jpg")and file_info.file_size // 1024 < 15000:
            return True
        return False
