from flask import Flask, jsonify, request

from .tasks.config import Config
from .tasks.database import db
from .utils import create_post, validate_posts, build_response

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/posts/", methods=["POST", "GET"])
def blog_server():
    if request.method == "POST":
        result, validated = validate_posts(request.json)
        if validated:
            response, code = create_post(result)
        else:
            return result, 400
        return response, code

    if request.method == "GET":
        # Returns all posts in db
        return jsonify(build_response(message="success", data=db.all()))


if __name__ == "__main__":
    app.run()
