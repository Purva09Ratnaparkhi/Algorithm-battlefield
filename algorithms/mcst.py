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
    """Kruskal's Algorithm - MST using Union-Find"""
    
    class UnionFind:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n
        
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px == py:
                return False
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            return True
    
    edges_sorted = sorted(edges, key=lambda x: x[2])
    uf = UnionFind(len(nodes))
    mst = []
    
    for u, v, weight in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, weight))
    
    return mst
