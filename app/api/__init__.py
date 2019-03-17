from flask import Blueprint
from flask_restful import Api

from app.api.resources.visit import (
    VisitRegistration,
)


bp = Blueprint('api', __name__)
api = Api(bp)

# Visit endpoints
api.add_resource(VisitRegistration, '/visit/registration/')
