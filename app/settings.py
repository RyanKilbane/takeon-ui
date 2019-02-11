import os
from app.utilities.helpers import str_to_bool

DEBUG = str_to_bool(os.getenv('DEBUG', default="False"))

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = os.getenv('SECRET_KEY')

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.getenv('SECRET_KEY')

APP_NAME = "Take_On_UI"
PORT = 5000

MOCKING = str_to_bool(os.getenv('MOCKING', default="False"))

TOKEN_ENDPOINT = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
ENCODING = "utf-8"
