from flask import Flask, request
from model import model

application = Flask(__name__)


@application.route("/api/score-post", methods=["POST"])
def score_post():
    payload = request.get_json()
    score = model.predict(payload)
    return str(score)


if __name__ == "__main__":
    application.run(threaded=True, port=5000)
