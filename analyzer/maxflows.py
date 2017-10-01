#!/usr/bin/env python

__author__ = "John W. O'Brien <obrienjw@upenn.edu>"


import random

import networkx
import requests


state_names = [
    'nominal',
    'reversed',
    'degraded',
]


def load_wedges(fname):
    with open(fname) as f:
        wedges = []
        for line in f:
            u, v, c = line.strip().split('\t')
            c = int(c)
            wedges.append(tuple((u, v, c)))
    return wedges


def compute_max_flows():
    G = networkx.DiGraph()

    # load current topology and capacities from DB
    state = random.choice(state_names)
    wedges = load_wedges(state + '.tsv')

    G.add_weighted_edges_from(wedges, weight='capacity')

    # iterate over pairwise endpoints
    results = []
    for u in G:
        if 'leaf' not in u:
            continue
        for v in G:
            if 'leaf' not in v or v == u:
                continue
            # compute max flow and flow dict
            f, d = networkx.algorithms.flow.maximum_flow(G, u, v)
            #print(u, v, f, d)

            # XXX store results back to DB
            """
            Two tables:
                1) timestamp, u, v, f
                2) timestamp, u, v, d as str
            """
            results.append((u, v, f))
    return results


if __name__ == '__main__':
    results = compute_max_flows()
    print(results)
