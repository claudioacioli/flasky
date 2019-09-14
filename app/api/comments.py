from flask import request, url_for, jsonify, current_app
from . import api as app_api
from ..models import Comment


@app_api.route('/comments')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(disabled=False).paginate(
        page,
        per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    prev = url_for('api_get_comments', page=page - 1) if pagination.has_prev else None
    next = url_for('api.get_comments', page=page + 1) if pagination.has_next else None
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total
    })
