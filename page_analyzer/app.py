from flask import (Flask,
                   render_template
                   )
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    """
    Render index.html.
    return: Render index.html.
    """

    return render_template(
        'index.html',
    )


if __name__ == '__main__':
    app.run()
