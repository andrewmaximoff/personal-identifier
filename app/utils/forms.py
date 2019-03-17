from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from app.utils.validators import UUID


class DeleteForm(FlaskForm):
    id = StringField('ID', [Length(max=64), DataRequired(), UUID()])
    submit = SubmitField('Delete')
