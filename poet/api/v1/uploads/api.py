# -*- coding: utf-8 -*-
"""The API module for uploads."""
from botocore.exceptions import ClientError
from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename

from poet.errors import (BadRequest, NotFound, UnsupportedMediaType,
                         UnprocessableEntity)
from poet.locales import Errors
from poet.models import Upload
from poet.utils import RESTBlueprint

from .schema import UploadSchema


ALLOWED_EXTENSIONS = set(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'])

blueprint = RESTBlueprint('uploads', __name__, version='v1')


def allowed_file(filename):
    """Return TRUE if the file is allowed based on the extension."""
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in ALLOWED_EXTENSIONS


def get_upload_by_id(upload_id):
    """Get a file given its ID or bail via some API error."""
    upload = Upload.find(upload_id)
    if upload is None:
        raise NotFound(Errors.RESOURCE_NOT_FOUND)
    return upload


@blueprint.find()
def find_upload(uid):
    """Find an upload based on its ID."""
    return jsonify(data=UploadSchema().dump(get_upload_by_id(uid)).data)


@blueprint.flexible_route('/<string:uid>/file')
def get_upload_file(uid):
    """Get an upload's file attachment by its ID."""
    upload = get_upload_by_id(uid)
    try:
        upload_fp = upload.retrieve_file()
    except (FileNotFoundError, ClientError):
        raise NotFound(Errors.FILE_NOT_FOUND)
    return send_file(upload_fp, as_attachment=True,
                     attachment_filename=upload.filename)


@blueprint.create()
def create_upload():
    """Create a new upload."""
    # validate to make sure that a file was uploaded, that it wasn't empty,
    # and that it has an acceptable extension
    if 'file' not in request.files:
        raise BadRequest(Errors.FILE_NOT_SENT)
    upload_file = request.files['file']
    if not upload_file.filename:
        raise BadRequest(Errors.FILE_NAME_REQUIRED)
    if not allowed_file(upload_file.filename):
        raise UnsupportedMediaType(Errors.IMAGE_TYPE_NOT_SUPPORTED)
    if not upload_file:
        raise UnprocessableEntity(Errors.FILE_EMPTY)

    filename = secure_filename(upload_file.filename)
    upload = Upload.create(filename=filename, upload_file=upload_file)
    return jsonify(data=UploadSchema().dump(upload).data)
