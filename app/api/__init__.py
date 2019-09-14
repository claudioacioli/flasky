from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, errors, decorators, users, posts, comments
