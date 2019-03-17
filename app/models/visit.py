import uuid

from typing import Optional
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, TEXT
from app import dbx, db


class Visit(db.Model):
    __tablename__ = 'visit'
    id = db.Column(UUID(), primary_key=True)
    visit_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(UUID(), db.ForeignKey('user.id'), nullable=False)
    family_id = db.Column(UUID(), db.ForeignKey('family.id'), nullable=False)
    picture_path = db.Column(db.String(1024))

    def __init__(self, picture_path: Optional[str] = None):
        self.id = uuid.uuid4().urn
        self.picture_path = picture_path

    @property
    def get_picture_url(self):
        if self.picture_path:
            return dbx.files_get_temporary_link(self.picture_path).link
        return None

    def __repr__(self):
        return f'<Visit {self.user.full_name}>'

    def __str__(self):
        return f'<Visit {self.user.full_name}>'
