from dataclasses import dataclass

from environs import Env

AVAILABLE_COMMANDS = ["/start", "/help", "/create", "/get", "/delete"]
CREATOR = '@Rocky_0013'


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class RedisConfig:
    host: str
    port: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        redis=RedisConfig(
            host=env.str('REDIS_HOST'),
            port=env.str('REDIS_PORT')
        ),
        misc=Miscellaneous()
    )
