"""
Distance-Vector Algorithm — From-Scratch Implementation
EC 441 Lecture 16: Distance Vector, Bellman-Ford, and BGP Introduction

Implements the distributed distance-vector algorithm following the pseudocode
from lecture. Uses the 5-node worked example from the slides. Includes:

1. DV convergence trace (round by round, matching the slides)
2. Forwarding table derivation
3. Link failure → count-to-infinity demonstration
4. Split horizon and poisoned reverse comparison

No external dependencies — uses only the Python standard library.

Usage:
    python -u demo_bellmanford_l16.py
"""


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class DVNode:
    """A node running the distance-vector algorithm."""

    def __init__(self, name):
        self.name = name
        self.dv = {}        # destination -> estimated cost
        self.next_hop = {}  # destination -> next hop node name
        self.neighbors = {} # neighbor name -> link cost

    def __repr__(self):
        entries = []
        for dest in sorted(self.dv):
            cost = self.dv[dest]
            c_str = "inf" if cost == float("inf") else str(int(cost))
            entries.append(f"{dest}={c_str}")
        return f"{self.name}: [{', '.join(entries)}]"


class DVNetwork:
    """A network of nodes running the distance-vector algorithm."""

    def __init__(self, edges):
        """Build network from a list of (src, dst, cost) tuples."""
        self.nodes = {}  # name -> DVNode
        self.edges = list(edges)

        # Collect all node names
        names = set()
        for src, dst, _ in edges:
            names.add(src)
            names.add(dst)
        self.all_names = sorted(names)

        # Create nodes
        for name in self.all_names:
            self.nodes[name] = DVNode(name)

        # Add neighbor relationships (undirected)
        for src, dst, cost in edges:
            self.nodes[src].neighbors[dst] = cost
            self.nodes[dst].neighbors[src] = cost

        # Initialize distance vectors
        for name in self.all_names:
            node = self.nodes[name]
            for dest in self.all_names:
                if dest == name:
                    node.dv[dest] = 0
                    node.next_hop[dest] = name
                elif dest in node.neighbors:
                    node.dv[dest] = node.neighbors[dest]
                    node.next_hop[dest] = dest
                else:
                    node.dv[dest] = float("inf")
                    node.next_hop[dest] = None


# ---------------------------------------------------------------------------
# Algorithm
# ---------------------------------------------------------------------------

def dv_round(network):
    """
    Run one round of DV updates. All nodes simultaneously process their
    neighbors' distance vectors from the previous round.

    Returns True if any distance vector changed, False if converged.
    """
    changed = False
    # Snapshot current DVs (nodes read from previous round, not current)
    old_dvs = {name: dict(node.dv) for name, node in network.nodes.items()}

    for name in network.all_names:
        node = network.nodes[name]
        for dest in network.all_names:
            if dest == name:
                continue
            for neighbor, link_cost in node.neighbors.items():
                new_cost = link_cost + old_dvs[neighbor][dest]
                if new_cost < node.dv[dest]:
                    node.dv[dest] = new_cost
                    node.next_hop[dest] = neighbor
                    changed = True

    return changed


def dv_round_split_horizon(network):
    """DV round with split horizon: don't advertise a route back to the
    neighbor you learned it from."""
    changed = False
    old_dvs = {name: dict(node.dv) for name, node in network.nodes.items()}
    old_nhs = {name: dict(node.next_hop) for name, node in network.nodes.items()}

    for name in network.all_names:
        node = network.nodes[name]
        for dest in network.all_names:
            if dest == name:
                continue
            for neighbor, link_cost in node.neighbors.items():
                # Split horizon: if neighbor routes to dest via us, it
                # advertises infinity. Equivalently, we ignore neighbor's
                # route to dest if neighbor's next hop for dest is us.
                if old_nhs[neighbor].get(dest) == name:
                    advertised_cost = float("inf")
                else:
                    advertised_cost = old_dvs[neighbor][dest]
                new_cost = link_cost + advertised_cost
                if new_cost < node.dv[dest]:
                    node.dv[dest] = new_cost
                    node.next_hop[dest] = neighbor
                    changed = True

    return changed


def dv_round_poisoned_reverse(network):
    """DV round with poisoned reverse: actively advertise infinity for routes
    learned from that neighbor."""
    changed = False
    old_dvs = {name: dict(node.dv) for name, node in network.nodes.items()}
    old_nhs = {name: dict(node.next_hop) for name, node in network.nodes.items()}

    for name in network.all_names:
        node = network.nodes[name]
        for dest in network.all_names:
            if dest == name:
                continue
            for neighbor, link_cost in node.neighbors.items():
                # Poisoned reverse: neighbor advertises infinity if its
                # next hop for dest is us
                if old_nhs[neighbor].get(dest) == name:
                    advertised_cost = float("inf")
                else:
                    advertised_cost = old_dvs[neighbor][dest]
                new_cost = link_cost + advertised_cost
                if new_cost < node.dv[dest]:
                    node.dv[dest] = new_cost
                    node.next_hop[dest] = neighbor
                    changed = True

    return changed


def run_dv(network, max_rounds=50, trace=True, update_fn=dv_round):
    """Run the DV algorithm to convergence with optional trace output."""
    if trace:
        print_dv_table(network, "Round 0 (Initialization)")

    for r in range(1, max_rounds + 1):
        changed = update_fn(network)

        if trace:
            print_dv_table(network, f"Round {r}")

        if not changed:
            if trace:
                print(f"  → Converged! No changes in round {r}.\n")
            return r

    if trace:
        print(f"  → Did not converge after {max_rounds} rounds.\n")
    return max_rounds


def print_dv_table(network, label, prev_dvs=None):
    """Print all nodes' distance vectors as a table."""
    names = network.all_names
    col_width = 6

    print(f"\n{label}:")
    # Header
    header = f"  {'Node':<6}"
    for dest in names:
        header += f" {dest:>{col_width}}"
    print(header)
    print("  " + "─" * (6 + (col_width + 1) * len(names)))

    # Rows
    for name in names:
        node = network.nodes[name]
        row = f"  {name:<6}"
        for dest in names:
            cost = node.dv[dest]
            if cost == float("inf"):
                row += f" {'inf':>{col_width}}"
            else:
                row += f" {int(cost):>{col_width}}"
        print(row)


def print_forwarding_table(network, source):
    """Print the forwarding table for a given source node."""
    node = network.nodes[source]
    names = network.all_names

    print(f"\nForwarding table for router {source}:")
    print(f"  {'Destination':<14} {'Next Hop':<10} {'Cost':<6} {'Path'}")
    print("  " + "─" * 55)

    for dest in names:
        if dest == source:
            continue
        cost = node.dv[dest]
        nh = node.next_hop[dest]
        cost_str = "inf" if cost == float("inf") else str(int(cost))
        nh_str = nh if nh else "—"

        # Reconstruct path by following next hops
        path = [source]
        current = source
        visited = {source}
        while current != dest:
            nxt = network.nodes[current].next_hop.get(dest)
            if nxt is None or nxt in visited:
                path.append("...")
                break
            path.append(nxt)
            visited.add(nxt)
            current = nxt

        path_str = " → ".join(path)
        print(f"  {dest:<14} {nh_str:<10} {cost_str:<6} {path_str}")


# ---------------------------------------------------------------------------
# Demo 1: Lecture example — DV convergence
# ---------------------------------------------------------------------------

def lecture_example():
    """Run DV on the 5-node network from the L16 slides."""

    print("=" * 60)
    print("Distance-Vector Algorithm — Lecture 16 Worked Example")
    print("=" * 60)

    edges = [
        ("A", "B", 1),
        ("A", "C", 4),
        ("B", "C", 2),
        ("B", "D", 3),
        ("C", "E", 1),
        ("D", "E", 5),
    ]

    print("\nNetwork edges:")
    for src, dst, cost in edges:
        print(f"  {src} — {dst} : cost {cost}")

    network = DVNetwork(edges)

    print("\nRunning DV algorithm (all nodes simultaneously):\n")
    run_dv(network, trace=True)

    # Show forwarding tables for all nodes
    for name in network.all_names:
        print_forwarding_table(network, name)

    return edges


# ---------------------------------------------------------------------------
# Demo 2: Count-to-infinity
# ---------------------------------------------------------------------------

def count_to_infinity_demo():
    """Demonstrate count-to-infinity on a 3-node chain.

    This uses a manual simulation because count-to-infinity requires
    route *invalidation* (not just relaxation) when a link fails —
    a detail that the general DV round function doesn't capture.
    """

    print("\n" + "=" * 60)
    print("Count-to-Infinity Demonstration")
    print("=" * 60)

    print("\nTopology: A —1— B —1— C")
    print("After convergence, the B-C link fails.")
    print("Watch A and B count toward infinity (RIP max = 16).\n")

    rip_infinity = 16

    # Initial converged state
    d_a = 2   # d_A(C) = 2 via B
    d_b = 1   # d_B(C) = 1 direct

    print("Initial converged state:")
    print(f"  d_A(C) = {d_a} via B")
    print(f"  d_B(C) = {d_b} via C (direct)")

    print("\n--- B-C link fails! ---\n")

    # After failure: B loses its direct link to C.
    # B must recompute d_B(C) using only neighbor A's advertisement.
    # But A's d_A(C) = 2 goes *through B* — circular dependency.

    print(f"{'Round':<8} {'d_A(C)':<12} {'d_B(C)':<12} {'Notes'}")
    print("─" * 55)
    print(f"{'0':<8} {'2':<12} {'1':<12} {'Before failure'}")

    for r in range(1, rip_infinity + 5):
        # B lost direct link. B's only neighbor is A.
        # B computes: d_B(C) = c(B,A) + d_A(C) = 1 + d_A(C)
        new_d_b = 1 + d_a

        # A's only neighbor (toward C) is B.
        # A computes: d_A(C) = c(A,B) + d_B(C) = 1 + new_d_B
        new_d_a = 1 + new_d_b

        # Cap at RIP infinity
        if new_d_b >= rip_infinity:
            new_d_b = rip_infinity
        if new_d_a >= rip_infinity:
            new_d_a = rip_infinity

        d_a = new_d_a
        d_b = new_d_b

        da_str = str(d_a) if d_a < rip_infinity else f"{rip_infinity} (inf)"
        db_str = str(d_b) if d_b < rip_infinity else f"{rip_infinity} (inf)"

        note = ""
        if r == 1:
            note = "B uses A's stale route (goes through B!)"
        elif d_a >= rip_infinity and d_b >= rip_infinity:
            note = "Converged (both = infinity)"

        print(f"{r:<8} {da_str:<12} {db_str:<12} {note}")

        if d_a >= rip_infinity and d_b >= rip_infinity:
            break

    time_sec = r * 30
    print(f"\nCount-to-infinity took {r} rounds.")
    print(f"At RIP's 30-second interval: {time_sec} seconds "
          f"({time_sec // 60} min {time_sec % 60} sec) of routing loops.")


# ---------------------------------------------------------------------------
# Demo 3: Split horizon and poisoned reverse comparison
# ---------------------------------------------------------------------------

def split_horizon_demo():
    """Compare no fix, split horizon, and poisoned reverse.

    Uses manual simulation (same as count-to-infinity demo) to correctly
    model route invalidation after a link failure.
    """

    print("\n" + "=" * 60)
    print("Split Horizon / Poisoned Reverse Comparison")
    print("=" * 60)

    print("\nTopology: A —1— B —1— C (B-C then fails)")
    print("Comparing convergence behavior with different fixes:\n")

    rip_infinity = 16

    for method in ["No fix", "Split horizon", "Poisoned reverse"]:
        print(f"\n--- {method} ---")

        # Initial converged state
        d_a = 2  # d_A(C) via B
        d_b = 1  # d_B(C) direct

        # A routes to C via B; B routes to C directly.
        # After B-C fails, simulate:

        for r in range(1, rip_infinity + 5):
            # What does A advertise to B about C?
            if method == "No fix":
                a_tells_b = d_a  # A tells B its real d_A(C)
            else:
                # Split horizon or poisoned reverse: A routes to C via B,
                # so A tells B that d_A(C) = infinity
                a_tells_b = rip_infinity

            # B lost direct link. Uses A's advertisement.
            new_d_b = min(1 + a_tells_b, rip_infinity)

            # B always advertises to A (B doesn't route to C via A initially)
            b_tells_a = new_d_b

            # A uses B's advertisement
            new_d_a = min(1 + b_tells_a, rip_infinity)

            d_a = new_d_a
            d_b = new_d_b

            if d_a >= rip_infinity and d_b >= rip_infinity:
                break

        da_str = str(d_a) if d_a < rip_infinity else "inf"
        db_str = str(d_b) if d_b < rip_infinity else "inf"

        print(f"  Rounds to converge: {r}")
        print(f"  Final: d_A(C) = {da_str}, d_B(C) = {db_str}")

        if r <= 2:
            print("  -> Fast convergence — fix works for this 2-node loop.")
        else:
            print(f"  -> Slow convergence — counted to infinity over {r} rounds.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    lecture_example()
    count_to_infinity_demo()
    split_horizon_demo()
