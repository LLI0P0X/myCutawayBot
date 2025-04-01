import secret
import os

BOT_TOKEN = secret.BOT_TOKEN
TOP_ADMINS = secret.TOP_ADMINS
GigaChatToken = secret.GigaChatToken
GPT_API_KEY = secret.GPT_API_KEY

gitHabUrl = 'https://github.com/LLI0P0X/myCutawayBot'
path = os.getcwd()
usrPath = '/home/admin'
usr = 'admin'

sqlite = True

try:
    if sqlite:
        raise AttributeError
    DB_ENGINE = 'postgresql+asyncpg'
    DB_NAME = secret.DB_NAME
    DB_USER = secret.DB_USER
    DB_PASSWORD = secret.DB_PASSWORD
    DB_HOST = secret.DB_HOST
    DB_PORT = 5432
    DB_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
except AttributeError:
    DB_URL = 'sqlite+aiosqlite:///db.sqlite'
