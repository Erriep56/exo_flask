from flask import Flask, render_template, request

app = Flask(__name__)

from .routes import generales

if __name__ == '__main__':
    app.run(debug=True)