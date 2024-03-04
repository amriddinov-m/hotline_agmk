import re

from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.MESSAGES import MESSAGES
from bot.keyboards.main import start_btns, phone_btns, languages_btns, inline_btns
from bot.loader import dp, bot, form_router
from bot.models import EEUser, Category
from bot.state.user import RegisterState


@dp.message(F.text.startswith('http'))
async def check_message(message: types.Message):
    await message.reply("Извините, отправка ссылок запрещена.")


async def main_menu(message):
    user = EEUser.objects.get(tg_id=message.chat.id)
    keyboard = start_btns(user.language)
    await message.answer(MESSAGES[f'user_main_text_{user.language}'], reply_markup=keyboard)


@dp.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    print(message.from_user.full_name)
    user = EEUser.objects.filter(tg_id=message.from_user.id)
    if user:
        await main_menu(message)
    else:
        markup = languages_btns('language')
        await state.set_state(RegisterState.language)
        await message.answer(MESSAGES['choose_language'], reply_markup=markup)


@form_router.callback_query(RegisterState.language, F.data.startswith("language_"))
async def language_change_step(callback_query: types.CallbackQuery, state: FSMContext):
    _, language = callback_query.data.split('_')
    await state.update_data(language=language)
    await callback_query.message.answer(MESSAGES[f'input_fullname_{language}'])
    await state.set_state(RegisterState.fullname)


@form_router.message(RegisterState.fullname)
async def user_register_fullname_step(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(fullname=fullname)
    data = await state.get_data()
    await message.answer(MESSAGES[f'input_position_{data["language"]}'])
    await state.set_state(RegisterState.position)


@form_router.message(RegisterState.position)
async def user_register_position_step(message: types.Message, state: FSMContext):
    position = message.text
    await state.update_data(position=position)
    data = await state.get_data()
    keyboard = phone_btns(data['language'])
    await message.answer(MESSAGES[f'input_phone_{data["language"]}'], reply_markup=keyboard)
    await state.set_state(RegisterState.phone)


@form_router.message(RegisterState.phone, F.contact)
async def user_register_phone_step(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    data = await state.get_data()
    EEUser.objects.get_or_create(tg_id=message.from_user.id,
                                 defaults={'fullname': data['fullname'], 'phone': data['phone'],
                                           'position': data['position'],
                                           'language': data['language']})
    await message.answer(MESSAGES[f'success_registered_{data["language"]}'])
    await main_menu(message)
    await state.clear()
