from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from settings import RE_SHORT_LNK_SYMBOLS_ALLOWED


class URLMapForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[DataRequired(message="Обязательное поле"),
                    Length(1, 256),
                    URL(message="Введите корректный URL (http://...)")]
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[Length(1, 16),
                    Optional(),
                    Regexp(regex=RE_SHORT_LNK_SYMBOLS_ALLOWED,
                           message="Используйте только символы A-Z, a-z, 0-9",
                           )
                    ]
    )
    submit = SubmitField("Создать")
