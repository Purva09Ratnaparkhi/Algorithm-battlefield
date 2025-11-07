"""Shortest Path Algorithms"""

import heapq
from collections import defaultdict


def dijkstra(graph, start):
    """Dijkstra's Algorithm - Finds shortest path using greedy approach"""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances


def bellman_ford(graph, start):
    """Bellman-Ford Algorithm - Works with negative weights"""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Relax edges V-1 times
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph.get(node, []):
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
    
    # Check for negative cycles
    for node in graph:
        for neighbor, weight in graph.get(node, []):
            if distances[node] + weight < distances[neighbor]:
                return None  # Negative cycle detected
    
    return distances


def floyd_warshall(graph):
    """Floyd-Warshall Algorithm - All pairs shortest path"""
    nodes = list(graph.keys())
    n = len(nodes)
    
    # Initialize distance matrix
    dist = {node: {n: float('inf') for n in nodes} for node in nodes}
    
    for node in nodes:
        dist[node][node] = 0
    
    for node in graph:
        for neighbor, weight in graph.get(node, []):
            dist[node][neighbor] = weight
    
    # Floyd-Warshall computation
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist
