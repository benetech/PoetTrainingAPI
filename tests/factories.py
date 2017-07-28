# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from io import BytesIO

from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from werkzeug.datastructures import FileStorage

from poet.database import db
from poet.models import Upload, User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        """Factory configuration."""

        model = User


class UploadFactory(BaseFactory):
    """Upload factory."""

    filename = Sequence(lambda n: 'upload{0}.png'.format(n))
    retrieval_location = PostGenerationMethodCall(
        'save_file', FileStorage(stream=BytesIO(b'hello world'),
                                 filename='testfile.png'))

    class Meta:
        """Factory configuration."""

        model = Upload
