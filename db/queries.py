from dataclasses import dataclass


@dataclass(frozen=True)
class Queries:
    create_user: str = """ INSERT INTO users (user_id, tg_name, chat_id) VALUES (%s, %s, %s)"""

    get_user: str = """SELECT user_id, bitrix_uid FROM users WHERE user_id = %s"""

    save_phone: str = """UPDATE users SET phone = %s WHERE user_id = %s"""

    store_b_data: str = """UPDATE users SET bitrix_uid = %s, bitrix_user_name = %s, bitrix_user_last_name = %s WHERE 
    user_id = %s"""

    store_cat_id: str = """ UPDATE users SET category = %s WHERE user_id = %s """

    get_category: str = """ SELECT cat_name, cat_descr FROM categories WHERE id = %s """

    store_msg: str = """ UPDATE users SET user_msg = %s WHERE user_id = %s """

    get_b_uid: str = """SELECT bitrix_uid FROM users where user_id = %s"""

    get_phone: str = """ SELECT phone FROM users WHERE user_id = %s """

    get_cat_id: str = """ SELECT category FROM users WHERE user_id = %s """

    get_b_user: str = """SELECT bitrix_user_name, bitrix_user_last_name FROM users WHERE user_id = %s """

    get_user_msg: str = """ SELECT user_msg FROM users WHERE user_id = %s """

    log_tasks: str = """INSERT INTO tasks (user_id, bitrix_id, task_id, task_date) VALUES (%s, %s, %s, %s)"""

    get_vote: str = """INSERT INTO marks (user_id, vote, vote_date, bitrix_id, comment) VALUES (%s, %s, %s, %s, %s)"""

    get_user_cat: str = """SELECT category FROM users WHERE user_id = %s"""

    get_vote_info: str = """SELECT m.vote, concat(u.bitrix_user_last_name, ' ', u.bitrix_user_name), m.comment 
    FROM marks m LEFT JOIN  users u ON m.user_id = u.user_id"""

    set_page: str = """UPDATE users SET page_num = %s where user_id = %s"""

    get_page: str = """SELECT page_num FROM users where user_id = %s"""

    get_cats_isd: str = """SELECT c.id FROM categories c WHERE c.cat_type = %s OR c.cat_type = 'other'"""

    get_cats: str = """SELECT id, cat_name FROM categories where cat_type = %s"""

    get_sla: str = """SELECT sla from categories where id = %s"""


@dataclass(frozen=True)
class BitrixQueries:
    get_phones: str = """SELECT bu.ID AS uid, bu.LAST_NAME AS last_name, bu.NAME AS name, bu.PERSONAL_MOBILE AS phone  
    FROM b_user bu"""

    get_name: str = """select bu.last_name, bu.name from b_user bu where bu.id = %s"""

    get_tg: str = """SELECT buu.VALUE_ID, buu.UF_USR_1658229353407 FROM b_uts_user buu 
    WHERE buu.UF_USR_1658229353407 IS NOT NULL"""

    check_user: str = """select bu.active from b_user bu where bu.id = %s"""
