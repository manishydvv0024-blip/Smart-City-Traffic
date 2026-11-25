"""Compare Dijkstra and Bellman-Ford across graph sizes."""
import csv
import time

from .algorithms import bellman_ford, dijkstra
from .graph import generate_city_graph


def _time(fn, graph, source, repeats):
    best = float("inf")
    for _ in range(repeats):
        t = time.perf_counter()
        fn(graph, source)
        best = min(best, time.perf_counter() - t)
    return best * 1000  # ms


def run_benchmark(sizes=(50, 100, 200, 500, 1000, 2000), repeats=3, csv_path=None, plot_path=None):
    rows = []
    print(f"{'V':>6} {'E':>7} {'Dijkstra (ms)':>15} {'Bellman-Ford (ms)':>19} {'Speedup':>9}")
    for n in sizes:
        g = generate_city_graph(n)
        d = _time(dijkstra, g, 0, repeats)
        b = _time(bellman_ford, g, 0, repeats)
        rows.append((n, g.num_edges // 2, d, b))
        print(f"{n:>6} {g.num_edges // 2:>7} {d:>15.3f} {b:>19.3f} {b / d:>8.1f}x")
    if csv_path:
        with open(csv_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["vertices", "roads", "dijkstra_ms", "bellman_ford_ms"])
            w.writerows(rows)
    if plot_path:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            xs = [r[0] for r in rows]
            plt.figure(figsize=(7, 4.5))
            plt.plot(xs, [r[2] for r in rows], "o-", label="Dijkstra")
            plt.plot(xs, [r[3] for r in rows], "s-", label="Bellman-Ford")
            plt.xlabel("Number of locations (V)")
            plt.ylabel("Time (ms)")
            plt.title("Dijkstra vs Bellman-Ford")
            plt.legend()
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.savefig(plot_path, dpi=150)
        except ImportError:
            print("matplotlib not installed; skipping plot.")
    return rows
