---
layout: post
title: Traveling Salesperson Problem in Python
date: 2023-06-21
image: "https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png"
downloads:
  - name: "💻 GitHub source"
    url: https://github.com/p13i/Traveling-Salesperson-Problem/blob/master/gt_tsp/held_karp.py#L9
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
