"""Minimum Spanning Tree Algorithms"""


def prim(graph, start_node=None):
    """Prim's Algorithm - Greedy MST algorithm"""
    if not graph:
        return []
    
    if start_node is None:
        start_node = list(graph.keys())[0]
    
    mst = []
    visited = {start_node}
    edges = []
    
    # Add all edges from start node
    for neighbor, weight in graph.get(start_node, []):
        edges.append((weight, start_node, neighbor))
    
    edges.sort()
    
    while edges and len(visited) < len(graph):
        weight, u, v = edges.pop(0)
        
        if v in visited:
            continue
        
        visited.add(v)
        mst.append((u, v, weight))
        
        # Add new edges
        for neighbor, w in graph.get(v, []):
            if neighbor not in visited:
                edges.append((w, v, neighbor))
        
        edges.sort()
    
    return mst


def kruskal(edges, nodes):
    parent = {}
    rank = {}

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            elif rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            else:
                parent[root_v] = root_u
                rank[root_u] += 1

    # Initialize disjoint sets
    for node in nodes:
        parent[node] = node
        rank[node] = 0

    # Sort edges by weight
    edges.sort(key=lambda x: x[2])

    mst = []
    for u, v, w in edges:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, w))

    return mst
