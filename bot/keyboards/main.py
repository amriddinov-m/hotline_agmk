# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
#
# from bot.models import CategoryProduct, LocationPoint, Product
#
# TG_BUTTON_MAX_LENGTH = 28
#
#
# async def generate_keyboard(btns, **kwargs):
#     reply_kb = ReplyKeyboardMarkup(**kwargs)
#     for desc in btns:
#         if desc:
#             reply_kb.insert(desc[:TG_BUTTON_MAX_LENGTH])
#     return reply_kb
#
#
# async def generate_keyboard_inline(*args, **kwargs):
#     kb = InlineKeyboardMarkup(**kwargs)
#     if isinstance(*args, list):
#         for arg in args:
#             for btn in arg:
#                 kb.insert(btn)
#     else:
#         kb.insert(*args)
#     return kb
#
#
# async def show_categories():
#     categories = CategoryProduct.objects.values_list('id', 'title')
#     btns = []
#     for obj_id, title in categories:
#         btn = InlineKeyboardButton(title, callback_data=f'category_{obj_id}')
#         btns.append(btn)
#     categories_kb = await generate_keyboard_inline(btns, row_width=1)
#     return categories_kb
#
#
# async def show_products(category_id):
#     products = Product.objects.filter(category_id=category_id).values_list('id', 'title')
#     btns = []
#     for obj_id, title in products:
#         btn = InlineKeyboardButton(title, callback_data=f'product_{obj_id}')
#         btns.append(btn)
#     products_kb = await generate_keyboard_inline(btns, row_width=2)
#     return products_kb
#
#
# async def show_location_points():
#     locations = LocationPoint.objects.values_list('id', 'title')
#     btns = []
#     for obj_id, title in locations:
#         btn = InlineKeyboardButton(f'{title}🟢', callback_data=f'location_{obj_id}')
#         btns.append(btn)
#     locations_kb = await generate_keyboard_inline(btns, row_width=2)
#     return locations_kb
#
#
# async def show_question_btn(order):
#     question_btn = [InlineKeyboardButton('✅ Принять',
#                                          callback_data=f'accept_order|{order.id}'),
#                     InlineKeyboardButton('❌ Отменить', callback_data=f'cancel_order|{order.id}')]
#     question_kb = await generate_keyboard_inline(question_btn)
#     return question_kb
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.MESSAGES import MESSAGES


def languages_btns(callback):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="O'zbek 🇺🇿",
            callback_data=f'{callback}_uz'),
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Русский язык 🇷🇺',
            callback_data=f'{callback}_ru'),
    )
    builder.row(
        types.InlineKeyboardButton(
            text='English 🇺🇸',
            callback_data=f'{callback}_us'),
    )
    builder.row(
        types.InlineKeyboardButton(
            text='कहंदी 🇮🇳',
            callback_data=f'{callback}_in'),
    )
    builder.row(
        types.InlineKeyboardButton(
            text='TIếng Việt Nam 🇻🇳',
            callback_data=f'{callback}_vn'),
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Türk dili 🇹🇷',
            callback_data=f'{callback}_tr'),
    )

    return builder.as_markup()


def start_btns(lang):
    kb = [
        [
            KeyboardButton(text=MESSAGES[f'btn_application_create_{lang}']),
        ],
        [
            KeyboardButton(text=MESSAGES[f'btn_application_list_{lang}']),
            KeyboardButton(text=MESSAGES[f'btn_settings_{lang}']),

        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def skip_btn(lang):
    kb = [
        [
            KeyboardButton(text=MESSAGES[f'skip_{lang}']),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def phone_btns(language):
    kb = [
        [
            KeyboardButton(text=MESSAGES[f'request_contact_{language}'], request_contact=True),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def inline_btns(qs, lang, callback_data):
    builder = InlineKeyboardBuilder()
    for obj in qs:
        builder.row(
            types.InlineKeyboardButton(
                text=f'{obj.get_name_by_lang(lang)}',
                callback_data=f'{callback_data}{obj.pk}')
        )
    return builder.as_markup()
