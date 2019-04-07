import os
import uuid

from pathlib import Path
from typing import Union

from dropbox.files import WriteMode
from flask import current_app as app
from werkzeug.utils import secure_filename

from app import dbx, db
from app.models import Visit, User, Family


def upload_visit_picture(file, user: Union[User, None], family: Family):
    """ Upload a visit image. """
    path = 'visits'
    extension = os.path.splitext(file.filename)[1]
    file_name = secure_filename(str(uuid.uuid4()) + extension)
    if user is None:
        file_path = str(Path(app.config['DROPBOX_PATH']) / path / str(family.id) / 'unknown' / file_name)
    else:
        file_path = str(Path(app.config['DROPBOX_PATH']) / path / user.name_lower / file_name)
    dbx.files_upload(file.stream.read(), file_path, mode=WriteMode('overwrite'))

    visit = Visit(picture_path=file_path)
    if user:
        visit.user_id = user.id
    visit.family_id = family.id
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
