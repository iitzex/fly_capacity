from flask import render_template
from flask import Flask, escape, request

from main import run
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    html = run()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    html += current_time
    # print(html)

    return render_template('index.html', html_col=html)


if __name__ == "__main__":
    app.run(debug=True, port=80)
