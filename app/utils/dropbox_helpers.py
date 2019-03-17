import os
import uuid

from pathlib import Path

from dropbox.files import WriteMode
from flask import current_app as app
from werkzeug.utils import secure_filename

from app import dbx, db
from app.models import Visit, User, Family


def upload_visit_picture(file, user: User):
    """ Upload a visit image. """
    path = 'visits'
    extension = os.path.splitext(file.filename)[1]
    file_name = secure_filename(str(uuid.uuid4()) + extension)
    file_path = str(Path(app.config['DROPBOX_PATH']) / path / user.name_lower / file_name)
    dbx.files_upload(file.stream.read(), file_path, mode=WriteMode('overwrite'))

    visit = Visit(picture_path=file_path)
    visit.user_id = user.id
    visit.family_id = user.family_id
    user.visits.append(visit)
    db.session.add(visit)
    db.session.commit()


def upload_user_picture(file, user: User):
    """ Upload a user avatar image. """
    path = 'avatars'
    extension = os.path.splitext(file.filename)[1]
    file_name = secure_filename(str(uuid.uuid4()) + extension)
    file_path = str(Path(app.config['DROPBOX_PATH']) / path / user.name_lower / file_name)
    dbx.files_upload(file.stream.read(), file_path, mode=WriteMode('overwrite'))
    user.picture_path = file_path
    db.session.commit()


def upload_family_picture(file, family: Family):
    """ Upload a family avatar image. """
    path = 'avatars'
    extension = os.path.splitext(file.filename)[1]
    file_name = secure_filename(str(uuid.uuid4()) + extension)
    file_path = str(Path(app.config['DROPBOX_PATH']) / path / str(family.id) / file_name)
    dbx.files_upload(file.stream.read(), file_path, mode=WriteMode('overwrite'))

    family.picture_path = file_path
    db.session.commit()
