# -*- coding: utf-8 -*-
"""Module with the SQLAlchemy database and DB-related utilities."""
import uuid

from sqlalchemy.dialects.postgresql import UUID

from .errors import BadRequest
from .compat import basestring
from .extensions import db
from .locales import Errors

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a 'primary key' column named ``id`` to a model."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


class UUIDMixin(object):
    """A mixin like SurrogatePK, but uses PostgreSQL's UUID type."""

    __table_args = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                default=uuid.uuid4)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by UUID."""
        if not isinstance(record_id, uuid.UUID):
            try:
                record_id = uuid.UUID(record_id)
            except:
                raise BadRequest(Errors.BAD_GUID)
        return cls.query.get(record_id)

    @classmethod
    def find(cls, record_id):
        """Alias for get_by_id."""
        return cls.get_by_id(record_id)


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
