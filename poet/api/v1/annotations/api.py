# -*- coding: utf-8 -*-
"""The API module for annotations."""
from flask import jsonify, request
from flask_login import current_user

from poet.errors import NotFound
from poet.locales import Errors, Success
from poet.models import Annotation, Upload
from poet.utils import RESTBlueprint

from .schema import AnnotationSchema


blueprint = RESTBlueprint('annotations', __name__, version='v1')


def get_annotation_by_id(annotation_id):
    """Get an annotation given its ID or bail via some API error."""
    annotation = Annotation.find(annotation_id)
    if annotation is None:
        raise NotFound(Errors.RESOURCE_NOT_FOUND)
    return annotation


@blueprint.find()
def find_annotation(uid):
    """Find an annotation based on its ID."""
    return jsonify(data=AnnotationSchema().dump(get_annotation_by_id(uid)).data)


@blueprint.create()
def create_annotation():
    """Create a new annotation."""
    annotation_data = AnnotationSchema().load(request.json).data
    upload = Upload.find(annotation_data['upload_id'])
    if upload is None:
        raise NotFound(Errors.RESOURCE_NOT_FOUND)
    annotation_user = None
    if current_user.is_authenticated:
        annotation_user = current_user
    annotation = Annotation.create(user=annotation_user, **annotation_data)
    return jsonify(data=AnnotationSchema().dump(annotation).data,
                   message=Success.ANNOTATION_CREATED)
