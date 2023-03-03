from typing import Dict, Tuple, Union

from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    status_code: int = 400
    message: str

    def __init__(self, message: str, status_code: Union[int, None] = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> Dict:
        return dict(message=self.message)


class ShortLinkGenerationError(BaseException):
    pass


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> Tuple:
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error: BaseException) -> Tuple:
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error: BaseException) -> Tuple:
    db.session.rollback()
    return render_template('500.html'), 500
