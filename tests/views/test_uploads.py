# -*- encoding: utf-8 -*-
"""Tests for the uploads API view functions."""
from uuid import uuid4

from flask_login import login_user
import pytest


@pytest.mark.usefixtures('db')
class TestCreateUpload:
    """Test the find_user view."""

    base_url = '/api/v1/uploads'

    def test_upload_file_success(self, testapp, user):
        """Test uploading files works fine."""
        login_user(user)
        res = testapp.post(
            self.base_url,
            upload_files=[
                ('file', 'test.pdf', b'this is a test file')])
        assert res.status_code == 200
