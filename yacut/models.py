from datetime import datetime
from typing import Dict

from yacut import db
from yacut.settings import MAX_LINK_LENGTH, MAX_SHORT_ID_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LINK_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_ID_LENGTH),
        nullable=False,
        index=True,
        unique=True,
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict:
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data: Dict) -> None:
        for field in ("original", "short"):
            if field in data:
                setattr(self, field, data[field])


def get_url_map_by_short_id(short_id: str) -> URLMap:
    return URLMap.query.filter_by(short=short_id).first()
