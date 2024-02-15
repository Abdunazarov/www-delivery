# stdlib
import os

# thirdparty
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_URL_SYNC = os.environ["DATABASE_URL_SYNC"]
CURRENCY_API = "https://www.cbr-xml-daily.ru/daily_json.js"
BROKER_URL = "redis://redis:6379/0"
