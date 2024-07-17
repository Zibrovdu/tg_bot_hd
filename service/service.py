
def _prepare_text(data) -> str:
    text = ''
    for i in data:
        text = ''.join([text, '<b>Оценка:</b> ', 'Положительная\n' if i[0] == 'happy' else 'Отрицательная\n'])
        text = ''.join([text, '<b>Пользователь:</b> ', str(i[1]), '\n'])
        text = ''.join([text, '<b>Комментарий:</b> ', i[2], '\n\n*'])

    return text


def _split_vote_data(page_size, text):
    if len(text) < page_size:
        return len(text), text.replace('*', '').strip('\n\n')
    while text[page_size] != '*':
        page_size -= 1
    return page_size, text[:page_size].replace('*', '').strip('\n\n')


def prepare_messages(data, page_size) -> dict[int: str]:
    book: dict[int, str] = {}

    i = 1

    text = _prepare_text(data)

    while len(text) > 0:
        book[i] = _split_vote_data(page_size, text)[1]
        text = text[_split_vote_data(page_size, text)[0]:]
        i += 1

    return book


def count_stat(data) -> tuple:
    positive, negative = 0, 0
    for vote in data:
        if 'happy' in vote:
            positive += 1
        elif 'unhappy' in vote:
            negative += 1
    return positive, negative
