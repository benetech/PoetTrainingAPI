# -*- coding: utf-8 -*-
"""Tests for the annotations API routes."""
from uuid import uuid4

import pytest


@pytest.mark.usefixtures('db')
class TestFindAnnotation:
    """Test the find_annotation view."""

    base_url = '/api/v1/annotations/{id}'

    def test_bad_guid(self, testapp):
        """Test it returns a 400 on a bad UUID."""
        res = testapp.get(self.base_url.format(id='asdf'), status=400)
        assert res.status_code == 400
        assert res.json

    def test_nonexistent_get(self, testapp):
        """Test that nonexistent find returns 404."""
        res = testapp.get(self.base_url.format(id=uuid4().hex), status=404)
        assert res.status_code == 404

    def test_existent_find(self, testapp, annotation):
        """Test finding an annotation works okay."""
        res = testapp.get(self.base_url.format(id=annotation.id))
        assert res.status_code == 200
        assert res.json['data']['id'] == str(annotation.id)


@pytest.mark.usefixtures('db')
class TestCreateAnnotation:
    """Test the create_annotation view."""

    base_url = '/api/v1/annotations'

    def test_no_upload_id(self, testapp):
        """Test that create without an upload_id fails."""
        res = testapp.post_json(
            self.base_url, {'description': 'this is a description'}, status=422)
        print(res)
        assert 'upload_id' in res.json['error_message']

    def test_bad_upload_id(self, testapp):
        """Test that a bad upload_id fails."""
        res = testapp.post_json(
            self.base_url,
            {'description': 'this is a description',
             'upload_id': str(uuid4())}, status=404)
        assert res.status_code == 404

    def test_annotation_create_works(self, testapp, upload):
        """Test that creating an annotation works fine."""
        desc = 'this is a description'
        res = testapp.post_json(self.base_url,
                                {'description': desc,
                                 'upload_id': str(upload.id)})
        assert res.status_code == 200
        assert res.json['message']
        assert res.json['data']['description'] == desc
