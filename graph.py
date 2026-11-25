"""Graph representation: locations are vertices, roads are weighted edges."""
import random


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = {}      # vertex -> list of (neighbour, weight)  (for Dijkstra)
        self.edges = []    # flat list of directed (u, v, weight)    (for Bellman-Ford)

    def add_vertex(self, v):
        self.adj.setdefault(v, [])

    def add_edge(self, u, v, w):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append((v, w))
        self.edges.append((u, v, w))
        if not self.directed:
            self.adj[v].append((u, w))
            self.edges.append((v, u, w))

    @property
    def vertices(self):
        return list(self.adj)

    @property
    def num_vertices(self):
        return len(self.adj)

    @property
    def num_edges(self):
        return len(self.edges)


def generate_city_graph(n, avg_degree=4, max_weight=100, seed=42):
    """Random connected city graph with n intersections.

    A random spanning tree guarantees connectivity; extra roads are added
    until the requested average degree is reached.
    """
    rng = random.Random(seed)
    g = Graph()
    for v in range(n):
        g.add_vertex(v)
    existing = set()
    for v in range(1, n):                       # spanning tree
        u = rng.randrange(v)
        g.add_edge(u, v, rng.randint(1, max_weight))
        existing.add((min(u, v), max(u, v)))
    target = max(n - 1, n * avg_degree // 2)
    while len(existing) < target and len(existing) < n * (n - 1) // 2:
        u, v = rng.sample(range(n), 2)
        key = (min(u, v), max(u, v))
        if key not in existing:
            existing.add(key)
            g.add_edge(u, v, rng.randint(1, max_weight))
    return g
