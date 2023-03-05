from http import HTTPStatus
import re
from typing import Tuple

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage, ShortLinkGenerationError
from yacut.models import URLMap
from yacut.views import gen_short_unique_link, check_short_id_exists
from yacut.utils import is_url
from yacut.settings import RE_SHORT_LNK_SYMBOLS_ALLOWED, MAX_SHORT_ID_LENGTH


@app.route("/api/id/<string:short_id>/", methods=("GET",))
def get_url_by_short_id(short_id: str) -> Tuple:
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK


@app.route("/api/id/", methods=("POST",))
def add_link() -> Tuple:
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    original = data["url"]
    if not is_url(original):
        raise InvalidAPIUsage("Некорректный url")
    if "custom_id" in data and data["custom_id"]:
        short_id = data["custom_id"]
        if (
            len(short_id) > MAX_SHORT_ID_LENGTH
            or re.match(RE_SHORT_LNK_SYMBOLS_ALLOWED, short_id) is None
        ):
            raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки")
        if check_short_id_exists(short_id):
            raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    else:
        # custom_id не задан - генерируем ссылку
        try:
            short_id = gen_short_unique_link()
        except ShortLinkGenerationError as err:
            raise InvalidAPIUsage(str(err), HTTPStatus.INTERNAL_SERVER_ERROR)
    # все проверки закончились - прописываем ссылку в базу
    url_map = URLMap(
        original=original,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()
    res = dict(
        url=original,
        short_link=f"{url_for('index_view', _external=True)}{url_map.short}",
    )
    return jsonify(res), HTTPStatus.CREATED
