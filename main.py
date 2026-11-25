"""Smart City Route Optimization System - command line interface."""
import argparse

from src.algorithms import bellman_ford, dijkstra, reconstruct_path
from src.benchmark import run_benchmark
from src.graph import Graph

CITY_ROADS = [  # (from, to, distance in km)
    ("Airport", "Central Station", 12), ("Airport", "Tech Park", 9),
    ("Central Station", "City Mall", 3), ("Central Station", "Hospital", 5),
    ("Central Station", "Old Town", 4), ("Tech Park", "University", 6),
    ("Tech Park", "Stadium", 8), ("University", "Hospital", 4),
    ("University", "Stadium", 3), ("City Mall", "Old Town", 2),
    ("City Mall", "Harbor", 7), ("Hospital", "Harbor", 6),
    ("Old Town", "Harbor", 5), ("Stadium", "Harbor", 10),
]


def build_city():
    g = Graph()
    for u, v, w in CITY_ROADS:
        g.add_edge(u, v, w)
    return g


def route(args):
    g = build_city()
    for name in (args.source, args.destination):
        if name not in g.adj:
            raise SystemExit(f"Unknown location '{name}'. Choose from: {', '.join(sorted(g.adj))}")
    for label, algo in (("Dijkstra", dijkstra), ("Bellman-Ford", bellman_ford)):
        dist, prev = algo(g, args.source)
        path = reconstruct_path(prev, args.source, args.destination)
        print(f"[{label}] {' -> '.join(path)}  |  {dist[args.destination]} km")


def main():
    p = argparse.ArgumentParser(description="Smart City Route Optimization System")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("route", help="shortest route in the demo city")
    r.add_argument("source")
    r.add_argument("destination")
    r.set_defaults(func=route)
    b = sub.add_parser("benchmark", help="compare algorithms on random graphs")
    b.add_argument("--sizes", type=int, nargs="+", default=[50, 100, 200, 500, 1000, 2000])
    b.set_defaults(func=lambda a: run_benchmark(
        sizes=a.sizes, csv_path="results/benchmark.csv", plot_path="results/benchmark.png"))
    sub.add_parser("locations", help="list demo locations").set_defaults(
        func=lambda a: print("\n".join(sorted(build_city().adj))))
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
