import json
from unittest import TestCase
from unittest.mock import patch

from posts_service.server.app import app
from posts_service.server.tasks.database import db
from posts_service.server.tasks.tasks import MLServerResponse
from posts_service.server.utils import build_response


class CeleryTest:
    """
    This class helps in writing tests to mock celery, the value returned from celery tasks is
    received using a .get() method. and in mocking the check_foul_language task that runs on
    the celery worker, we need something that implements .get() to be used as the return value.
    """

    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class APITest(TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        self.request_body = {
            "title": "This is an engaging title",
            "paragraphs": [
                "This is the first paragraph. It contains two sentences.",
                "This is the second parapgraph. It contains two more sentences",
                "Third paraphraph here.",
            ],
        }
        self.posts_path = "/posts/"
        self.bad_request_body = {}

    def tearDown(self) -> None:
        # Resets the request body
        self.request_body = {
            "title": "This is an engaging title",
            "paragraphs": [
                "This is the first paragraph. It contains two sentences.",
                "This is the second parapgraph. It contains two more sentences",
                "Third paraphraph here.",
            ],
        }
        # drops table
        db.drop_table("posts")

    @patch("posts_service.server.tasks.tasks.check_foul_language.delay")
    def test_post_request_no_foul_language(self, check_foul_language):
        check_foul_language.return_value = CeleryTest(MLServerResponse.false.value)
        response = app.test_client().post(
            self.posts_path,
            data=json.dumps(self.request_body),
            content_type="application/json",
        )
        new_body = self.request_body
        new_body["hasFoulLanguage"] = False
        json_response = build_response(message="success", data=new_body)
        assert response.status_code == 201
        assert response.json == json_response

    @patch("posts_service.server.tasks.tasks.check_foul_language.delay")
    def test_post_request_foul_language(self, check_foul_language):
        check_foul_language.return_value = CeleryTest(MLServerResponse.true.value)
        response = app.test_client().post(
            self.posts_path,
            data=json.dumps(self.request_body),
            content_type="application/json",
        )
        new_body = self.request_body
        new_body["hasFoulLanguage"] = True
        json_response = build_response(message="success", data=new_body)
        assert response.status_code == 201
        assert response.json == json_response

    @patch("posts_service.server.tasks.tasks.check_foul_language.delay")
    def test_bad_request(self, check_foul_language):
        check_foul_language.return_value = CeleryTest(MLServerResponse.true.value)
        response = app.test_client().post(
            self.posts_path,
            data=json.dumps(self.bad_request_body),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert response.json["message"] == "validation error"

    @patch("posts_service.server.tasks.tasks.check_foul_language.delay")
    def test_ml_service_unreachable(self, check_foul_language):
        check_foul_language.return_value = CeleryTest(
            MLServerResponse.unavailable.value
        )
        response = app.test_client().post(
            self.posts_path,
            data=json.dumps(self.request_body),
            content_type="application/json",
        )
        json_response = build_response(message="ML service Unavailable", data={})
        assert response.status_code == 502
        assert response.json == json_response
