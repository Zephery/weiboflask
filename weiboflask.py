from flask import Flask, request, jsonify, g, render_template, redirect, url_for, session, current_app
import multi_NB as ada_real
import sys

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/hello/<word>")
def hello_user(word):
    temp = ada_real.test(word)
    return word + "   " + str(temp)


if __name__ == '__main__':
    print(sys.path)
    app.run()
