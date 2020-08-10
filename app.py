from flask import Flask, request
import model

application = Flask(__name__)
model_runner = model.ModelRunner()


@application.route("/api/score-post", methods=["POST"])
def score_post():
    payload = request.get_json()
    score = model_runner.predict(payload)
    return str(round(score))


if __name__ == "__main__":
    application.run(threaded=True, port=5000)
