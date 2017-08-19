from flask import Flask

import multi_NB as ada_real

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/hello/<word>")
def hello_user(word):
    temp =ada_real.test(word)
    return str(temp)


if __name__ == '__main__':
    app.run()
