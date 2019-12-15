from flask import Flask, request

application = Flask(__name__)


@application.route('/')
def index():
    return "<h1>Welcome to our server</h1>"


@application.route("/score-post", methods=["POST"])
def score_post():
    payload = request.args.get("title")
    # Make the score equal the length of the title for now
    score = len(payload)
    return score


if __name__ == "__main__":
    application.run(threaded=True, port=5000)
