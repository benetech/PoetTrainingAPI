# -*- coding: utf-8 -*-
"""Upload schema."""
from marshmallow import Schema, fields


class UploadSchema(Schema):
    """The base schema for an upload."""

    created_at = fields.DateTime(dump_only=True)
    filename = fields.Str(dump_only=True)
    id = fields.UUID(dump_only=True)

    class Meta:
        type_ = 'uploads'
        strict = True
