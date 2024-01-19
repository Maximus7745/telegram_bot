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
from text import db


from kboard import get_reply_markup



@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "statistics"))
async def spam_start_hundler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory): 
    pass