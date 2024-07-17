from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_list: list[int]


@dataclass
class DbConnect:
    path: str


@dataclass
class BitrixDbConnect:
    user: str
    password: str
    host: str
    port: str
    name: str


@dataclass
class BitrixConfig:
    url: str
    resp_id: str
    group_id: str


@dataclass
class MySqlConnect:
    user: str
    password: str
    host: str
    port: str
    name: str


@dataclass
class Config:
    tg_bot: TgBot
    bitrix_db: BitrixDbConnect
    bitrix: BitrixConfig
    db: MySqlConnect


def load_config(path: str) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        TgBot(
            token=env.str('BOT_TOKEN'),
            admin_list=list(map(int, env.list('ADMIN_IDS')))
        ),
        BitrixDbConnect(
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            port=env.str('DB_PORT'),
            name=env.str('DB_NAME')
        ),
        BitrixConfig(
            url=env.str('BITRIX_API_URL'),
            resp_id=env.str('BITRIX_RESP_ID'),
            group_id=env.str('BITRIX_GROUP_ID')
        ),
        MySqlConnect(
            user=env.str('BOT_USER'),
            password=env.str('BOT_PASS'),
            host=env.str('BOT_HOST'),
            port=env.str('BOT_PORT'),
            name=env.str('BOT_NAME')
        )
    )
