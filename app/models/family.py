import uuid
from typing import Optional

from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.orm import relationship

from app import db, dbx


class Family(db.Model):
    __tablename__ = 'family'
    id = db.Column(UUID(), primary_key=True)
    users = db.relationship('User', backref='family', lazy='dynamic', cascade='delete')
    visits = db.relationship('Visit', backref='family', lazy='dynamic', cascade='delete')
    picture_path = db.Column(db.String(1024))

    def __init__(self, picture_path: Optional[str] = None):
        self.id = uuid.uuid4().urn
        if picture_path:
            self.picture_path = picture_path

    @property
    def get_picture_url(self):
        if self.picture_path:
            return dbx.files_get_temporary_link(self.picture_path).link
        return None

    def __repr__(self):
        return f'<Family {self.id}>'

    def __str__(self):
        return f'<Family {self.id}>'
