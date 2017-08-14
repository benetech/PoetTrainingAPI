# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('POET_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SAVE_UPLOADS_LOCALLY = True
    SEND_EMAILS = False
    S3_UPLOADS_BUCKET = os.environ.get('S3_UPLOADS_BUCKET', 'poet-uploads')
    UPLOADS_DIR = os.path.join(APP_DIR, 'local_uploads')
    # limit uploads to 16 MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@benetech.org')
    CC_EMAIL = os.environ.get('CC_EMAIL', 'some-email@benetech.org')
    EMAIL_SUBJECT = os.environ.get(
        'EMAIL_SUBJECT', 'Your image annotation from Poet Training!')
    REPLY_TO_EMAIL = os.environ.get(
        'REPLY_TO_EMAIL', 'poet-support@benetech.org')
    BASE_CDN_HOST = os.environ.get('BASE_CDN_HOST',
                                   's3-us-west-2.amazonaws.com')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SAVE_UPLOADS_LOCALLY = False
    SEND_EMAILS = True


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://poet:poet123@localhost:5432/poet'
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://poet:poet123@localhost:5432/poet_test'
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4
