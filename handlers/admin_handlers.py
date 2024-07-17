from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from db.mysql_db import load_db

from filters.filters import IsUserAdmin
from lexicon.lexicon import LEXICON
from service.service import prepare_messages, count_stat
from keyboards.pagination import create_pagination_keyboard

router = Router()
page_size = 700


@router.message(Command(commands='report'), IsUserAdmin())
async def get_users_votes(message: Message, db_conn):
    db = load_db(db_conn)
    vote_info = db.get_vote_info()

    await message.answer(text=LEXICON.get('vote_info'))

    db.set_page(1, message.from_user.id)
    votes = prepare_messages(data=vote_info, page_size=page_size)
    text = votes.get(int(db.get_page(message.from_user.id)[0][0]))

    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{db.get_page(message.from_user.id)[0][0]}/{len(votes.keys())}',
            'forward'
        )
    )

    happy, unhappy = count_stat(vote_info)

    await message.answer(text=LEXICON.get('vote_stat').format(happy, unhappy))


@router.callback_query(F.data == 'forward', IsUserAdmin())
async def go_forward(callback: CallbackQuery, db_conn):
    db = load_db(db_conn)
    vote_info = db.get_vote_info()

    votes = prepare_messages(data=vote_info, page_size=page_size)

    curr_page = int(db.get_page(callback.from_user.id)[0][0])

    if curr_page < len(votes.keys()):
        next_page = curr_page + 1
        db.set_page(next_page, callback.from_user.id)
        text = votes.get(next_page)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{next_page}/{len(votes.keys())}',
                'forward'
            )
        )
    else:
        await callback.answer(LEXICON.get('end_log'))
    await callback.answer()


@router.callback_query(F.data == 'backward', IsUserAdmin())
async def go_forward(callback: CallbackQuery, db_conn):
    db = load_db(db_conn)
    vote_info = db.get_vote_info()

    votes = prepare_messages(data=vote_info, page_size=page_size)

    curr_page = int(db.get_page(callback.from_user.id)[0][0])

    if curr_page > 1:
        prev_page = curr_page - 1
        db.set_page(prev_page, callback.from_user.id)
        text = votes.get(prev_page)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{prev_page}/{len(votes.keys())}',
                'forward'
            )
        )
    else:
        await callback.answer(LEXICON.get('start_log'))
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit(), IsUserAdmin())
async def process_page_press(callback: CallbackQuery):
    await callback.answer(LEXICON.get('not_ready'))
