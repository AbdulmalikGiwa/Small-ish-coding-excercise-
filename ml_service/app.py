from flask import Flask, request

app = Flask(__name__)

foul_words = [
    "cunt",
    "fuck",
    "wanker",
    "bollocks",
    "crap",
    "damn",
    "prick",
    "twat",
    "pussy",
]


@app.route("/sentences/", methods=["POST"])
def hello_world():
    sentence = request.json.get("fragment")
    if not sentence:
        return "Bad request", 400
    # checks if any word in sentence is in defined list of foul words
    return {"hasFoulLanguage": any(s in sentence.lower() for s in foul_words)}


if __name__ == "__main__":
    app.run()
