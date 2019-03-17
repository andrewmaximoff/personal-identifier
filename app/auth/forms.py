from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    SubmitField,
    StringField,
    BooleanField
)
from flask_wtf.file import FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    ValidationError
)

from app import db
from app.models import User


class LoginForm(FlaskForm):
    name = StringField('Name', [DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    name = StringField('Username', [
        DataRequired(),
        Length(min=4, max=32),
    ])
    first_name = StringField('First name', [
        DataRequired(),
        Length(min=4, max=32),
    ])
    last_name = StringField('Last name', [
        DataRequired(),
        Length(min=4, max=32),
    ])
    email = EmailField('Email', [
        DataRequired(),
        Length(min=4, max=256),
    ])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
    ])
    confirm = PasswordField('Repeat Password', [
        DataRequired(),
    ])
    admin = BooleanField(
        'Admin',
        default=False
    )
    user_picture = FileField(
        'User picture'
    )

    def validate_email(form, field):
        if db.session.query(db.exists().where(
                User.email == field.data.lower())
        ).scalar():
            raise ValidationError(f'{field.data} is already taken.')

    def validate_name(form, field):
        if db.session.query(db.exists().where(
                User.name_lower == field.data.lower())
        ).scalar():
            raise ValidationError(f'{field.data} is already taken.')
