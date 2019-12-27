from flask import Flask, request

application = Flask(__name__)


@application.route("/api/score-post", methods=["POST"])
def score_post():
    payload = request.get_json()
    # Make the score equal the length of the title for now
    score = len(payload)
    return str(score)


if __name__ == "__main__":
    application.run(threaded=True, port=5000)
