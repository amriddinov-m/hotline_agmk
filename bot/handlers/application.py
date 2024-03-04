import mimetypes
from mimetypes import MimeTypes

import aiohttp
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from bot.MESSAGES import MESSAGES
from bot.handlers.start import main_menu
from bot.keyboards.main import inline_btns, skip_btn
from bot.loader import dp, bot, form_router
from bot.models import Category, EEUser, Application
from bot.state.user import ApplicationState


@form_router.message(F.text.in_([MESSAGES['btn_application_create_uz'], MESSAGES['btn_application_create_ru'],
                                 MESSAGES['btn_application_create_us'], MESSAGES['btn_application_create_in'],
                                 MESSAGES['btn_application_create_vn'], MESSAGES['btn_application_create_tr']]))
async def choose_application_category_step(message: types.Message, state: FSMContext):
    categories = Category.objects.all()
    user = EEUser.objects.get(tg_id=message.from_user.id)
    markup = inline_btns(categories, user.language, 'category_')
    await message.answer(MESSAGES[f'input_category_{user.language}'], reply_markup=markup)
    await state.update_data(language=user.language)
    await state.set_state(ApplicationState.category)


@form_router.callback_query(ApplicationState.category, F.data.startswith("category_"))
async def input_comment_step(callback_query: types.CallbackQuery, state: FSMContext):
    _, category_id = callback_query.data.split('_')
    await state.update_data(category_id=category_id)
    data = await state.get_data()
    await callback_query.message.answer(MESSAGES[f'input_comment_{data["language"]}'])
    await state.set_state(ApplicationState.comment)


@form_router.message(ApplicationState.comment, F.text)
async def input_document_step(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)
    data = await state.get_data()
    keyboard = skip_btn(data['language'])
    await message.answer(MESSAGES[f'input_document_{data["language"]}'], reply_markup=keyboard)
    await state.set_state(ApplicationState.document)


async def create_application_step(user, state):
    data = await state.get_data()
    application = Application.objects.create(creator=user, category_id=data['category_id'], comment=data['comment'])
    return application


@form_router.message(ApplicationState.document, F.text)
async def document_skip_step(message: types.Message, state: FSMContext):
    user = EEUser.objects.get(tg_id=message.from_user.id)
    if message.text in MESSAGES[f'skip_{user.language}']:
        await create_application_step(user, state)
        await message.answer(MESSAGES[f'success_created_application_{user.language}'])

    await main_menu(message)
    await state.clear()


@form_router.message(ApplicationState.document)
async def create_application_photo_step(message: types.Message, state: FSMContext):
    user = EEUser.objects.get(tg_id=message.from_user.id)
    application = await create_application_step(user, state)
    if message.photo or message.document or message.voice:
        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.voice:
            file_id = message.voice.file_id
        else:
            file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.telegram.org/file/bot{bot.token}/{file_path}') as response:
                if response.status == 200:
                    file_content = await response.read()
                    if message.voice:
                        file_name = f'{file_id}.ogg'
                    elif message.photo:
                        file_name = f'{file_id}.jpg'
                    else:
                        file_name = message.document.file_name
                    application.document.save(file_name, ContentFile(file_content))
                    await message.answer(MESSAGES[f'success_created_application_{user.language}'])
                    await main_menu(message)
                    await state.clear()
                    return True
                else:
                    return False


current_page = 1
items_per_page = 5


async def show_current_page(chat_id, data, creator, update=False, message_id=0):
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_data = data[start_index:end_index]
    builder = InlineKeyboardBuilder()
    total_pages = (len(data) + items_per_page - 1) // items_per_page
    builder.row(
        types.InlineKeyboardButton(text="⬅️", callback_data="pagination_prev"),
        types.InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="current_page"),
        types.InlineKeyboardButton(text="➡️", callback_data="pagination_next"),
    )
    text = MESSAGES[f'result_pagination_{creator.language}'].format(start_index, end_index, len(data))
    counter = start_index + 1
    for application in current_data:
        text += (MESSAGES[f'application_detail_{creator.language}']
                 .format(f'{counter}.', application.pk,
                         application.category.get_name_by_lang(creator.language),
                         application.comment,
                         application.created_at.strftime("%d-%m-%Y %H:%M"),
                         MESSAGES[f'status_{application.status}_{creator.language}']))
        counter += 1
    if update:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=builder.as_markup())
    else:
        await bot.send_message(chat_id, text,
                               reply_markup=builder.as_markup())


@form_router.message(F.text.in_([MESSAGES['btn_application_list_uz'], MESSAGES['btn_application_list_ru'],
                                 MESSAGES['btn_application_list_us'], MESSAGES['btn_application_list_in'],
                                 MESSAGES['btn_application_list_vn'], MESSAGES['btn_application_list_tr']]))
async def my_applications(message: types.Message, state: FSMContext):
    creator = EEUser.objects.get(tg_id=message.from_user.id)
    applications = Application.objects.filter(creator=creator)
    global current_page
    current_page = 1
    await show_current_page(message.chat.id, applications, creator)


@dp.callback_query(F.data.startswith('pagination_'))
async def handle_pagination_buttons(callback_query: types.CallbackQuery):
    global current_page
    creator = EEUser.objects.get(tg_id=callback_query.from_user.id)
    data = Application.objects.filter(creator=creator)
    if callback_query.data == "pagination_prev" and current_page > 1:
        current_page -= 1
    elif callback_query.data == "pagination_next" and current_page < len(data) / items_per_page:
        current_page += 1
    await show_current_page(callback_query.message.chat.id, data, creator, update=True,
                            message_id=callback_query.message.message_id)
