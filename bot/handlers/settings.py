from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.MESSAGES import MESSAGES
from bot.handlers.start import main_menu
from bot.keyboards.main import languages_btns
from bot.loader import form_router, bot, dp
from bot.models import EEUser
from bot.state.user import UserState


@form_router.message(F.text.in_([MESSAGES['btn_settings_uz'], MESSAGES['btn_settings_ru'],
                                 MESSAGES['btn_settings_us'], MESSAGES['btn_settings_in'],
                                 MESSAGES['btn_settings_vn'], MESSAGES['btn_settings_tr']]))
async def settings(message: types.Message, state: FSMContext):
    markup = languages_btns('change-language')
    await bot.send_message(message.from_user.id,
                           MESSAGES['choose_language'],
                           reply_markup=markup)
    await state.set_state(UserState.settings)


@form_router.callback_query(UserState.settings, F.data.startswith("change-language_"))
async def change_language_step(callback_query: types.CallbackQuery, state: FSMContext):
    _, language = callback_query.data.split('_')
    await callback_query.message.delete()
    user = EEUser.objects.get(tg_id=callback_query.from_user.id)
    user.language = language
    user.save()
    await bot.send_message(callback_query.from_user.id,
                           MESSAGES[f'successfully_changed_{language}'])
    await main_menu(callback_query.message)

