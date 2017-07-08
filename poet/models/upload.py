# -*- coding: utf-8 -*-
"""Upload models."""
import datetime as dt
import os
import uuid

from flask import current_app
from flask_login import current_user

from poet.database import (Column, Model, db, reference_col, relationship,
                           UUIDMixin)


class Upload(UUIDMixin, Model):
    """An upload submitted by a user."""

    __tablename__ = 'uploads'
    filename = Column(db.String(80), unique=True, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='uploads')

    # this column is internal and used to find & retrieve the file
    retrieval_location = Column(db.String(512), nullable=False)

    @classmethod
    def create(cls, filename, file):
        """Create a new upload from the parameters."""
        if current_user.is_authenticated:
            file_user = current_user
        else:
            file_user = None
        upload = cls(filename=filename, user=file_user)
        upload.save_file(file)
        return upload.save()

    def save_file(self, file):
        """Save the file to a destination based on the environment.

        This method should set the retrieval_location column.
        """
        if current_app.config['SAVE_UPLOADS_LOCALLY']:
            self.retrieval_location = self.save_file_locally(file)
        else:
            self.retrieval_location = self.save_file_to_s3(file)

    def save_file_locally(self, file):
        """Save a file to the local file system."""
        saved_filename = str(uuid.uuid4()) + "_{}".format(self.filename)
        fpath = os.path.join(current_app.config['UPLOADS_DIR'], saved_filename)
        file.save(fpath)
        return fpath

    def save_file_to_s3(self, file):
        """Save a file to some S3 bucket."""
        pass

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Upload({filename!r})>'.format(filename=self.filename)
