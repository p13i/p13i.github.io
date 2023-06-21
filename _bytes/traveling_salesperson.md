---
layout: post
title: Traveling Sales-person Problem
description: pip install gt-tsp
date: 2023-06-21
image: "https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png"
downloads:
  - name: "💻 GitHub source"
    url: https://github.com/p13i/Traveling-Salesperson-Problem/blob/master/gt_tsp/held_karp.py#L9
downloads:
  - name: "🐍 PyPi package from `pip`"
    url: https://pypi.org/project/gt-tsp/
---

```py
def solver(G, source):  # type: (nx.Graph, Any) -> Tuple[Tuple[Any, ...], int]
    """
    Produces the optimal TSP tour using the Held-Karp, dynamic programming
    approach - O(n^2 * 2^n)
    :param G: A fully connected networkx MultiDiGraph.
    :param source: A source node in G.
    :return: A list of nodes to visit, forming a TSP tour, and the cost of
    that tour.
    """

    utils.check_arguments(G, source)

    distance = utils.get_adjacency_dicts(G)

    min_cost_dp = {}  # type: Dict[Index, int]
    parent = {}  # type: Dict[Index, Any]

    nodes_except_source = list(G.nodes)
    nodes_except_source.remove(source)

    for _set in _power_set(nodes_except_source):  # type: set
        _set = set(_set)

        for current_vertex in nodes_except_source:
            if current_vertex in _set:
                continue

            index = Index(current_vertex, _set)

            min_cost = INFINITY

            min_prev_vertex = source

            set_copy = set(copy.deepcopy(_set))

            for prev_vertex in _set:
                cost = distance[prev_vertex][current_vertex] + \
                       _get_cost(set_copy, prev_vertex, min_cost_dp)

                if cost < min_cost:
                    min_cost = cost
                    min_prev_vertex = prev_vertex

            if len(_set) == 0:
                min_cost = distance[source][current_vertex]

            min_cost_dp[index] = min_cost
            parent[index] = min_prev_vertex

    _set = set(nodes_except_source)
    min_ = INFINITY
    prev_vertex = None
    set_copy = copy.deepcopy(_set)

    for vertex in _set:
        cost = distance[vertex][source] + \
               _get_cost(set_copy, vertex, min_cost_dp)
        if cost < min_:
            min_ = cost
            prev_vertex = vertex

    parent[Index(source, _set)] = prev_vertex

    tour = _get_tour(source, parent, G.nodes)

    return tour, min_
```

```py
"""
Implementation of Christofide's Algorithm for Traveling Salesman Problem!
Author: Pramod Kotipalli (pramodk@gatech.edu)

Properties:
- Approximation ratio of 3/2 (within 50% of optimal solution)
- O(n ^ 3) time runtime on graph with n nodes

References:
- https://en.wikipedia.org/wiki/Christofides_algorithm
- https://www.geeksforgeeks.org/backtracking-set-7-hamiltonian-cycle/

"""
import networkx as nx
import copy


def tsp_circuit(G, source_node):
    """
    Christofide's algorithm
    """
    # 1. Create an MST
    T = nx.minimum_spanning_tree(G)  # type: nx.Graph

    # 2. Get all odd nodes
    O = _get_nodes_with_odd_degree(T)

    # 3. Induce a sub-graph on the odd nodes
    subgraph_on_O = G.subgraph(O)

    # 4. Compute a minimum weight matching on the sub-graph
    M = _min_weight_matching(subgraph_on_O)

    # 5. Add the matching's edges to the MST
    _add_matching_to_mst(T, M)

    # 6. Compute a Hamiltonian circuit
    path = _hamilton_circuit(T, source=source_node)

    return path


def _get_nodes_with_odd_degree(G):
    nodes = []
    for node in G.nodes:
        if nx.degree(G, node) % 2 == 1:
            nodes.append(node)
    return nodes


def _min_weight_matching(G):  # type: (nx.Graph) -> set
    nodes = copy.deepcopy(set(G.nodes))

    matching = set()

    while nodes:
        v = nodes.pop()
        min_weight = float('inf')
        closest = None

        if not nodes:
            raise ValueError("G has an odd number of nodes")

        for u in nodes:
            edge = G.get_edge_data(u, v, default=None)
            if edge is not None and edge['weight'] < min_weight:
                min_weight = edge['weight']
                closest = u

        matching.add((v, closest, min_weight))
        nodes.remove(closest)

    return matching


def _add_matching_to_mst(T, M):
    for u, v, weight in M:
        T.add_edge(u, v, weight=weight)


def _hamilton_circuit(G, source):
    ham_path = [source]

    path_found = _hamilton_circuit_helper(G, source, ham_path)

    if not path_found:
        return None

    return ham_path


def _hamilton_circuit_helper(G, source, ham_path):  # type: (nx.Graph, []) -> bool
    # If the path has all the nodes of G, check if there is an edge back to the source
    if len(ham_path) == G.number_of_nodes():
        edge_back_to_source = G.get_edge_data(ham_path[-1], source, default=None)
        if edge_back_to_source is not None:
            ham_path.append(source)
            return True
        else:
            return False

    for node in G.nodes:
        edge = G.get_edge_data(ham_path[-1], node, default=None)

        if edge is not None and node not in ham_path:
            ham_path.append(node)

            if _hamilton_circuit_helper(G, source, ham_path):
                return True

            # Else, the path wasn't proper, so backtrack
            ham_path.pop(len(ham_path) - 1)

    return False
```