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
                       kboard_admin.AdminCallbackFactory.filter(F.action == "spam"))
async def spam_start_hundler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory): 
    await callback.message.edit_text("""Выберите тип рассылки.""", reply_markup= kboard_admin.spam_markup
                                     , parse_mode=ParseMode.HTML)


@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "spam_users"))
async def write_spam_users_hundler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(StatesAdmin.print_spam_users)
    await callback.message.delete()
    markup = get_reply_markup("cancel", "ru")
    await callback.message.answer("""Введите текст рассылки для пользователей.""", reply_markup= markup,  parse_mode=ParseMode.HTML)




@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "spam_admin"))
async def write_spam_admins_hundler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(StatesAdmin.print_spam_admin)
    await callback.message.delete()
    markup = get_reply_markup("cancel", "ru")
    await callback.message.answer("""Введите текст рассылки для администраторов.""", reply_markup= markup, 
    parse_mode=ParseMode.HTML)


@router.message(StatesAdmin.print_spam_users, F.text.lower() == "отмена")
@router.message(StatesAdmin.print_spam_admin, F.text.lower() == "отмена")
async def cancel_spam_hundler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("""Отправка рассылки остановлена.""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    await message.answer("""Выберите тип рассылки.""", reply_markup= kboard_admin.spam_markup, 
                         parse_mode=ParseMode.HTML)



@router.message(StatesAdmin.print_spam_admin)
async def send_spam_admin_hundler(message: types.message, state: FSMContext):
    my_id = message.from_user.id
    id_adms = db.get_all_admins_id()
    for id in id_adms:
        if(id != my_id):
            await bot.send_message(id, message.text)
    await state.clear()
    await message.answer("""Рассылка успешно отправлена.""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)



    await message.answer("""Выберите тип рассылки.""", reply_markup= kboard_admin.spam_markup, parse_mode=ParseMode.HTML)


#Добавить возможность выбирать пользователей при рассылке, но как??????
@router.message(StatesAdmin.print_spam_users)
async def send_spam_users_hundler(message: types.message, state: FSMContext):
    id_usrs = db.get_all_users_id()
    for id in id_usrs:
        await bot.send_message(id, message.text)
    await state.clear()
    await message.answer("""Рассылка успешно отправлена.""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

    await message.answer("""Выберите тип рассылки.""", reply_markup= kboard_admin.spam_markup, parse_mode=ParseMode.HTML)