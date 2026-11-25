import unittest

from src.algorithms import NegativeCycleError, bellman_ford, dijkstra, reconstruct_path
from src.graph import Graph, generate_city_graph


class TestShortestPaths(unittest.TestCase):
    def setUp(self):
        g = Graph()
        for u, v, w in [("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 5), ("C", "D", 8)]:
            g.add_edge(u, v, w)
        self.g = g

    def test_known_distances(self):
        for algo in (dijkstra, bellman_ford):
            dist, prev = algo(self.g, "A")
            self.assertEqual(dist["B"], 3)
            self.assertEqual(dist["D"], 8)
            self.assertEqual(reconstruct_path(prev, "A", "D"), ["A", "C", "B", "D"])

    def test_algorithms_agree_on_random_graphs(self):
        for seed in range(5):
            g = generate_city_graph(150, seed=seed)
            self.assertEqual(dijkstra(g, 0)[0], bellman_ford(g, 0)[0])

    def test_unreachable(self):
        g = Graph()
        g.add_vertex("X")
        g.add_edge("A", "B", 1)
        dist, prev = dijkstra(g, "A")
        self.assertEqual(dist["X"], float("inf"))
        self.assertEqual(reconstruct_path(prev, "A", "X"), [])

    def test_negative_edge_and_cycle(self):
        g = Graph(directed=True)
        g.add_edge("A", "B", 4)
        g.add_edge("A", "C", 5)
        g.add_edge("C", "B", -3)
        self.assertEqual(bellman_ford(g, "A")[0]["B"], 2)
        with self.assertRaises(ValueError):
            dijkstra(g, "A")
        g.add_edge("B", "C", 1)  # B->C->B = -2 : negative cycle
        with self.assertRaises(NegativeCycleError):
            bellman_ford(g, "A")


if __name__ == "__main__":
    unittest.main()
