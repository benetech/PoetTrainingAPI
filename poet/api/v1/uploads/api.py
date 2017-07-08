# -*- coding: utf-8 -*-
"""The API module for uploads."""
from flask import request, jsonify
from werkzeug.utils import secure_filename

from poet.errors import (BadRequest, NotFound, UnsupportedMediaType,
                         UnprocessableEntity)
from poet.locales import Errors
from poet.models import Upload
from poet.utils import RESTBlueprint

from .schema import UploadSchema


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

blueprint = RESTBlueprint('uploads', __name__, version='v1')


def allowed_file(filename):
    """Return TRUE if the file is allowed based on the extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.find()
def find_upload(uid):
    """Find an upload based on its ID."""
    # TODO: come back to this
    raise NotFound(Errors.RESOURCE_NOT_FOUND)


@blueprint.create()
def create_upload():
    """Create a new upload."""
    if 'file' not in request.files:
        raise BadRequest(Errors.FILE_NOT_SENT)
    file = request.files['file']
    if not file.filename:
        raise BadRequest(Errors.FILE_NAME_REQUIRED)
    if not allowed_file(file.filename):
        raise UnsupportedMediaType(Errors.IMAGE_TYPE_NOT_SUPPORTED)
    if not file:
        raise UnprocessableEntity(Errors.FILE_EMPTY)
    filename = secure_filename(file.filename)
    upload = Upload.create(filename=filename, file=file)
    return jsonify(data=UploadSchema().dump(upload))
