from flask import jsonify, request, current_app, url_for
from . import api as app_api
from .decorators import permission_required
from ..models import User, Post


def _get_posts(posts, page):
    pagination = posts.paginate(
        page,
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    prev = url_for('api.get_user_posts', page=page - 1) if pagination.has_prev else None
    next = url_for('api.get_user_posts', page=page + 1) if pagination.has_next else None
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total
    })


@app_api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@app_api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    return _get_posts(user.posts, page)


@app_api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    return _get_posts(user.followed_posts, page)

