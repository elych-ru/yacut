from string import ascii_letters, digits as a_digits
from random import choices
from urllib.parse import urlparse


def gen_random_str(length: int = 6) -> str:
    """Функция возвращает строку нужной длины из случайных символов."""
    return ''.join(choices(ascii_letters + a_digits, k=length))


def is_url(url: str) -> bool:
    """Функция проверяет, является ли строка корректным URL'ом."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
