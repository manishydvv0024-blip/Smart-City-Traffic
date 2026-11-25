# Smart City Route Optimization System

Finds the shortest route between locations in a city. Locations are **vertices**, roads are
**weighted edges** (distance in km). Implements **Dijkstra** and **Bellman-Ford** from scratch and
compares their performance on graphs of increasing size.

## Project structure
```
smart-city-route-optimizer/
├── main.py                 # CLI (route / benchmark / locations)
├── src/
│   ├── graph.py            # Graph class + random city generator
│   ├── algorithms.py       # Dijkstra, Bellman-Ford, path reconstruction
│   └── benchmark.py        # timing, CSV + plot output
├── tests/test_algorithms.py
├── results/                # benchmark.csv, benchmark.png
└── requirements.txt        # matplotlib (optional, plot only)
```

## Usage
```bash
python main.py locations                      # list demo locations
python main.py route Airport Harbor           # shortest route with both algorithms
python main.py benchmark                      # compare on random graphs
python main.py benchmark --sizes 100 500 1000
python -m unittest discover -v                # run tests
```
Example output:
```
[Dijkstra]     Airport -> Central Station -> Old Town -> Harbor  |  21 km
[Bellman-Ford] Airport -> Central Station -> Old Town -> Harbor  |  21 km
```

## Algorithms & complexity
| | Dijkstra (binary heap) | Bellman-Ford |
|---|---|---|
| Time | O((V + E) log V) | O(V · E) worst case |
| Space | O(V + E) | O(V + E) |
| Negative weights | No | Yes |
| Negative cycle detection | No | Yes |
| Best for | Road networks (weights ≥ 0) | Graphs with negative costs, e.g. toll rebates/incentives |

Bellman-Ford here stops early when a full pass makes no changes, so it is faster than its worst
case on typical graphs but is still slower than Dijkstra.

## Benchmark results
Random connected graphs, average degree 4, weights 1-100, best of 3 runs
(numbers vary by machine; see `results/benchmark.csv` and `results/benchmark.png`):

| Locations (V) | Roads (E) | Dijkstra (ms) | Bellman-Ford (ms) | Speedup |
|---:|---:|---:|---:|---:|
| 50 | 100 | 0.037 | 0.079 | 2.2x |
| 100 | 200 | 0.074 | 0.247 | 3.3x |
| 200 | 400 | 0.148 | 0.527 | 3.6x |
| 500 | 1000 | 0.497 | 1.965 | 4.0x |
| 1000 | 2000 | 1.033 | 3.290 | 3.2x |
| 2000 | 4000 | 2.329 | 8.640 | 3.7x |

**Conclusion:** both give identical distances (verified by tests), but Dijkstra is consistently
~3-4x faster on non-negative road networks, and the gap widens on denser graphs. Use Bellman-Ford
only when negative weights must be supported.

## Push to GitHub / upload to zosima.ai
```bash
git init && git add . && git commit -m "Smart City Route Optimization System"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
