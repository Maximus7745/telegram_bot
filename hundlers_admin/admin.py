from handlers.start import router
from filters import IsAdminFilter 
from aiogram import types
from magic_filter import F
from aiogram.enums import ParseMode
from states import StatesReductBtn, StatesReductMsg, StateAddBtn, StatesAdmin, StatesReductForm, StatesCancelForm, StatesReductApplication, StatesAnswerQuestions
from aiogram.types import FSInputFile
from bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram.filters import Command, StateFilter
import kboard_admin
from text import get_action_msg, get_text, get_text_for_all_lang, db


@router.message(StateFilter(None), Command("yhtynhhrytnryh5e54gseae4fvfdsgw354egf4e"))
async def add_admin(message: types.Message):
    user_id = message.from_user.id
    db.add_admin_by_id(user_id)
    await message.answer("Поздравляем, вы администратор!!!")


@router.message(StateFilter(None), Command("ywe9483wfiewfj34efweefwq3qr3fef3qewf"))
async def del_admin(message: types.Message):
    user_id = message.from_user.id
    db.del_admin_by_id(user_id)
    await message.answer("Вы больше не администратор((((")


@router.message(StateFilter(None), Command("3rf34fg43o329r32E3jifweowkfoewfwfr3"))
async def start_admin(message: types.Message):
    user_id = message.from_user.id
    if(db.check_admin(user_id)):
        await message.answer("Добро пожаловать! Выберите интересующий вас раздел и приступайте к администрированию телеграм бота.",
                             reply_markup= kboard_admin.start_markup,
                             parse_mode=ParseMode.HTML)
        
@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "start"))
async def start_admin_callback(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    if(db.check_admin(user_id)):
        await callback.message.edit_text("Добро пожаловать! Выберите интересующий вас раздел и приступайте к администрированию телеграм бота.",
                             reply_markup= kboard_admin.start_markup,
                             parse_mode=ParseMode.HTML)