# -*- coding: utf-8 -*-
"""User schema."""
from marshmallow import Schema, fields


class UserSchema(Schema):
    """The base schema for a user."""
    created_at = fields.DateTime(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    id = fields.UUID(dump_only=True)

    class Meta:
        type_ = 'users'
        strict = True
