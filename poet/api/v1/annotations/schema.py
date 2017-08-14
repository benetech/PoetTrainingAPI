# -*- coding: utf-8 -*-
"""Annotation schema."""
from marshmallow import Schema, fields

from poet.api.v1.uploads.schema import UploadSchema


class AnnotationSchema(Schema):
    """The base schema for an annotation."""

    created_at = fields.DateTime(dump_only=True)
    description = fields.Str(required=True)
    id = fields.UUID(dump_only=True)
    upload = fields.Nested(UploadSchema, dump_only=True)
    upload_id = fields.UUID(load_only=True, required=True)

    class Meta:
        type_ = 'annotations'
        strict = True
