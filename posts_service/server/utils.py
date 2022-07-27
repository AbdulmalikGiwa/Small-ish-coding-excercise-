import ast
import json

from flask import jsonify
from marshmallow import Schema, ValidationError, fields
from tinydb.operations import set

from .tasks.config import Config
from .tasks.database import db
from .tasks.tasks import MLServerResponse, check_foul_language


def build_response(message="", data=None):
    # Wraps response data to ensure consistent response
    response = {"message": message, "data": data}
    return response


class PostSchema(Schema):
    title = fields.String(required=True)
    paragraphs = fields.List(fields.String())


def validate_posts(request_data):
    # Used to validate posts to ensure right body is sent
    schema = PostSchema()
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        response = build_response("validation error", err.messages)
        return jsonify(response), False

    return result, True


def create_post(result):
    # Adds post to database and concurrently calls ml service per paragraph
    result["hasFoulLanguage"] = None
    post_id = db.insert(result)
    paragraphs = result.get("paragraphs")
    ml_service = Config.ML_API
    for paragraph in paragraphs:
        json_data = ast.literal_eval(json.dumps({"fragment": paragraph}))
        result = check_foul_language.delay(json_data, ml_service).get()
        if result == MLServerResponse.true.value:
            db.update(
                set("hasFoulLanguage", True),
                doc_ids=[
                    post_id,
                ],
            )
            response = build_response("success", db.get(doc_id=post_id))
            return jsonify(response), 201
        elif result == MLServerResponse.false.value:
            db.update(
                set("hasFoulLanguage", False),
                doc_ids=[
                    post_id,
                ],
            )
            response = build_response("success", db.get(doc_id=post_id))
            return jsonify(response), 201

        elif result == MLServerResponse.unavailable.value:
            response = build_response("ML service Unavailable", {})
            return jsonify(response), 502
