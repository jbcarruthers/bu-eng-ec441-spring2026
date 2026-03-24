"""
Dijkstra's Algorithm — From-Scratch Implementation
EC 441 Lecture 15: Link-State Routing

Implements Dijkstra's shortest-path algorithm following the CLRS-style
pseudocode from lecture. Uses the 6-node worked example from the slides.

No external dependencies — uses only the Python standard library.

Usage:
    python -u demo_dijkstra_l15.py
"""


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Vertex:
    """A graph vertex with Dijkstra bookkeeping: distance d and predecessor pi."""

    def __init__(self, name):
        self.name = name
        self.d = float("inf")   # best-known cost from source
        self.pi = None          # predecessor on best-known path

    def __repr__(self):
        pi_name = self.pi if self.pi is None else self.pi
        return f"{self.name}: d={self.d}, pi={pi_name}"


class Graph:
    """Weighted undirected graph stored as an adjacency list."""

    def __init__(self, edges):
        """Build graph from a list of (src, dst, cost) tuples."""
        self.V = {}      # name -> Vertex
        self.Adj = {}    # name -> [neighbor names]
        self.w = {}      # (name, name) -> cost

        # Collect all vertex names
        nodes = set()
        for src, dst, _ in edges:
            nodes.add(src)
            nodes.add(dst)

        for name in sorted(nodes):
            self.V[name] = Vertex(name)
            self.Adj[name] = []

        # Undirected: add both directions
        for src, dst, cost in edges:
            self.Adj[src].append(dst)
            self.Adj[dst].append(src)
            self.w[(src, dst)] = cost
            self.w[(dst, src)] = cost

    def initialize_source(self, source):
        """Reset all distances to inf and source distance to 0."""
        for v in self.V.values():
            v.d = float("inf")
            v.pi = None
        self.V[source].d = 0


# ---------------------------------------------------------------------------
# Algorithm
# ---------------------------------------------------------------------------

def relax(u, v, G):
    """If the path through u improves the best-known cost to v, update v."""
    if G.V[v].d > G.V[u].d + G.w[(u, v)]:
        G.V[v].d = G.V[u].d + G.w[(u, v)]
        G.V[v].pi = u


def dijkstra(G, source, trace=False):
    """
    Run Dijkstra's algorithm from source.
    If trace=True, print the state table after each step (matching the slides).
    """
    G.initialize_source(source)
    Q = set(G.V.keys())   # un-finalized nodes
    N_prime = set()        # finalized nodes (N' in the slides)

    # Header for trace output
    non_source = sorted(v for v in G.V if v != source)
    if trace:
        header = f"{'Step':<6} {'N (finalized)':<22}"
        for v in non_source:
            header += f" {'D('+v+'),p('+v+')':<14}"
        header += f"  {'Select':<6}"
        print(header)
        print("─" * len(header))

    step = 0
    while Q:
        # Select un-finalized node with minimum D
        u = min(Q, key=lambda x: G.V[x].d)
        Q.remove(u)
        N_prime.add(u)

        # Relax all neighbors of u that are still in Q
        for v in G.Adj[u]:
            if v in Q:
                relax(u, v, G)

        # Print trace row
        if trace:
            label = "Init" if step == 0 else str(step)
            n_str = "{" + ",".join(sorted(N_prime)) + "}"
            row = f"{label:<6} {n_str:<22}"
            for v in non_source:
                d = G.V[v].d
                p = G.V[v].pi
                d_str = "∞" if d == float("inf") else str(int(d))
                p_str = "-" if p is None else p
                if v in N_prime and v != u:
                    row += f" {'—':<14}"
                else:
                    row += f" {d_str+','+p_str:<14}"
            selected = u if step > 0 or u == source else "—"
            row += f"  {selected:<6}"
            print(row)

        step += 1


def get_path(G, source, dest):
    """Reconstruct the shortest path from source to dest using predecessor pointers."""
    if source == dest:
        return [source]
    if G.V[dest].pi is None:
        return None  # no path
    path = get_path(G, source, G.V[dest].pi)
    if path is None:
        return None
    return path + [dest]


def forwarding_table(G, source):
    """Derive a forwarding table from the shortest-path tree."""
    print(f"\nForwarding table for router {source}:")
    print(f"{'Destination':<14} {'Next Hop':<10} {'Cost':<6} {'Path'}")
    print("─" * 55)
    for dest in sorted(G.V.keys()):
        if dest == source:
            continue
        path = get_path(G, source, dest)
        if path and len(path) >= 2:
            next_hop = path[1]
            cost = int(G.V[dest].d)
            path_str = " → ".join(path)
            print(f"{dest:<14} {next_hop:<10} {cost:<6} {path_str}")


# ---------------------------------------------------------------------------
# Worked example from Lecture 15 slides
# ---------------------------------------------------------------------------

def lecture_example():
    """Run Dijkstra on the 6-node network from the L15 slides."""

    print("=" * 60)
    print("Dijkstra's Algorithm — Lecture 15 Worked Example")
    print("=" * 60)

    # The 6-node graph from the slides
    edges = [
        ("u", "v", 2),
        ("u", "w", 1),
        ("u", "x", 5),
        ("v", "y", 3),
        ("w", "y", 3),
        ("w", "z", 2),
        ("x", "z", 1),
        ("y", "z", 4),
    ]

    print("\nNetwork edges:")
    for src, dst, cost in edges:
        print(f"  {src} — {dst} : cost {cost}")

    G = Graph(edges)
    source = "u"

    # Run with step-by-step trace
    print(f"\nRunning Dijkstra from source '{source}':\n")
    dijkstra(G, source, trace=True)

    # Show shortest paths
    print(f"\nShortest paths from {source}:")
    for dest in sorted(G.V.keys()):
        if dest == source:
            continue
        path = get_path(G, source, dest)
        cost = int(G.V[dest].d)
        print(f"  {source} → {dest}: cost {cost}, path {' → '.join(path)}")

    # Derive forwarding table
    forwarding_table(G, source)

    return G, edges


def link_failure_demo(edges):
    """Show what happens when a link fails — the routing recomputes."""

    print("\n" + "=" * 60)
    print("Link Failure Simulation: w—z cost increases to 100")
    print("=" * 60)

    # Modify w-z cost
    modified = []
    for src, dst, cost in edges:
        if (src, dst) in [("w", "z"), ("z", "w")]:
            modified.append((src, dst, 100))
        else:
            modified.append((src, dst, cost))

    G2 = Graph(modified)
    source = "u"

    dijkstra(G2, source, trace=True)

    print(f"\nNew shortest paths from {source}:")
    for dest in sorted(G2.V.keys()):
        if dest == source:
            continue
        path = get_path(G2, source, dest)
        cost = int(G2.V[dest].d)
        print(f"  {source} → {dest}: cost {cost}, path {' → '.join(path)}")

    forwarding_table(G2, source)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    G, edges = lecture_example()
    link_failure_demo(edges)
