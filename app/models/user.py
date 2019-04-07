import uuid

from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login, dbx


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(UUID(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    name_lower = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean)

    visits = db.relationship('Visit', backref='user', lazy='dynamic', cascade='delete')
    family_id = db.Column(UUID(), db.ForeignKey('family.id'))
    picture_path = db.Column(db.String(1024))

    def __init__(
            self,
            name: str,
            first_name: str,
            last_name: str,
            email: str,
            password: str,
            picture_path: Optional[str] = None,
            admin: bool = False,
    ):
        self.id = uuid.uuid4().urn
        self.name = name
        self.name_lower = name.lower()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.set_password(password)
        self.datetime = datetime.utcnow()
        if picture_path:
            self.picture_path = picture_path
        self.admin = admin

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_picture_url(self):
        if self.picture_path:
            return dbx.files_get_temporary_link(self.picture_path).link
        return None

    @property
    def last_visit(self):
        from app.models import Visit
        return self.visits.order_by(Visit.visit_date.desc()).first()

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

    def __str__(self):
        return f'<User {self.name}>'


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
