import MySQLdb
import MySQLdb.converters
from db.queries import Queries


class CustomList(list):
    def __init__(self, *items):
        super(CustomList, self).__init__(items)


conv = MySQLdb.converters.conversions.copy()
conv[CustomList] = lambda lst, conv_: "(%s)" % ', '.join(str(item) for item in lst)


class Connection:
    def __init__(self, config):
        self.db = MySQLdb.connect(
            config.host,
            config.user,
            config.password,
            config.name,
            conv=conv
        )
        self.db.autocommit(True)
        self.db.set_character_set('utf8mb4')
        self.cur = self.db.cursor()

    def execute_select_command(self, command: str, params: tuple):
        if self.cur:
            self.cur.execute(command, params)
            return self.cur.fetchall()
        else:
            raise ConnectionError("You need to create connection to DB")

    def execute_command(self, command: str, params: tuple):
        if self.cur:
            self.cur.execute(command, params)
        else:
            raise ConnectionError("You need to create connection to DB")

    def close_curr(self):
        if self.cur:
            self.cur.close()

    def literal(self, params):
        self.db.literal(params)

    def close_dbconn(self):
        if self.db:
            self.db.close()


class MySqlDb:
    def __init__(self, database_client: Connection):
        self.database_client = database_client

    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(Queries.get_user, (user_id,))
        return user[0] if user else user

    def create_user(self, user_id: str, tg_name: str, chat_id: int):
        self.database_client.execute_command(Queries.create_user, (user_id, tg_name, chat_id))

    def save_phone(self, user_id: int, phone: int):
        self.database_client.execute_command(Queries.save_phone, (phone, user_id))

    def save_bitrix_data(self, user_id: int, b_uid: int, b_user_name: str, b_user_last_name: str):
        self.database_client.execute_command(
            Queries.store_b_data,
            (b_uid, b_user_name, b_user_last_name, user_id))

    def store_cat_id(self, user_id: int, category_id: int):
        self.database_client.execute_command(Queries.store_cat_id, (category_id, user_id))

    def get_category(self, category_id: int):
        cat_info = self.database_client.execute_select_command(Queries.get_category, (category_id,))
        return cat_info[0] if cat_info else 0

    def store_msg(self, user_id: int, msg: str):
        self.database_client.execute_command(Queries.store_msg, (msg, user_id))

    def get_b_uid(self, user_id: int):
        b_uid = self.database_client.execute_select_command(Queries.get_b_uid, (user_id,))
        return b_uid[0][0] if b_uid else 0

    def get_phone(self, user_id: int):
        phone = self.database_client.execute_select_command(Queries.get_phone, (user_id,))
        return phone[0] if phone else 0

    def get_b_username(self, user_id: int):
        b_user = self.database_client.execute_select_command(Queries.get_b_user, (user_id,))
        return b_user[0] if b_user else b_user

    def get_user_msg(self, user_id: int):
        user_msg = self.database_client.execute_select_command(Queries.get_user_msg, (user_id,))
        return user_msg[0] if user_msg else 0

    def log_tasks(self, user_id: int, bitrix_id: int, task_id: int, task_date):
        self.database_client.execute_command(
            Queries.log_tasks,
            (user_id, bitrix_id, task_id, task_date))

    def set_vote_user(self, user_id: int, vote: str, vote_date, bitrix_id: int, comment: str):
        self.database_client.execute_command(
            Queries.get_vote,
            (user_id, vote, vote_date, bitrix_id, comment))

    def get_user_cat(self, user_id: int):
        cat_info = self.database_client.execute_select_command(Queries.get_user_cat, (user_id,))
        return cat_info[0][0] if cat_info else 0

    def get_vote_info(self):
        vote_info = self.database_client.execute_select_command(Queries.get_vote_info, ())
        return vote_info

    def set_page(self, page: int, user_id: int):
        self.database_client.execute_command(Queries.set_page, (page, user_id))

    def get_page(self, user_id: int):
        page = self.database_client.execute_select_command(Queries.get_page, (user_id,))
        return page

    def get_categories_ids(self, cat_type: str):
        cat_ids = self.database_client.execute_select_command(Queries.get_cats_isd, (cat_type,))
        return cat_ids

    def get_cats(self, cat_type: str):
        cats = self.database_client.execute_select_command(Queries.get_cats, (cat_type,))
        return cats

    def get_sla(self, cat_id: int):
        sla = self.database_client.execute_select_command(Queries.get_sla, (cat_id, ))
        return sla[0][0] if sla else 8

    def get_cat_id(self, user_id: int):
        cat_id = self.database_client.execute_select_command(Queries.get_cat_id, (user_id,))
        return cat_id[0][0]

    def get_phones(self):
        phones = self.database_client.execute_select_command(Queries.get_phones, ())
        return phones

    def get_tg(self):
        tg = self.database_client.execute_select_command(Queries.get_tg, ())
        return tg

    def get_user_name(self, buid: int):
        user = self.database_client.execute_select_command(Queries.get_name, (buid,))
        return user


def load_db(mysql_conn):
    db = MySqlDb(Connection(mysql_conn))
    return db
