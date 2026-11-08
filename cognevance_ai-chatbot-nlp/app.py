"""Flask web interface.   python app.py   ->  open http://127.0.0.1:5000"""
from flask import Flask, jsonify, render_template, request, session

from src import config as cfg
from src.chatbot import Chatbot

app = Flask(__name__)
app.secret_key = "change-this-secret-key"      # needed for the per-user session (name memory)
bot = Chatbot()


@app.route("/")
def index():
    return render_template("index.html", bot_name=cfg.BOT_NAME)


@app.route("/chat", methods=["POST"])
def chat():
    message = (request.get_json(silent=True) or {}).get("message", "")
    state = {"name": session.get("name")}
    result = bot.respond(message, state)
    if state.get("name"):
        session["name"] = state["name"]
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False)
