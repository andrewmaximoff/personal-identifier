from datetime import datetime

from werkzeug.datastructures import FileStorage
from flask_restful import Resource, reqparse

from app import socketio
from app.models import User, Family
from app.utils.dropbox_helpers import upload_visit_picture


class VisitRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='username not blank and must be string', required=True)
    parser.add_argument('family_id', type=str, help='family_id not blank and must be string', required=True)
    parser.add_argument('file', type=FileStorage, location='files', required=True)

    def post(self):
        args = self.parser.parse_args()
        file = args['file']
        username = args['username']
        family_id = args['family_id']

        user = User.query.filter_by(name=username).first()
        family = Family.query.get(family_id)

        if user is None:
            upload_visit_picture(file, user, family)
            socketio.emit(
                'new_visit',
                {
                    'user': 'Unknown',
                    'datetime': str(datetime.utcnow().strftime("%H:%M:%S %p"))
                },
                namespace='/visit'
            )
            return {'status': 'OK'}

        if user.family_id == family.id:
            upload_visit_picture(file, user, family)
            socketio.emit(
                'new_visit',
                {
                    'user': user.full_name,
                    'datetime': str(datetime.utcnow().strftime("%H:%M:%S %p"))
                },
                namespace='/visit'
            )
            return {'status': 'OK'}
        else:
            return {'status': f'User {username} doesn\'t exists or incorrect family_id'}
