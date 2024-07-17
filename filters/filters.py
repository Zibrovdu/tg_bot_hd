from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
# from lexicon.lexicon import menu_items


class IsChoseCat(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsEditMessage(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'edit_msg'


class IsSetTask(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'set_task'


class IsCancelTask(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'cancel_task'


class IsUserHappy(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'user_happy'


class IsUserUnHappy(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'user_unhappy'


class IsPressedBackBtn(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'return_btn'


class IsUserContact(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (message.contact.user_id == message.from_user.id) and (message.contact.vcard is None)


class IsUserAdmin(BaseFilter):
    async def __call__(self, message: Message, admin_list) -> bool:
        return message.from_user.id in admin_list


class IsChoosePerson(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == '10'
