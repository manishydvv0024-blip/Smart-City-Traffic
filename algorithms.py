"""Shortest-path algorithms: Dijkstra and Bellman-Ford."""
import heapq

INF = float("inf")


class NegativeCycleError(Exception):
    pass


def dijkstra(graph, source):
    """Binary-heap Dijkstra. O((V + E) log V). Requires non-negative weights."""
    dist = {v: INF for v in graph.adj}
    prev = {v: None for v in graph.adj}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                            # stale entry
        for v, w in graph.adj[u]:
            if w < 0:
                raise ValueError("Dijkstra does not support negative weights")
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def bellman_ford(graph, source):
    """Bellman-Ford with early exit. O(V * E). Handles negative weights."""
    dist = {v: INF for v in graph.adj}
    prev = {v: None for v in graph.adj}
    dist[source] = 0
    for _ in range(graph.num_vertices - 1):
        changed = False
        for u, v, w in graph.edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                changed = True
        if not changed:
            break
    for u, v, w in graph.edges:                 # negative-cycle check
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise NegativeCycleError("Graph contains a negative-weight cycle")
    return dist, prev


def reconstruct_path(prev, source, target):
    path, cur = [], target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == source else []
