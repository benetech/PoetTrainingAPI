# -*- encoding: utf-8 -*-
"""Tests for the uploads API view functions."""
from io import BytesIO
from uuid import uuid4

from flask_login import login_user
import pytest


@pytest.mark.usefixtures('db')
class TestCreateUpload:
    """Test the create_upload view."""

    base_url = '/api/v1/uploads'

    def test_upload_file_success(self, testapp, user):
        """Test uploading files works fine."""
        login_user(user)
        res = testapp.post(
            self.base_url,
            upload_files=[
                ('file', 'test.png', b'this is a test file')])
        assert res.status_code == 200

    def test_upload_file_anonymous(self, testapp):
        """Test uploading files works fine when not logged in."""
        res = testapp.post(
            self.base_url,
            upload_files=[
                ('file', 'test.png', b'this is a test file')])
        assert res.status_code == 200

    def test_no_file_sent(self, testapp):
        """Test uploading without a file fails."""
        res = testapp.post(self.base_url, status=400)
        assert res.status_code == 400

    def test_misnamed_param(self, testapp):
        """Test uploading with the wrong parameter name fails."""
        res = testapp.post(
            self.base_url,
            upload_files=[
                ('myfile', 'test.png', b'this is a test file')], status=400)
        assert res.status_code == 400

    def test_no_filename(self, testapp):
        """Test uploading without a filename fails."""
        res = testapp.post(
            self.base_url,
            upload_files=[
                ('file', '', b'this is a test file')], status=400)
        assert res.status_code == 400

    def test_bad_mediatype(self, testapp):
        """Test uploading with a non image type fails."""
        res = testapp.post(
            self.base_url,
            upload_files=[
                ('file', 'test.pdf', b'this is a test file')], status=415)
        assert res.status_code == 415


@pytest.mark.usefixtures('db')
class TestGetUpload:
    """Test the find_upload view."""

    base_url = '/api/v1/uploads/{}'

    def test_get_nonexistent_upload(self, testapp):
        """Test that getting an upload that doesnt exist returns a 404."""
        res = testapp.get(self.base_url.format(uuid4()), status=404)
        assert res.status_code == 404

    def test_get_upload_works(self, testapp, upload):
        """Test that getting an upload works."""
        res = testapp.get(self.base_url.format(upload.id))
        assert res.status_code == 200
        data = res.json['data']
        assert data['id'] == str(upload.id)
