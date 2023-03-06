from flask import (Flask,
                   )
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def hello():
    return 'Hello World!!!'


if __name__ == '__main__':
    app.run()
