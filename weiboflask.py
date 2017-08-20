from flask import Flask, request, jsonify, g, render_template, redirect, url_for, session, current_app
import multi_NB as ada_real
import sys
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/hello/<word>")
def hello_user(word):
    temp = ada_real.test(word)
    print(temp)
    return str(temp)


@app.route("/helloscore/<word>")
def hello_score(word):
    score = ada_real.testandscore(word)
    score = json.dumps(score)
    print(score)
    return score


if __name__ == '__main__':
    app.run()
