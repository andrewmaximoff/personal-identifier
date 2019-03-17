from werkzeug.datastructures import FileStorage
from flask_restful import Resource, reqparse

from app.utils.dropbox_helpers import upload_visit_picture
from app.models import User


class VisitRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, help='user_id not blank and must be string', required=True)
    parser.add_argument('file', type=FileStorage, location='files', required=True)

    def post(self):
        args = self.parser.parse_args()
        file = args['file']
        user_id = args['user_id']
        user = User.query.get(user_id)
        if user:
            upload_visit_picture(file, user)
            return {'status': 'OK'}
        else:
            return {'status': f'User {user_id} doesn\'t exists'}
