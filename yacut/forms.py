from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from yacut.settings import (
    RE_SHORT_LNK_SYMBOLS_ALLOWED,
    MAX_SHORT_ID_LENGTH,
    MAX_LINK_LENGTH,
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(1, MAX_LINK_LENGTH),
            URL(message="Введите корректный URL (http://...)"),
        ],
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Length(1, MAX_SHORT_ID_LENGTH),
            Optional(),
            Regexp(
                regex=RE_SHORT_LNK_SYMBOLS_ALLOWED,
                message="Используйте только символы A-Z, a-z, 0-9",
            ),
        ],
    )
    submit = SubmitField("Создать")
