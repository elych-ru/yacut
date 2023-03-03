import re
from typing import Tuple

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage, ShortLinkGenerationError
from .models import URLMap
from .views import gen_short_unique_link, check_short_id_exists
from .utils import is_url
from settings import RE_SHORT_LNK_SYMBOLS_ALLOWED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url_by_short_id(short_id: str) -> Tuple:
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage("Указанный id не найден", 404)
    return jsonify({"url": url_map.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_link() -> Tuple:
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data:
        raise InvalidAPIUsage("\"url\" является обязательным полем!")
    original = data["url"]
    if not is_url(original):
        raise InvalidAPIUsage("Некорректный url")
    if "custom_id" in data and data["custom_id"]:
        short_id = data["custom_id"]
        if len(short_id) > 16 or re.match(RE_SHORT_LNK_SYMBOLS_ALLOWED,
                                          short_id,
                                          ) is None:
            raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки")
        if check_short_id_exists(short_id):
            raise InvalidAPIUsage(f"Имя \"{short_id}\" уже занято.")
    else:
        # custom_id не задан - генерируем ссылку
        try:
            short_id = gen_short_unique_link()
        except ShortLinkGenerationError as err:
            raise InvalidAPIUsage(str(err), 500)
    # все проверки закончились - прописываем ссылку в базу
    url_map = URLMap(original=original,
                     short=short_id,
                     )
    db.session.add(url_map)
    db.session.commit()
    res = dict(url=original,
               short_link=f"{url_for('index_view', _external=True)}{url_map.short}",
               )
    return jsonify(res), 201
