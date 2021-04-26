from flask import render_template
from flask import Flask, escape, request

from main import run

app = Flask(__name__)


@app.route('/')
def index():
    r = escape(run())
    r = run()
    print(r)
    # return f'{r}!'
    return render_template('index.html', html_col=r)


if __name__ == "__main__":
    app.run(debug=True, port=80)
