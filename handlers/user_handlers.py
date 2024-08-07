import logging
from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, FSInputFile, CallbackQuery, ReplyKeyboardRemove

from db.mysql_db import load_db
from external_services.bitrix import (id_by_phone, set_bitrix_task, id_by_tg, search_user_by_phone, check_user_active,
                                      get_user_name)
from filters.filters import (IsChoseCat, IsPressedBackBtn, IsEditMessage, IsSetTask, IsCancelTask, IsUserHappy,
                             IsUserUnHappy, IsUserContact, IsChoosePerson)
from keyboards.kbs import create_ask_phone, category_menu, other_menu, link_buttons
from lexicon.lexicon import LEXICON, msg_menu, ynbtns, additions, service, srv_cats
from states.states import FSMFillForm

router = Router()
logger = logging.getLogger(__name__)


# Этот хендлер срабатывает на команду start вне машины состояний и предлагает пользователю поделиться номером телефона
@router.message(CommandStart(), StateFilter(default_state))
async def start(message: Message, db_conn, state: FSMContext, url_hook):
    logger.info('User send start command')
    db = load_db(db_conn)
    photo = FSInputFile('assets/it_block.jpg', 'it_block')

    await message.answer_photo(photo)

    user = db.get_user(user_id=str(message.from_user.id))
    if not user:
        db.create_user(
            user_id=str(message.from_user.id),
            tg_name=message.from_user.username,
            chat_id=message.chat.id
        )
        user = db.get_user(user_id=str(message.from_user.id))
    buid = id_by_tg(tg_name=message.from_user.username, mysql_conn=db_conn)[0]

    if user[1] or buid > 0:
        if user[1]:
            buid = user[1]
        b_user_name, b_user_last_name = get_user_name(mysql_conn=db_conn, buid=buid)[0]

        db.save_bitrix_data(
            user_id=message.from_user.id,
            b_uid=int(buid),
            b_user_name=b_user_name,
            b_user_last_name=b_user_last_name
        )
        # проверяем активность учетной записи пользователя
        if not check_user_active(buid, url_hook):
            await message.answer(LEXICON.get('not_active'))
            await state.clear()
        else:
            await message.answer(
                text=LEXICON.get('hello_user').format(b_user_name, b_user_last_name),
                reply_markup=ReplyKeyboardRemove()
            )
            cat_ids = [i for i in db.get_cats('tech_sup')]
            cat_ids = service(cat_ids)

            msg = await message.answer(text=LEXICON.get('choose_cat'),
                                       reply_markup=category_menu(cat_ids))
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(FSMFillForm.fill_cat)
    else:
        await message.answer(text=LEXICON.get('welcome'), reply_markup=create_ask_phone())
        await state.set_state(FSMFillForm.fill_phone)


# Хендлер сработает если пользователь отправит боту команду start пока бот ожидает номер телефона
@router.message(CommandStart(), StateFilter(FSMFillForm.fill_phone))
@router.message(StateFilter(FSMFillForm.fill_phone), ~IsUserContact())
async def start_in_fsm(message: Message):
    logger.info('User send start command when bot waiting phone or user send not his contact')
    await message.answer(text=LEXICON.get('bad_phone'), reply_markup=create_ask_phone())


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии по умолчанию и сообщать, что эта команда работает
# внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    logger.info('User send cancel command')
    await message.answer(text=LEXICON.get('nothing_cancel'))


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях, кроме состояния по умолчанию, и отключать
# машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext, bot: Bot):
    logger.info('User send start command during process creating tasks')
    msg_data = await state.get_data()
    if msg_data:
        await bot.edit_message_text(text=LEXICON.get('exit_fsm'), message_id=msg_data['msg_id'],
                                    chat_id=message.chat.id, reply_markup=None)
    else:
        await message.answer(text=LEXICON.get('exit_fsm'))
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Пользователь отправил боту свой номер телефона
@router.message(F.contact, StateFilter(FSMFillForm.fill_phone), IsUserContact())
async def user_entering_phone(message: Message, db_conn, state: FSMContext, url_hook):
    db = load_db(db_conn)
    photo_profile = FSInputFile('assets/profile_wo_phone.jpg', 'profile_wo_phone.jpg')
    photo_hd_bitrix = FSInputFile('assets/bitrix_hd.jpg', 'bitrix_hd.jpg')
    logger.info('User send his contact')

    db.save_phone(user_id=message.from_user.id, phone=int(message.contact.phone_number))

    # Получаем ид пользователя в Битрикс по номеру телефона
    buid, bitrix_user_last_name, bitrix_user_name = id_by_phone(db_conn, message.contact.phone_number)
    print(buid)

    if buid == 0:
        _, buid, bitrix_user_last_name, bitrix_user_name = search_user_by_phone(message.contact.phone_number,
                                                                                url_hook)

    if buid == 9999999:
        await message.answer(text=LEXICON.get('too_many_users'), reply_markup=ReplyKeyboardRemove())
        await message.answer_photo(photo_hd_bitrix)
        await state.clear()

    elif buid != 0:

        # Пользователь найден
        db.save_bitrix_data(
            user_id=message.from_user.id,
            b_uid=int(buid),
            b_user_name=bitrix_user_name,
            b_user_last_name=bitrix_user_last_name
        )
        # проверяем активность учетной записи пользователя
        if not check_user_active(buid, url_hook):
            await message.answer(LEXICON.get('not_active'))
            await state.clear()
        else:
            await message.answer(
                text=LEXICON.get('hello_user').format(bitrix_user_name, bitrix_user_last_name),
                reply_markup=ReplyKeyboardRemove()
            )
            cat_ids = [i for i in db.get_cats('tech_sup')]
            cat_ids = service(cat_ids)
            msg = await message.answer(text=LEXICON.get('choose_cat'),
                                       reply_markup=category_menu(cat_ids))
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(FSMFillForm.fill_cat)
    else:
        # Пользователь не найден
        await message.answer(text=LEXICON.get('no_user'), reply_markup=ReplyKeyboardRemove())
        await message.answer_photo(photo_profile)
        await state.clear()


# Этот хендлер сработает если пользователь поделится контактом в неожидаемое время
@router.message(StateFilter(FSMFillForm.fill_phone))
async def bad_phone(message: Message):
    logger.info("User send phone number when not current state")
    await message.answer(text=LEXICON.get('bad_phone'))


# Этот хэндлер будет срабатывать на команду "/help" и отправлять пользователю сообщение со списком доступных команд
# в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    logger.info('User send help command')
    await message.answer(LEXICON.get('/help'))


# Хендлер сработает если пользователь отправит команду старт в любых других слкчаях кроме описанных выше.
@router.message(CommandStart(), ~StateFilter(default_state))
async def start_in_fsm(message: Message):
    await message.answer(text=LEXICON.get('in_progress'))


@router.callback_query(StateFilter(FSMFillForm.fill_cat), IsChoosePerson())
async def choose_person(callback: CallbackQuery, state: FSMContext, bot: Bot):
    msg_data = await state.get_data()
    if msg_data:
        await bot.edit_message_text(text=LEXICON.get('first_line'), message_id=msg_data['msg_id'],
                                    chat_id=callback.message.chat.id, reply_markup=link_buttons('first_line'))
    logger.info('User call first line')
    await state.clear()


@router.callback_query(StateFilter(FSMFillForm.fill_cat), IsChoseCat())
async def choose_category(callback: CallbackQuery, db_conn, state: FSMContext, bot: Bot):
    db = load_db(db_conn)

    db.store_cat_id(user_id=callback.from_user.id, category_id=int(callback.data[-2:]))
    cat_list = db.get_category(category_id=int(callback.data[-2:]))

    if callback.data == '98':
        cat_list = srv_cats[0][1:]

    if not cat_list:
        return await callback.message.answer(text='Get error when read category from DB')
    # cat_id = db.get_cat_id(callback.from_user.id)
    # sla = db.get_sla(db.get_cat_id(callback.from_user.id))

    add_text = ''
    if additions.get(''.join(['tech_sup_', callback.data])):
        add_text = LEXICON.get('hint')
        for item in additions.get(''.join(['tech_sup_', callback.data])):
            add_text = '\n\n'.join([add_text, item])

    msg = [
        LEXICON.get('choosen_cat').format(cat_list[0]),
        cat_list[1],
        LEXICON.get('write_msg')
    ]
    if add_text:
        msg.insert(2, add_text)

    msg_text = '\n\n'.join(msg)

    msg_data = await state.get_data()
    if msg_data:
        msg = await bot.edit_message_text(text=msg_text, reply_markup=other_menu('return_btn'),
                                          message_id=msg_data['msg_id'], chat_id=callback.message.chat.id)
        await state.update_data(msg_id=msg.message_id)
    await callback.answer()
    await state.set_state(FSMFillForm.enter_problem)


@router.callback_query(StateFilter(FSMFillForm.enter_problem), IsPressedBackBtn())
async def back_to_choose_cat_menu(callback: CallbackQuery, state: FSMContext, db_conn, bot: Bot):
    await callback.answer()
    db = load_db(db_conn)
    cat_ids = [i for i in db.get_cats('tech_sup')]
    cat_ids = service(cat_ids)

    msg_data = await state.get_data()

    if msg_data:
        await bot.edit_message_text(text=LEXICON.get('choose_cat'), reply_markup=category_menu(cat_ids),
                                    message_id=msg_data['msg_id'], chat_id=callback.message.chat.id)

    await state.set_state(FSMFillForm.fill_cat)


@router.message(StateFilter(FSMFillForm.fill_cat))
async def no_category(message: Message):
    await message.answer(text=LEXICON['bad_category'])


@router.message(StateFilter(FSMFillForm.enter_problem))
@router.message(StateFilter(FSMFillForm.edit_problem))
async def get_info(message: Message, db_conn, state: FSMContext, bot: Bot):
    db = load_db(db_conn)

    msg_data = await state.get_data()
    msg_text = '\n\n'.join([LEXICON.get('check_user_msg'), LEXICON.get('user_msg').format(message.text)])

    if msg_data:
        await bot.edit_message_reply_markup(message_id=msg_data['msg_id'], chat_id=message.chat.id)

    msg = await message.answer(text=msg_text, reply_markup=other_menu(*msg_menu))
    await state.update_data(msg_id=msg.message_id)

    db.store_msg(message.from_user.id, message.text)
    await state.set_state(FSMFillForm.wait_user)


@router.callback_query(StateFilter(FSMFillForm.wait_user), IsEditMessage())
async def user_want_edit_msg(callback: CallbackQuery, state: FSMContext, bot: Bot):
    msg_data = await state.get_data()
    if msg_data:
        await bot.edit_message_reply_markup(message_id=msg_data['msg_id'], chat_id=callback.message.chat.id)
        await state.set_data({})
    await callback.answer(text=LEXICON.get('user_edit_msg'))
    await state.set_state(FSMFillForm.edit_problem)
    await callback.answer()


@router.callback_query(StateFilter(FSMFillForm.wait_user), IsSetTask())
async def set_task(callback: CallbackQuery, db_conn, state: FSMContext, url_hook, resp_id, group_id, bot: Bot):
    db = load_db(db_conn)
    msg_data = await state.get_data()
    if msg_data:
        await bot.edit_message_reply_markup(message_id=msg_data['msg_id'], chat_id=callback.message.chat.id)
        await callback.answer(text=LEXICON.get('sending_data'))

    b_uid = db.get_b_uid(user_id=callback.from_user.id)
    phone = db.get_phone(callback.from_user.id)
    user = db.get_b_username(user_id=callback.from_user.id)

    msg_text = db.get_user_msg(callback.from_user.id)[0]

    set_tasks, task_id, task_date = set_bitrix_task(
        url_hook=url_hook,
        user_id=b_uid,
        resp_id=resp_id,
        group_id=group_id,
        msg=LEXICON.get('set_b_task').format(msg_text, " ".join(user), phone[0]),
        title=db.get_category(db.get_user_cat(callback.from_user.id))[0],
        chat_id=callback.message.chat.id,
        sla=db.get_sla(db.get_cat_id(callback.from_user.id))
    )
    await state.clear()

    if set_tasks != 200:
        logger.error(f'Status code = {int(set_tasks)}, task = {task_id}, user = {callback.from_user.username}')
        logger.error(f'Can`t set task bitrix. Bitrix user id = {b_uid}')

        msg = await callback.message.answer(text=LEXICON.get('cant_create_task').format(str(set_task)))
        await state.update_data(msg_id=msg.message_id)

    await callback.message.answer(text=LEXICON.get('task_send').format(task_id, b_uid, task_id))
    logger.info(f'Task set successfully. ID: {task_id}, Creator: {" ".join(user)}, Creator id: {b_uid}')

    db.log_tasks(user_id=callback.from_user.id, bitrix_id=b_uid, task_id=task_id, task_date=task_date)
    logger.info('Stored data in db')

    await callback.message.answer(text=LEXICON.get('new_task'))
    if b_uid == 1028 or b_uid == 0:
        msg = await callback.message.answer(text=LEXICON.get('not_recognize'))
        await state.update_data(msg_id=msg.message_id)

    msg = await callback.message.answer(text=LEXICON.get('vote_me'), reply_markup=other_menu(*ynbtns))
    await state.update_data(msg_id=msg.message_id)
    await callback.answer()


@router.message(StateFilter(FSMFillForm.wait_user))
@router.message(StateFilter(FSMFillForm.fill_cat))
async def need_use_buttons(message: Message):
    await message.answer(text=LEXICON.get('need_use_btn'))


@router.callback_query(StateFilter(FSMFillForm.wait_user), IsCancelTask())
async def user_cancel_task(callback: CallbackQuery, state: FSMContext, bot: Bot):
    msg_text = '\n\n'.join([LEXICON.get('exit_fsm'), LEXICON.get('vote_me')])
    msg_data = await state.get_data()
    await state.clear()

    if msg_data:
        msg = await bot.edit_message_text(text=msg_text, reply_markup=other_menu(*ynbtns),
                                          message_id=msg_data['msg_id'], chat_id=callback.message.chat.id)
        await state.update_data(msg_id=msg.message_id)


@router.callback_query(IsUserHappy())
async def user_happy(callback: CallbackQuery, db_conn, state: FSMContext, bot: Bot):
    db = load_db(db_conn)
    b_uid = db.get_b_uid(user_id=callback.from_user.id)
    msg_data = await state.get_data()

    if msg_data:
        await bot.edit_message_text(text=LEXICON.get('user_happy_text'), message_id=msg_data['msg_id'],
                                    chat_id=callback.message.chat.id)
    db.set_vote_user(user_id=callback.from_user.id, vote='happy', vote_date=datetime.now(), bitrix_id=b_uid, comment='')


@router.callback_query(IsUserUnHappy())
async def user_unhappy(callback: CallbackQuery, state: FSMContext, bot: Bot):
    msg_data = await state.get_data()
    if msg_data:
        await bot.edit_message_text(text=LEXICON.get('user_unhappy_text'), message_id=msg_data['msg_id'],
                                    chat_id=callback.message.chat.id)
    await state.set_state(FSMFillForm.wait_user_comment)


@router.message(StateFilter(FSMFillForm.wait_user_comment))
async def get_unhappy_user_comment(message: Message, db_conn, state: FSMContext):
    db = load_db(db_conn)
    b_uid = db.get_b_uid(user_id=message.from_user.id)

    await message.answer(text=LEXICON.get('user_unhappy_comment'), )
    db.set_vote_user(
        user_id=message.from_user.id,
        vote='unhappy',
        vote_date=datetime.now(),
        bitrix_id=b_uid,
        comment=message.text
    )
    await state.clear()

# @router.callback_query(IsUserHappy(), ~StateFilter(FSMFillForm.wait_vote))
# @router.callback_query(IsUserUnHappy(), ~StateFilter(FSMFillForm.wait_vote))
# async def cant_vote(callback: CallbackQuery):
#     await callback.message.answer(text=LEXICON.get('no_vote'))
