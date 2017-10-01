#!/usr/env/python3

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from random import randint
from typing import List

app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET'])
def home():
    path_details: Dict[str, Dict] = {}

    peers: List[str] = ['H1', 'H2', 'H3']
    for name in ('H1', 'H2', 'H3'):
        path_details[name] = {
            p: randint(0, 100) for p in peers
        }

    return render_template(
        'home.html',
        path_details=path_details,
    )

if __name__ == '__main__':
    app.run()
