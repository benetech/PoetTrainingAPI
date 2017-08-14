# -*- coding: utf-8 -*-
"""Annotation models."""
import datetime as dt

from poet.database import (Column, Model, db, reference_col, relationship,
                           UUIDMixin)


class Annotation(UUIDMixin, Model):
    """An annotation submitted by a user."""

    __tablename__ = 'annotations'
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='annotations')
    upload_id = reference_col('uploads', nullable=False)
    upload = relationship('Upload', backref='annotations')
    description = Column(db.Text, nullable=False)
