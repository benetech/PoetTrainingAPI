# -*- coding: utf-8 -*-
"""Upload models."""
import datetime as dt
import os
import uuid
from io import BytesIO

import boto3
from flask import current_app
from flask_login import current_user

from poet.database import (Column, Model, db, reference_col, relationship,
                           UUIDMixin)


class Upload(UUIDMixin, Model):
    """An upload submitted by a user."""

    __tablename__ = 'uploads'
    filename = Column(db.String(80), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='uploads')

    # this column is internal and used to find & retrieve the file
    retrieval_location = Column(db.String(512), nullable=False)

    @classmethod
    def create(cls, filename, upload_file):
        """Create a new upload from the parameters.

        :param filename string: the name of the file (includes extension)
        :param upload_file file-like: the file-like object which will be read
            and saved
        :return Upload: the created upload
        """
        if current_user.is_authenticated:
            file_user = current_user
        else:
            file_user = None
        upload = cls(filename=filename, user=file_user)
        upload.save_file(upload_file)
        return upload.save()

    def save_file(self, upload_file):
        """Save the file to a destination based on the environment.

        :param upload_file file-like: the file pointer to read and save
        :return: None

        This method should set the retrieval_location column.

        Note that a new file cannot be saved if the upload has already saved a
        file.
        """
        if self.retrieval_location is not None:
            raise RuntimeError('cannot overwrite an upload\'s file')
        if current_app.config['SAVE_UPLOADS_LOCALLY']:
            self.retrieval_location = self.save_file_locally(upload_file)
        else:
            self.retrieval_location = self.save_file_to_s3(upload_file)

    def save_file_locally(self, upload_file):
        """Save a file to the local file system.

        :param upload_file file-like: the file pointer to read and save
        :return string: the string of where the file the file locally
        """
        saved_filename = str(uuid.uuid4()) + "_{}".format(self.filename)
        fpath = os.path.join(current_app.config['UPLOADS_DIR'], saved_filename)
        upload_file.save(fpath)
        return fpath

    def save_file_to_s3(self, upload_file):
        """Save a file to some S3 bucket.

        :param upload_file file-like: the file pointer to read and save
        :return string: the string of where the file the file in the S3 bucket
        """
        s3 = boto3.resource('s3')
        saved_filename = str(uuid.uuid4()) + "_{}".format(self.filename)
        s3.Object(current_app.config['S3_UPLOADS_BUCKET'], saved_filename)\
            .put(Body=upload_file)
        return saved_filename

    def retrieve_file(self):
        """Return the file as a file pointer that is open to be read.

        :return file-like: object
        """
        if current_app.config['SAVE_UPLOADS_LOCALLY']:
            return self.get_local_file()
        else:
            return self.get_s3_file()

    def get_local_file(self):
        """Return a file pointer to the local file.

        :return file-like:
        """
        return open(self.retrieval_location, 'rb')

    def get_s3_file(self):
        """Return a file pointer to the S3 object.

        :return file-like:
        """
        s3 = boto3.client('s3')
        fp = BytesIO()
        s3.download_fileobj(current_app.config['S3_UPLOADS_BUCKET'],
                            self.retrieval_location, fp)
        return fp

    @property
    def cdn_link(self):
        """A link to the CDN location for the file attached to the upload."""
        return 'https://{host}/{dir}/{fname}'.format(
            host=current_app.config['BASE_CDN_HOST'],
            dir=current_app.config['S3_UPLOADS_BUCKET'],
            fname=self.retrieval_location)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Upload({filename!r})>'.format(filename=self.filename)
