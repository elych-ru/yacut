from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for, Response

from yacut import app, db
from yacut.error_handlers import ShortLinkGenerationError
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import gen_random_str
from yacut.settings import INDEX_TEMPLATE


def check_short_id_exists(short_id: str) -> bool:
    """Ищет запись по короткой ссылке и возвращает True/False."""
    return bool(URLMap.query.filter_by(short=short_id).first())


def gen_short_unique_link(tries: int = 10) -> str:
    """Генерирует уникальную короткую ссылку.

    После генерации значения проверяет его уникальность в базе, если ссылка не
    уникальная, пытается сгенерировать tries раз. Вероятность этого крайне низка, но
    если такое случилось - выбрасывается исключение ShortLinkGenerationError.
    Возвращает сгенерированную уникальную строку.
    """

    count = 0
    while count < tries:
        short_id = gen_random_str()
        if not check_short_id_exists(short_id):
            return short_id
        count += 1
    msg = f"Не удалось сгенерировать уникальную ссылку с {count} попыток"
    raise ShortLinkGenerationError(msg)


@app.route("/", methods=("GET", "POST"))
def index_view() -> str:
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_TEMPLATE, form=form)
    short_id = form.custom_id.data
    if not short_id:
        # короткая ссылка пуста - нужно сгенерировать
        try:
            short_id = gen_short_unique_link()
        except ShortLinkGenerationError as err:
            flash(str(err), "short-message")
            return render_template(INDEX_TEMPLATE, form=form)
    elif check_short_id_exists(short_id):
        flash(f"Имя {short_id} уже занято!", "short-message")
        return render_template(INDEX_TEMPLATE, form=form)
    url_map = URLMap(
        original=form.original_link.data,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()
    flash("Ваша новая ссылка готова:", "info")
    flash(f"{url_for('index_view', _external=True)}{url_map.short}", "info-link")
    return render_template(INDEX_TEMPLATE, form=form)


@app.route("/<string:short_id>", methods=("GET",))
def redirect_short(short_id: str) -> Response:
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
