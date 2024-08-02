from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_phone = State()         # Состояние ожидания передачи контакта
    fill_cat = State()           # Состояние ожидания выбора категории обращения
    enter_problem = State()      # Состояние ожидания ввода описания обращения
    wait_user = State()
    upload_photo = State()       # Состояние ожидания загрузку изображения
    edit_problem = State()       # Состояние ожидания редактирования сообщения
    wait_vote = State()
    wait_user_comment = State()  # Ждем комментарий пользователя почему не понравился бот
