# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, jsonify


blueprint = Blueprint('public', __name__)


@blueprint.route('/healthcheck')
def healthcheck():
    """Return a health check for the ELB."""
    return jsonify(status='ok')
