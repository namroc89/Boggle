from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "lots-of-secrets"


@app.route("/")
def make_boggle_board():
    """Start game with a new board. Displays 
    number of games played and Highest score"""
    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore")
    times_played = session.get("times_played")

    return render_template("index.html",
                           board=board,
                           times_played=times_played,
                           highscore=highscore)


@app.route("/check-word")
def check_word():
    """checks if word is valid. Sends back 
    either ok, not-on-board or not-word"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify(response=response)


@app.route("/post-score", methods=["POST"])
def post_score():
    """posts score to session and checks to see if it 
    is the highscore. Also adds 1 to games played"""
    score = request.json["score"]
    times_played = session.get("times_played", 0)
    highscore = session.get("highscore", 0)

    session["highscore"] = max(score, highscore)
    session["times_played"] = times_played + 1
    highscore = session.get("highscore")
    times_played = session.get("times_played")
    return jsonify(score=score, highscore=highscore, times_played=times_played)
