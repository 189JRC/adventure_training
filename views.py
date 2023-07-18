import markdown
from flask import Flask, render_template, request, flash, redirect, url_for


app = Flask(__name__)


@app.route('/')
def index():
    f = open("sample.md", "r")
    md = markdown.markdown(f.read())
    return render_template('base.html', content=md)


if __name__ == "__main__":
    app.run()
