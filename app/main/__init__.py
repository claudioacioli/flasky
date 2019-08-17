from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permission():
    """Injeta dicionario de permissoes nos templates da main"""
    return dict(Permission=Permission)

