from datetime import datetime, timedelta

import pandas as pd
import requests

from db.mysql_db import load_bitrix_db


def id_by_phone(mysql_conn, phone):
    db = load_bitrix_db(mysql_conn)
    phone = phone.strip('+')

    df = pd.DataFrame(
        data=db.get_phones(),
        columns=['uid', 'last_name', 'name', 'phone']
    )
    df['clear_phone'] = df['phone'].apply(lambda x: ''.join([j for j in x if j.isdigit()]) if x else '-')
    filtered_df = df[df.clear_phone.str.contains(phone[1:])]
    if not filtered_df.empty:
        return filtered_df['uid'].iloc[0], filtered_df['last_name'].iloc[0], filtered_df['name'].iloc[0]
    return 0, 'undefine', 'undefine'


def set_bitrix_task(url_hook: str, user_id: int, msg: str, title: str, chat_id: int, resp_id: str, group_id: str):
    date = (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M")
    params = {
        "fields[CREATED_BY]": user_id,
        "fields[RESPONSIBLE_ID]": resp_id,
        "fields[TITLE]": ' '.join([title, "(telegram)"]),
        "fields[DESCRIPTION]": msg,
        "fields[GROUP_ID]": group_id,
        "fields[TAGS][0]": title,
        "fields[TAGS][1]": 'Telegram',
        "fields[TAGS][2]": 'helpdesk',
        "fields[DEADLINE]": date,
        "fields[UF_CHAT_ID]": chat_id
    }
    r = requests.get(f'{url_hook}tasks.task.add.json', params=params, verify=False)

    if r.status_code != 200:
        return r.status_code, 0, 0
    return r.status_code, r.json()['result']['task']['id'], r.json()['result']['task']['createdDate']


def get_user_name(buid, mysql_conn):
    db = load_bitrix_db(mysql_conn)
    return db.get_user_name((buid,))


def id_by_tg(tg_name, mysql_conn):
    db = load_bitrix_db(mysql_conn)
    df = pd.DataFrame(
        data=db.get_tg(),
        columns=['uid', 'tg']
    )
    df['tg_name'] = df.tg.apply(lambda x: x.replace('@', '').replace('https://t.me/', ''))
    filtered_df = df[df.tg_name == tg_name]['uid']
    if not filtered_df.empty:
        data = get_user_name(mysql_conn=mysql_conn, buid=(filtered_df.iloc[0],))[0]
        print(data)
        print(get_user_name(mysql_conn=mysql_conn, buid=(filtered_df.iloc[0],)))
        if data:
            return filtered_df.iloc[0], data[0], data[1]
    return 0, 'undefine', 'undefine'


def user_check(buid, mysql_conn):
    db = load_bitrix_db(mysql_conn)
    df = pd.DataFrame(
        data=db.check_user((buid,)),
        columns=['active']
    )
    if not df.empty:
        return True if df['active'].loc[0] == 'Y' else False
    return False
