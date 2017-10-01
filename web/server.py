#!/usr/bin/env python3

import requests
from collections import defaultdict
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from influxdb import InfluxDBClient
from random import randint

INFLUX_ENDPOINT = 'http://'
LEAF_DATA_URL = 'http://199.187.223.134:8000/latest.json'
CAPACITIES_DATA_URL = 'http://199.187.223.134:8000/capacities.json'

app = Flask(__name__)
Bootstrap(app)


def get_influx_client() -> InfluxDBClient:
    return InfluxDBClient('199.187.220.207', 8083, 'user', 'pass', 'wadus')


def get_info(url):  # type () -> List[List[str, str, int]]
    resp = requests.get(url)
    return resp.json()


@app.route('/', methods=['GET'])
def home():
    leaf_metrics = defaultdict(dict)
    for near, far, metric in get_info(LEAF_DATA_URL):
        leaf_metrics[near].update({
            far: metric
        })
    headers = leaf_metrics.keys()

    capacities = get_info(CAPACITIES_DATA_URL)

    return render_template(
        'home.html',
        headers=headers,
        leaf_metrics=dict(leaf_metrics),
        capacities=capacities,
    )

if __name__ == '__main__':
    app.run()
