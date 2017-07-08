# -*- coding: utf-8 -*-
"""The API module for users."""
from flask import jsonify

from poet.errors import NotFound
from poet.locales import Errors
from poet.models import User
from poet.utils import RESTBlueprint

from .schema import UserSchema


blueprint = RESTBlueprint('users', __name__, version='v1')


@blueprint.find()
def find_user(uid):
    """Find a user by the UUID."""
    user = User.find(uid)
    if user is None:
        raise NotFound(Errors.USER_NOT_FOUND)
    return jsonify(data=UserSchema().dump(user).data)
