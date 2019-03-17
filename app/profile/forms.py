from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    SubmitField,
    StringField,
    BooleanField
)
from flask_login import current_user
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


class FamilyProfileUpdateForm(FlaskForm):
    family_picture = FileField(
        'Family picture'
    )


class UserProfileUpdateForm(FlaskForm):
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
    user_picture = FileField(
        'User picture'
    )

    def validate_email(form, field):
        if db.session.query(db.exists().where(
                User.email == field.data.lower())
        ).scalar():
            if current_user.email != field.data.lower():
                raise ValidationError(f'{field.data} is already taken.')

    def validate_name(form, field):
        if db.session.query(db.exists().where(
                User.name_lower == field.data.lower())
        ).scalar():
            if current_user.name_lower != field.data.lower():
                raise ValidationError(f'{field.data} is already taken.')


class NewUserForm(FlaskForm):
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
        default=True
    )
    user_picture = FileField(
        'User picture'
    )

    def validate_email(form, field):
        if db.session.query(db.exists().where(
                User.email == field.data.lower())
        ).scalar():
            if current_user.email != field.data.lower():
                raise ValidationError(f'{field.data} is already taken.')

    def validate_name(form, field):
        if db.session.query(db.exists().where(
                User.name_lower == field.data.lower())
        ).scalar():
            if current_user.name_lower != field.data.lower():
                raise ValidationError(f'{field.data} is already taken.')


class DeleteUserForm(FlaskForm):
    name = StringField('Username', [
        Length(min=4, max=32),
        DataRequired()
    ])
    submit = SubmitField('Delete')
