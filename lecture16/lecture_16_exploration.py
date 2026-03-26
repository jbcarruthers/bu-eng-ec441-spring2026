import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, nx, plt


@app.cell
def _(mo):
    mo.md("""
    # Lecture 16: Distance Vector, Bellman-Ford, and BGP — Interactive Exploration

    **EC 441 - Introduction to Computer Networking**
    Boston University, Spring 2026

    This notebook has five interactive parts:

    1. **Network Graph Builder** — define edges and weights, visualize the network
    2. **DV Algorithm Step-by-Step** — watch distance vectors converge round by round
    3. **Count-to-Infinity Simulator** — see how link failures cause slow convergence
    4. **Split Horizon / Poisoned Reverse** — compare fixes for count-to-infinity
    5. **LS vs. DV Comparison** — side-by-side Dijkstra and Bellman-Ford on the same graph
    """)
    return


# ============================================================
# Part 1: Network Graph Builder
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 1: Network Graph Builder

    Define a network as a weighted graph. Enter edges as `node1-node2:cost`, one per line.
    The default is the 5-node example from the lecture slides.
    """)
    return


@app.cell
def _(mo):
    edge_input = mo.ui.text_area(
        value="A-B:1\nA-C:4\nB-C:2\nB-D:3\nC-E:1\nD-E:5",
        label="Network edges (node1-node2:cost):",
        rows=8,
    )
    edge_input
    return (edge_input,)


@app.cell
def _(edge_input, nx):
    def parse_edges(text):
        """Parse edge definitions into a list of (src, dst, cost) tuples."""
        edges = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                nodes_part, cost_str = line.split(":")
                n1, n2 = nodes_part.split("-")
                edges.append((n1.strip(), n2.strip(), float(cost_str.strip())))
            except (ValueError, IndexError):
                continue
        return edges

    def build_graph(edges):
        """Build a networkx graph from edge tuples."""
        _G = nx.Graph()
        for src, dst, cost in edges:
            _G.add_edge(src, dst, weight=cost)
        return _G

    parsed_edges = parse_edges(edge_input.value)
    G = build_graph(parsed_edges)
    return G, build_graph, parse_edges, parsed_edges


@app.cell
def _(G, mo, nx, plt):
    fig1, ax1 = plt.subplots(1, 1, figsize=(8, 6))
    if len(G.nodes()) > 0:
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=ax1, with_labels=True, node_color="lightblue",
                node_size=800, font_size=14, font_weight="bold",
                edge_color="gray", width=2)
        _edge_labels = nx.get_edge_attributes(G, "weight")
        _edge_labels_int = {k: int(v) if v == int(v) else v for k, v in _edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, _edge_labels_int, font_size=12, ax=ax1)
        ax1.set_title("Network Graph", fontsize=14)
    else:
        ax1.text(0.5, 0.5, "No valid edges defined", ha="center", va="center", fontsize=14)
    plt.tight_layout()

    adj_rows = []
    for _node in sorted(G.nodes()):
        _neighbors = sorted(G.neighbors(_node))
        _neighbor_strs = [f"{n} (cost {int(G[_node][n]['weight'])})" for n in _neighbors]
        adj_rows.append(f"| {_node} | {len(_neighbors)} | {', '.join(_neighbor_strs)} |")

    adj_table = "| Node | Degree | Neighbors |\n| --- | --- | --- |\n" + "\n".join(adj_rows)

    mo.vstack([fig1, mo.md(f"**Adjacency list** ({len(G.nodes())} nodes, {len(G.edges())} edges):\n\n{adj_table}")])
    return ax1, fig1, pos


# ============================================================
# Part 2: DV Algorithm Step-by-Step
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 2: Distance-Vector Algorithm Step-by-Step

    Watch the DV algorithm converge round by round. Each node starts knowing only its
    direct links, then iteratively exchanges distance vectors with neighbors until
    no table changes — matching the convergence trace from the slides.
    """)
    return


@app.cell
def _(G, mo):
    dv_source_dropdown = mo.ui.dropdown(
        options=sorted(G.nodes()),
        value=sorted(G.nodes())[0] if G.nodes() else "A",
        label="View forwarding table for:",
    )
    dv_source_dropdown
    return (dv_source_dropdown,)


@app.cell
def _(G, dv_source_dropdown, mo):
    def run_dv(graph):
        """Run DV algorithm, recording distance vectors after each round."""
        nodes = sorted(graph.nodes())
        n = len(nodes)

        # Initialize distance vectors: each node knows only direct links
        dv = {}
        next_hop = {}
        for x in nodes:
            dv[x] = {}
            next_hop[x] = {}
            for y in nodes:
                if x == y:
                    dv[x][y] = 0.0
                    next_hop[x][y] = x
                elif graph.has_edge(x, y):
                    dv[x][y] = graph[x][y]["weight"]
                    next_hop[x][y] = y
                else:
                    dv[x][y] = float("inf")
                    next_hop[x][y] = None

        # Record round 0
        history = []
        history.append({x: dict(dv[x]) for x in nodes})

        # Iterate until convergence
        for _round in range(n):
            changed = False
            new_dv = {x: dict(dv[x]) for x in nodes}
            new_nh = {x: dict(next_hop[x]) for x in nodes}

            for x in nodes:
                for y in nodes:
                    if x == y:
                        continue
                    for v in graph.neighbors(x):
                        new_cost = graph[x][v]["weight"] + dv[v][y]
                        if new_cost < new_dv[x][y]:
                            new_dv[x][y] = new_cost
                            new_nh[x][y] = v
                            changed = True

            dv = new_dv
            next_hop = new_nh
            history.append({x: dict(dv[x]) for x in nodes})

            if not changed:
                break

        return history, dv, next_hop, nodes

    history, final_dv, final_nh, nodes = run_dv(G)

    # Build round-by-round tables
    round_tables = []
    for r_idx, snapshot in enumerate(history):
        prev = history[r_idx - 1] if r_idx > 0 else None
        header = "| Node | " + " | ".join(nodes) + " |"
        sep = "| --- " * (len(nodes) + 1) + "|"
        rows = []
        for x in nodes:
            cells = [f"**{x}**"]
            for y in nodes:
                val = snapshot[x][y]
                val_str = "inf" if val == float("inf") else str(int(val))
                if prev is not None and snapshot[x][y] != prev[x][y]:
                    val_str = f"**{val_str}**"
                cells.append(val_str)
            rows.append("| " + " | ".join(cells) + " |")
        label = "Initialization" if r_idx == 0 else f"Round {r_idx}"
        if r_idx == len(history) - 1 and r_idx > 0:
            label += " (converged)"
        round_tables.append(f"### {label}\n\n{header}\n{sep}\n" + "\n".join(rows))

    # Forwarding table for selected source
    src = dv_source_dropdown.value
    fwd_header = "| Destination | Next Hop | Cost | Path |"
    fwd_sep = "| --- | --- | --- | --- |"
    fwd_rows = []
    for _dest in nodes:
        if _dest == src:
            continue
        cost = final_dv[src][_dest]
        nh = final_nh[src][_dest]
        cost_str = "inf" if cost == float("inf") else str(int(cost))

        # Reconstruct path
        _path = [src]
        _current = src
        _visited = {src}
        while _current != _dest and final_nh[_current][_dest] is not None:
            _nxt = final_nh[_current][_dest]
            if _nxt in _visited:
                _path.append("...")
                break
            _path.append(_nxt)
            _visited.add(_nxt)
            _current = _nxt

        path_str = " -> ".join(_path)
        nh_str = nh if nh else "—"
        fwd_rows.append(f"| {_dest} | {nh_str} | {cost_str} | {path_str} |")

    fwd_table = f"{fwd_header}\n{fwd_sep}\n" + "\n".join(fwd_rows)

    converge_msg = f"Converged in **{len(history) - 1} round(s)** (max possible: {len(nodes) - 1})."

    sections = [mo.md(converge_msg)]
    for rt in round_tables:
        sections.append(mo.md(rt))
    sections.append(mo.md(f"### Forwarding table for node **{src}**\n\n{fwd_table}"))

    mo.vstack(sections)
    return final_dv, final_nh, history, nodes, run_dv


# ============================================================
# Part 3: Count-to-Infinity Simulator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 3: Count-to-Infinity Simulator

    A simple 3-node chain: A — B — C. After convergence, the B-C link **fails**.
    Watch how A and B's costs to C increment toward infinity — the classic
    count-to-infinity problem.

    Use the slider to set the "infinity" value (RIP uses 16).
    """)
    return


@app.cell
def _(mo):
    infinity_slider = mo.ui.slider(
        start=4, stop=32, step=1, value=16,
        label="Infinity value (RIP = 16):",
    )
    infinity_slider
    return (infinity_slider,)


@app.cell
def _(infinity_slider, mo, plt):
    inf_val = infinity_slider.value

    # Initial converged state: A--1--B--1--C
    # d_A(C) = 2, d_B(C) = 1
    d_a = [2]
    d_b = [1]

    # B-C link fails. Simulate round by round (no split horizon).
    # B sees A's d_A(C) and computes c(B,A) + d_A(C) = 1 + d_A(C)
    # A sees B's d_B(C) and computes c(A,B) + d_B(C) = 1 + d_B(C)
    curr_a = 2
    curr_b = 1

    for _ in range(100):
        # B updates: can't reach C directly (failed), uses A
        _new_b = min(1 + curr_a, inf_val)
        # A updates: uses B (its only neighbor toward C)
        _new_a = min(1 + _new_b, inf_val)

        d_b.append(_new_b)
        d_a.append(_new_a)

        if _new_a >= inf_val and _new_b >= inf_val:
            break
        curr_a = _new_a
        curr_b = _new_b

    rounds = list(range(len(d_a)))

    # Build trace table (first 20 rounds + last few)
    trace_header = "| Round | d_A(C) | d_B(C) | Notes |"
    trace_sep = "| --- | --- | --- | --- |"
    trace_rows = []
    trace_rows.append(f"| 0 | 2 | 1 | Initial (converged, before failure) |")
    _show_rounds = list(range(1, min(len(rounds), 12)))
    if len(rounds) > 12:
        _show_rounds.append(-1)  # ellipsis marker
        _show_rounds.extend(range(len(rounds) - 3, len(rounds)))

    for _i in _show_rounds:
        if _i == -1:
            trace_rows.append("| ... | ... | ... | ... |")
            continue
        note = ""
        if _i == 1:
            note = "B-C fails; B thinks A can reach C"
        elif d_a[_i] >= inf_val and d_b[_i] >= inf_val:
            note = f"Both reach {inf_val} = infinity. Converged."
        a_str = str(int(d_a[_i])) if d_a[_i] < inf_val else f"**{inf_val}** (inf)"
        b_str = str(int(d_b[_i])) if d_b[_i] < inf_val else f"**{inf_val}** (inf)"
        trace_rows.append(f"| {_i} | {a_str} | {b_str} | {note} |")

    trace_table = f"{trace_header}\n{trace_sep}\n" + "\n".join(trace_rows)

    # Plot
    fig3, ax3 = plt.subplots(1, 1, figsize=(10, 4.5))
    ax3.plot(rounds, d_a, "b-o", markersize=3, label="d_A(C)", linewidth=1.5)
    ax3.plot(rounds, d_b, "r-s", markersize=3, label="d_B(C)", linewidth=1.5)
    ax3.axhline(y=inf_val, color="gray", linestyle="--", alpha=0.7, label=f"Infinity = {inf_val}")
    ax3.set_xlabel("Round", fontsize=12)
    ax3.set_ylabel("Estimated cost to C", fontsize=12)
    ax3.set_title(f"Count-to-Infinity (infinity = {inf_val})", fontsize=14)
    ax3.legend(fontsize=11)
    ax3.set_ylim(-0.5, inf_val + 2)
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()

    converge_rounds = len(d_a) - 1
    time_at_30s = converge_rounds * 30

    summary = (
        f"With infinity = {inf_val}, count-to-infinity takes **{converge_rounds} rounds** "
        f"to converge.\n\n"
        f"At RIP's 30-second update interval, that's **{time_at_30s} seconds** "
        f"({time_at_30s // 60} min {time_at_30s % 60} sec) of routing loops."
    )

    mo.vstack([mo.md(trace_table), fig3, mo.md(summary)])
    return converge_rounds, d_a, d_b, fig3, inf_val, rounds


# ============================================================
# Part 4: Split Horizon / Poisoned Reverse
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 4: Split Horizon and Poisoned Reverse

    Compare three approaches on the A — B — C chain after B-C fails:
    - **No fix**: basic DV (count-to-infinity)
    - **Split horizon**: don't advertise a route back to the neighbor you learned it from
    - **Poisoned reverse**: advertise infinity for routes learned from that neighbor
    """)
    return


@app.cell
def _(mo):
    fix_radio = mo.ui.radio(
        options=["No fix", "Split horizon", "Poisoned reverse"],
        value="No fix",
        label="Select DV variant:",
    )
    fix_radio
    return (fix_radio,)


@app.cell
def _(fix_radio, mo, plt):
    mode = fix_radio.value
    inf_val_fix = 16  # RIP infinity

    # A--1--B--1--C, B-C fails
    # A routes to C via B. B routes to C directly.
    # After failure:

    d_a_fix = [2]
    d_b_fix = [1]
    curr_a_f = 2
    curr_b_f = 1
    # A's next hop to C is B; B's next hop to C was direct (now failed)
    a_via = "B"  # A reaches C via B
    b_via = "direct"  # B reached C directly (now failed)

    for _r in range(50):
        # What does A advertise to B for C?
        if mode == "No fix":
            a_advertised_to_b = curr_a_f  # A tells B its real d_A(C)
        elif mode == "Split horizon":
            # A routes to C via B, so A does NOT advertise C to B
            a_advertised_to_b = float("inf")  # effectively hidden
        else:  # Poisoned reverse
            # A routes to C via B, so A tells B: d_A(C) = inf
            a_advertised_to_b = float("inf")

        # B updates: B-C is broken, so only option is via A
        _new_b = min(1 + a_advertised_to_b, inf_val_fix)
        if _new_b >= inf_val_fix:
            _new_b = inf_val_fix

        # What does B advertise to A for C?
        b_advertised_to_a = _new_b  # B always advertises to A (A is not B's route to C)

        # A updates
        _new_a = min(1 + b_advertised_to_a, inf_val_fix)
        if _new_a >= inf_val_fix:
            _new_a = inf_val_fix

        d_a_fix.append(_new_a)
        d_b_fix.append(_new_b)

        if _new_a >= inf_val_fix and _new_b >= inf_val_fix:
            break
        curr_a_f = _new_a
        curr_b_f = _new_b

    rounds_fix = list(range(len(d_a_fix)))

    fig4, ax4 = plt.subplots(1, 1, figsize=(10, 4.5))
    ax4.plot(rounds_fix, d_a_fix, "b-o", markersize=4, label="d_A(C)", linewidth=1.5)
    ax4.plot(rounds_fix, d_b_fix, "r-s", markersize=4, label="d_B(C)", linewidth=1.5)
    ax4.axhline(y=inf_val_fix, color="gray", linestyle="--", alpha=0.7, label="Infinity = 16")
    ax4.set_xlabel("Round", fontsize=12)
    ax4.set_ylabel("Estimated cost to C", fontsize=12)
    ax4.set_title(f"DV Convergence after B-C failure — {mode}", fontsize=14)
    ax4.legend(fontsize=11)
    ax4.set_ylim(-0.5, inf_val_fix + 2)
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()

    converge_fix = len(d_a_fix) - 1

    if mode == "No fix":
        explanation = (
            f"**No fix**: A and B count to infinity over **{converge_fix} rounds**. "
            "A tells B it can reach C (via B!), creating a circular dependency."
        )
    elif mode == "Split horizon":
        explanation = (
            f"**Split horizon**: A does not advertise its route to C back to B "
            "(since A reaches C via B). B correctly sets d_B(C) = inf in **1 round**. "
            "A then also sets d_A(C) = inf."
        )
    else:
        explanation = (
            f"**Poisoned reverse**: A actively tells B that d_A(C) = inf "
            "(since A reaches C via B). B correctly sets d_B(C) = inf in **1 round**. "
            "Stronger than silence — B gets an explicit signal."
        )

    mo.vstack([fig4, mo.md(explanation)])
    return converge_fix, fig4, mode


@app.cell
def _(mo):
    mo.md("""### Limitation: 3+ Node Loops

Split horizon and poisoned reverse fix **two-node loops** but fail for loops with 3+ nodes.
Consider this topology where the D-C link fails:

```
A ──1── B ──1── C
 \\               |
  2              1 (fails!)
   \\             |
    D ──────────┘
```

After D-C fails, A might route to C via B, B via A via D, D via A — a 3-node
loop that split horizon cannot detect because no single node is advertising
back to the neighbor it learned from.
""")
    return


# ============================================================
# Part 5: LS vs. DV Comparison
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 5: Link-State vs. Distance-Vector Comparison

    Side-by-side comparison on the same graph:
    - **Left**: Dijkstra (link-state) — computes all shortest paths in one shot
    - **Right**: DV (Bellman-Ford) — converges over multiple rounds

    Both produce the same forwarding table when they converge — the algorithms
    are different methods for solving the same problem.
    """)
    return


@app.cell
def _(G, mo):
    cmp_source = mo.ui.dropdown(
        options=sorted(G.nodes()),
        value=sorted(G.nodes())[0] if G.nodes() else "A",
        label="Source node for comparison:",
    )
    cmp_source
    return (cmp_source,)


@app.cell
def _(G, cmp_source, final_dv, final_nh, history, mo, nx, plt):
    src_cmp = cmp_source.value
    nodes_cmp = sorted(G.nodes())

    # --- Dijkstra (LS) ---
    lengths_ls, paths_ls = nx.single_source_dijkstra(G, src_cmp, weight="weight")

    # --- DV (already computed) ---
    # Use final_dv and final_nh from Part 2

    # Build comparison table
    cmp_header = "| Dest | Dijkstra Cost | Dijkstra Path | DV Cost | DV Next Hop | Match? |"
    cmp_sep = "| --- | --- | --- | --- | --- | --- |"
    cmp_rows = []
    all_match = True
    for dest in nodes_cmp:
        if dest == src_cmp:
            continue
        ls_cost = int(lengths_ls[dest])
        ls_path = " -> ".join(paths_ls[dest])
        dv_cost = final_dv[src_cmp][dest]
        dv_cost_str = "inf" if dv_cost == float("inf") else str(int(dv_cost))
        dv_nh = final_nh[src_cmp][dest] if final_nh[src_cmp][dest] else "—"
        match = "yes" if ls_cost == int(dv_cost) else "**NO**"
        if ls_cost != int(dv_cost):
            all_match = False
        cmp_rows.append(f"| {dest} | {ls_cost} | {ls_path} | {dv_cost_str} | {dv_nh} | {match} |")

    cmp_table = f"{cmp_header}\n{cmp_sep}\n" + "\n".join(cmp_rows)

    match_msg = "All costs match!" if all_match else "**Mismatch detected** — check the graph."

    # Side-by-side SPT visualization
    fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(14, 5.5))
    pos_cmp = nx.spring_layout(G, seed=42)
    edge_labels_cmp = {k: int(v) if v == int(v) else v
                       for k, v in nx.get_edge_attributes(G, "weight").items()}

    # Left: Dijkstra SPT
    tree_edges_ls = []
    for _dest in nodes_cmp:
        if _dest == src_cmp:
            continue
        _path = paths_ls[_dest]
        for _i in range(len(_path) - 1):
            _e = tuple(sorted((_path[_i], _path[_i + 1])))
            if _e not in tree_edges_ls:
                tree_edges_ls.append(_e)

    nx.draw(G, pos_cmp, ax=ax5a, with_labels=True, node_color="lightyellow",
            node_size=700, font_size=13, font_weight="bold",
            edge_color="lightgray", width=1, style="dashed")
    nx.draw_networkx_edges(G, pos_cmp, edgelist=tree_edges_ls, ax=ax5a,
                           edge_color="red", width=3)
    nx.draw_networkx_edge_labels(G, pos_cmp, edge_labels_cmp, font_size=11, ax=ax5a)
    # Highlight source
    nx.draw_networkx_nodes(G, pos_cmp, nodelist=[src_cmp], ax=ax5a,
                           node_color="orange", node_size=800)
    ax5a.set_title(f"Dijkstra SPT from {src_cmp} (Link-State)", fontsize=13)

    # Right: DV result — same tree (costs match), different color to distinguish
    tree_edges_dv = []
    for _dest in nodes_cmp:
        if _dest == src_cmp:
            continue
        # Trace path from DV next hops
        _current = src_cmp
        _visited = {_current}
        while _current != _dest:
            _nxt = final_nh[_current][_dest]
            if _nxt is None or _nxt in _visited:
                break
            _e = tuple(sorted((_current, _nxt)))
            if _e not in tree_edges_dv:
                tree_edges_dv.append(_e)
            _visited.add(_nxt)
            _current = _nxt

    nx.draw(G, pos_cmp, ax=ax5b, with_labels=True, node_color="lightyellow",
            node_size=700, font_size=13, font_weight="bold",
            edge_color="lightgray", width=1, style="dashed")
    nx.draw_networkx_edges(G, pos_cmp, edgelist=tree_edges_dv, ax=ax5b,
                           edge_color="blue", width=3)
    nx.draw_networkx_edge_labels(G, pos_cmp, edge_labels_cmp, font_size=11, ax=ax5b)
    nx.draw_networkx_nodes(G, pos_cmp, nodelist=[src_cmp], ax=ax5b,
                           node_color="orange", node_size=800)
    ax5b.set_title(f"DV Result from {src_cmp} ({len(history)-1} rounds)", fontsize=13)
    plt.tight_layout()

    # Complexity comparison
    n_nodes = len(nodes_cmp)
    n_edges = len(G.edges())
    complexity = (
        f"**Dijkstra**: O({n_nodes}^2) = O({n_nodes**2}) with simple array; "
        f"needs full topology ({n_edges} edges stored at every node).\n\n"
        f"**DV**: {len(history)-1} rounds of neighbor exchange; "
        f"each node stores only its distance vector ({n_nodes} entries) "
        f"and talks to {max(G.degree(n) for n in G.nodes())} neighbors (max degree)."
    )

    mo.vstack([
        mo.md(f"### Comparison from source **{src_cmp}**\n\n{cmp_table}\n\n{match_msg}"),
        fig5,
        mo.md(complexity),
    ])
    return cmp_rows, cmp_table, fig5, src_cmp


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Summary

    | Property | Link-State (Dijkstra) | Distance-Vector (Bellman-Ford) |
    | --- | --- | --- |
    | **Information** | Full topology at every node | Only neighbor distances |
    | **Communication** | Flood LSAs to all routers | Exchange DVs with neighbors |
    | **Convergence (good news)** | Fast | Fast |
    | **Convergence (bad news)** | Fast | **Slow** (count-to-infinity) |
    | **Loop-free?** | Yes | Not during convergence |
    | **Deployed as** | OSPF, IS-IS | RIP |

    Both algorithms compute the **same shortest paths** — they are different
    distributed methods for the same mathematical problem. The key difference
    is in failure handling: LS reconverges quickly, DV can count to infinity.

    **BGP** is a third approach (path vector) used **between** autonomous systems,
    where routing is driven by business policy rather than shortest paths.
    """)
    return


if __name__ == "__main__":
    app.run()
