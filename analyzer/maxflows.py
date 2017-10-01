#!/usr/bin/env python

__author__ = "John W. O'Brien <obrienjw@upenn.edu>"


import random
import json

import networkx
import requests


endpoint = 'host'


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


def compute_max_flows(wedges):
    G = networkx.DiGraph()
    G.add_weighted_edges_from(wedges, weight='capacity')

    # iterate over pairwise endpoints
    max_flows = []
    link_capacities = []
    for u in G:
        if endpoint not in u:
            continue
        for v in G:
            if endpoint not in v or v == u:
                continue
            # compute max flow and flow dict
            f, d = networkx.algorithms.flow.maximum_flow(G, u, v)

            max_flows.append((u, v, f))
            link_capacities.append((u, v, d))
    return max_flows, link_capacities


if __name__ == '__main__':
    # load current topology and capacities from DB
    state = random.choice(state_names)
    wedges = load_wedges(state + '.tsv')

    max_flows, capacities = compute_max_flows(wedges)
    with open('www/latest.json', 'wt') as f:
        f.write(json.dumps(max_flows))
    with open('www/capacities.json', 'wt') as f:
        f.write(json.dumps(capacities))
