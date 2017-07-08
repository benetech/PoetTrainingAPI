# -*- encoding: utf-8 -*-
"""Tests for the user API view functions."""
from uuid import uuid4

import pytest


@pytest.mark.usefixtures('db')
class TestFindUser:
    """Test the find_user view."""

    base_url = '/api/v1/users/{id}'

    def test_bad_guid(self, testapp):
        """Test it returns a 400 on a bad UUID."""
        res = testapp.get(self.base_url.format(id='asdf'), status=400)
        assert res.status_code == 400
        assert res.json

    def test_nonexistent_get(self, testapp):
        """Test that nonexistent find returns 404."""
        res = testapp.get(self.base_url.format(id=uuid4().hex), status=404)
        assert res.status_code == 404

    def test_existent_find(self, testapp, user):
        """Test finding a user works okay."""
        res = testapp.get(self.base_url.format(id=user.id))
        assert res.status_code == 200
        assert res.json['data']['id'] == str(user.id)
