from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON, Links


def create_ask_phone():
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(text=LEXICON['ask_phone_btn'], request_contact=True)
    )
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def category_menu(btns):
    kb_builder = InlineKeyboardBuilder()

    for button in btns:
        kb_builder.row(InlineKeyboardButton(
            text=button[1],
            callback_data=str(button[0])
        ))

    return kb_builder.as_markup()


def other_menu(*btns):
    kb_builder = InlineKeyboardBuilder()

    for button in btns:
        kb_builder.row(InlineKeyboardButton(
            text=LEXICON.get(button),
            callback_data=str(button)
        ))

    return kb_builder.as_markup()


def link_buttons(*btns):
    builder = InlineKeyboardBuilder()

    for button in btns:
        builder.row(InlineKeyboardButton(
            text=LEXICON.get(button),
            url=Links.first_line
        ))
    return builder.as_markup()
