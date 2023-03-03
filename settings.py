import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


# шаблон главной страницы
INDEX_TEMPLATE = "index.html"
# регулярка, допускающая только символы A-Z, a-z, 0-9 в строке
RE_SHORT_LNK_SYMBOLS_ALLOWED = r"^[A-Za-z\d]+$"
