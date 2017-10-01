#!/usr/bin/env python


__author__ = "John W. O'Brien <obrienjw@upenn.edu>"

"""
Portions borrowed from Celery and Flask docs.
"""

import networkx

from flask import Flask
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(flask_app)


@celery.task()
def compute_max_flows():
    G = networkx.DiGraph()

    # load current topology and capacities from DB
    # XXX dummy data
    wedges = [
        ('leaf1', 'spine1', 9),
        ('spine1', 'leaf1', 10),
        ('leaf1', 'spine2', 8),
        ('spine2', 'leaf1', 11),
        ('spine1', 'vmx8', 15),
        ('spine1', 'vmx9', 5),
        ('vmx8', 'spine3', 10),
        ('vmx9', 'spine3', 12),
        ('spine3', 'leaf3', 100),
        # all the rest of the links and capacities here
    ]

    G.add_weighted_edges_from(wedges, weight='capacity')

    # iterate over pairwise endpoints
    for u in G:
        if 'leaf' not in u:
            continue
        for v in G:
            if 'leaf' not in v or v == u:
                continue
            # compute max flow and flow dict
            f, d = networkx.algorithms.flow.maximum_flow(G, u, v)
            print(u, v, f, d)

            # XXX store results back to DB
            """
            Two tables:
                1) timestamp, u, v, f
                2) timestamp, u, v, d as str
            """
