from typing import Dict, Tuple, Union
from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app, db


class InvalidAPIUsage(Exception):
    def __init__(
        self, message: str, status_code: Union[int, None] = HTTPStatus.BAD_REQUEST
    ):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict:
        return dict(message=self.message)


class ShortLinkGenerationError(BaseException):
    pass


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> Tuple:
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error: BaseException) -> Tuple:
    return render_template("404.html"), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error: BaseException) -> Tuple:
    db.session.rollback()
    return render_template("500.html"), HTTPStatus.INTERNAL_SERVER_ERROR
