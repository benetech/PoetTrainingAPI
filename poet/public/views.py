# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, jsonify, render_template

from poet.extensions import login_manager


blueprint = Blueprint('public', __name__)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return None


@blueprint.route('/healthcheck')
def healthcheck():
    """Return a health check for the ELB."""
    print('test log')
    return jsonify(status='ok')


@blueprint.route('/test-upload')
def index():
    """Test page for uploads."""
    return render_template('index.html')
