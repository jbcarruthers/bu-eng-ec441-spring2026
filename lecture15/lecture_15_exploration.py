import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    return mo, mpatches, np, nx, plt


@app.cell
def _(mo):
    mo.md("""
    # Lecture 15: Link-State Routing and Dijkstra's Algorithm — Interactive Exploration

    **EC 441 - Introduction to Computer Networking**
    Boston University, Spring 2026

    This notebook has six interactive parts:

    1. **Network Graph Builder** — define edges and weights, visualize the network graph
    2. **Dijkstra Step-by-Step** — watch the algorithm run with a full trace table
    3. **Shortest-Path Tree** — visualize the SPT and derive the forwarding table
    4. **Link Failure Simulator** — see how routing changes when a link fails
    5. **OSPF Cost Calculator** — compute OSPF link costs from bandwidth
    6. **Edge Weight Explorer** — how different weight schemes change shortest paths
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
    The default is the 6-node example from the lecture slides.
    """)
    return


@app.cell
def _(mo):
    edge_input = mo.ui.text_area(
        value="u-v:2\nu-w:1\nu-x:5\nv-y:3\nw-y:3\nw-z:2\nx-z:1\ny-z:4",
        label="Network edges (node1-node2:cost):",
        rows=10,
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
        G = nx.Graph()
        for src, dst, cost in edges:
            G.add_edge(src, dst, weight=cost)
        return G

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

    # Build adjacency info
    adj_rows = []
    for _node in sorted(G.nodes()):
        _neighbors = sorted(G.neighbors(_node))
        _neighbor_strs = [f"{n} (cost {int(G[_node][n]['weight'])})" for n in _neighbors]
        adj_rows.append(f"| {_node} | {len(_neighbors)} | {', '.join(_neighbor_strs)} |")

    adj_table = "| Node | Degree | Neighbors |\n| --- | --- | --- |\n" + "\n".join(adj_rows)

    mo.vstack([fig1, mo.md(f"**Adjacency list** ({len(G.nodes())} nodes, {len(G.edges())} edges):\n\n{adj_table}")])
    return ax1, fig1, pos


# ============================================================
# Part 2: Dijkstra Step-by-Step
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 2: Dijkstra Step-by-Step Visualizer

    Select a source node and watch Dijkstra's algorithm run.
    The trace table shows $D(v)$, $p(v)$, and the finalized set $N'$ at each step —
    matching the table format from the slides.
    """)
    return


@app.cell
def _(G, mo):
    source_dropdown = mo.ui.dropdown(
        options=sorted(G.nodes()),
        value=sorted(G.nodes())[0] if G.nodes() else "u",
        label="Source node:",
    )
    source_dropdown
    return (source_dropdown,)


@app.cell
def _(G, mo, source_dropdown):
    def dijkstra_trace(graph, source):
        """Run Dijkstra with step-by-step trace. Returns (dist, pred, trace_rows)."""
        nodes = sorted(graph.nodes())
        dist = {v: float("inf") for v in nodes}
        pred = {v: None for v in nodes}
        dist[source] = 0
        remaining = set(nodes)
        finalized = []
        trace = []

        # Record init state
        non_source = [v for v in nodes if v != source]
        # Set initial distances for source neighbors
        for neighbor in graph.neighbors(source):
            dist[neighbor] = graph[source][neighbor]["weight"]
            pred[neighbor] = source

        row = {
            "step": "Init",
            "N_prime": [source],
            "selected": "—",
        }
        for v in non_source:
            d = dist[v]
            p = pred[v]
            row[v] = (d, p)
        trace.append(row)

        remaining.remove(source)
        finalized.append(source)

        step = 1
        while remaining:
            # Find minimum
            w = min(remaining, key=lambda x: dist[x])
            remaining.remove(w)
            finalized.append(w)

            # Relax neighbors
            updates = {}
            for neighbor in graph.neighbors(w):
                if neighbor in remaining:
                    alt = dist[w] + graph[w][neighbor]["weight"]
                    if alt < dist[neighbor]:
                        old = dist[neighbor]
                        dist[neighbor] = alt
                        pred[neighbor] = w
                        updates[neighbor] = (old, alt)

            row = {
                "step": str(step),
                "N_prime": list(finalized),
                "selected": w,
            }
            for v in non_source:
                d = dist[v]
                p = pred[v]
                improved = v in updates
                row[v] = (d, p, improved, updates.get(v))
                if v in finalized and v != w:
                    row[v] = "done"
            trace.append(row)
            step += 1

        return dist, pred, trace, non_source

    source = source_dropdown.value
    dist, pred, trace, non_source = dijkstra_trace(G, source)

    # Build markdown table
    header = "| Step | N' | " + " | ".join(f"D({v}), p({v})" for v in non_source) + " | Select |"
    sep = "| --- " * (len(non_source) + 3) + "|"
    rows = []
    for t in trace:
        n_str = "{" + ",".join(t["N_prime"]) + "}"
        cells = [t["step"], n_str]
        for v in non_source:
            val = t[v]
            if val == "done":
                cells.append("—")
            elif len(val) == 2:
                d, p = val
                d_str = "∞" if d == float("inf") else str(int(d))
                p_str = "—" if p is None else p
                cells.append(f"{d_str}, {p_str}")
            else:
                d, _p, improved, update_info = val
                d_str = "∞" if d == float("inf") else str(int(d))
                p_str = "—" if _p is None else _p
                if improved and update_info:
                    old_d = update_info[0]
                    old_str = "∞" if old_d == float("inf") else str(int(old_d))
                    cells.append(f"**{old_str}→{d_str}**, {p_str}")
                else:
                    cells.append(f"{d_str}, {p_str}")
        cells.append(str(t["selected"]))
        rows.append("| " + " | ".join(cells) + " |")

    table_md = header + "\n" + sep + "\n" + "\n".join(rows)

    mo.md(f"### Dijkstra trace from source **{source}**\n\n{table_md}")
    return dijkstra_trace, dist, non_source, pred, source, trace


# ============================================================
# Part 3: Shortest-Path Tree Visualization
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 3: Shortest-Path Tree Visualization

    Side-by-side comparison: full graph (left) vs. shortest-path tree highlighted in red (right).
    The forwarding table is derived from the SPT below.
    """)
    return


@app.cell
def _(G, dist, mo, nx, plt, pred, source):
    def get_path(pred_dict, src, dst):
        """Reconstruct path from predecessor dict."""
        if src == dst:
            return [src]
        if pred_dict[dst] is None:
            return None
        path = get_path(pred_dict, src, pred_dict[dst])
        if path is None:
            return None
        return path + [dst]

    def get_tree_edges(graph, pred_dict, src):
        """Extract SPT edges from predecessor pointers."""
        edges = []
        for v in graph.nodes():
            if v != src and pred_dict[v] is not None:
                e = tuple(sorted((pred_dict[v], v)))
                if e not in edges:
                    edges.append(e)
        return edges

    tree_edges = get_tree_edges(G, pred, source)
    pos2 = nx.spring_layout(G, seed=42)
    edge_labels = {k: int(v) if v == int(v) else v
                   for k, v in nx.get_edge_attributes(G, "weight").items()}

    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: full graph
    nx.draw(G, pos2, ax=ax2a, with_labels=True, node_color="lightblue",
            node_size=700, font_size=13, font_weight="bold",
            edge_color="gray", width=2)
    nx.draw_networkx_edge_labels(G, pos2, edge_labels, font_size=11, ax=ax2a)
    ax2a.set_title("Full Network Graph", fontsize=13)

    # Right: SPT highlighted
    nx.draw(G, pos2, ax=ax2b, with_labels=True, node_color="lightyellow",
            node_size=700, font_size=13, font_weight="bold",
            edge_color="lightgray", width=1, style="dashed")
    nx.draw_networkx_edges(G, pos2, edgelist=tree_edges, ax=ax2b,
                            edge_color="red", width=3)
    nx.draw_networkx_edge_labels(G, pos2, edge_labels, font_size=11, ax=ax2b)

    # Annotate costs
    for _node in G.nodes():
        if _node != source:
            x, y = pos2[_node]
            ax2b.annotate(f"cost={int(dist[_node])}", xy=(x, y),
                          fontsize=9, xytext=(5, 10), textcoords="offset points",
                          color="red", fontweight="bold")
    ax2b.set_title(f"Shortest-Path Tree from {source}", fontsize=13)
    plt.tight_layout()

    # Forwarding table
    fwd_rows = []
    for _dest in sorted(G.nodes()):
        if _dest == source:
            continue
        _path = get_path(pred, source, _dest)
        if _path and len(_path) >= 2:
            _next_hop = _path[1]
            _path_str = " → ".join(_path)
            fwd_rows.append(f"| {_dest} | {_next_hop} | {int(dist[_dest])} | {_path_str} |")

    fwd_table = "| Destination | Next Hop | Cost | Path |\n| --- | --- | --- | --- |\n" + "\n".join(fwd_rows)

    mo.vstack([
        fig2,
        mo.md(f"### Forwarding table for router **{source}**\n\n{fwd_table}"),
    ])
    return ax2a, ax2b, edge_labels, fig2, fwd_rows, fwd_table, get_path, get_tree_edges, pos2, tree_edges


# ============================================================
# Part 4: Link Failure Simulator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 4: Link Failure Simulator

    Select an edge to "fail" (its cost is set to 100). Compare the original and new
    shortest-path trees to see how routing adapts.
    """)
    return


@app.cell
def _(G, mo):
    edge_options = [f"{u}-{v}" for u, v in sorted(G.edges())]
    fail_dropdown = mo.ui.dropdown(
        options=edge_options,
        value=edge_options[5] if len(edge_options) > 5 else edge_options[0] if edge_options else "",
        label="Edge to fail:",
    )
    fail_dropdown
    return edge_options, fail_dropdown


@app.cell
def _(G, dijkstra_trace, dist, fail_dropdown, get_path, get_tree_edges, mo, nx, plt, pred, source):
    # Parse failed edge
    parts = fail_dropdown.value.split("-")
    fail_u, fail_v = parts[0], parts[1]

    # Build modified graph
    G_fail = G.copy()
    G_fail[fail_u][fail_v]["weight"] = 100

    # Run Dijkstra on modified graph
    dist2, pred2, _, _ = dijkstra_trace(G_fail, source)

    tree_edges_orig = get_tree_edges(G, pred, source)
    tree_edges_new = get_tree_edges(G_fail, pred2, source)

    pos3 = nx.spring_layout(G, seed=42)
    edge_labels_orig = {k: int(v) if v == int(v) else v
                        for k, v in nx.get_edge_attributes(G, "weight").items()}
    edge_labels_new = {k: int(v) if v == int(v) else v
                       for k, v in nx.get_edge_attributes(G_fail, "weight").items()}

    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: original SPT
    nx.draw(G, pos3, ax=ax3a, with_labels=True, node_color="lightyellow",
            node_size=700, font_size=13, font_weight="bold",
            edge_color="lightgray", width=1, style="dashed")
    nx.draw_networkx_edges(G, pos3, edgelist=tree_edges_orig, ax=ax3a,
                            edge_color="red", width=3)
    nx.draw_networkx_edge_labels(G, pos3, edge_labels_orig, font_size=11, ax=ax3a)
    ax3a.set_title(f"Original SPT from {source}", fontsize=13)

    # Right: new SPT after failure
    nx.draw(G_fail, pos3, ax=ax3b, with_labels=True, node_color="lightyellow",
            node_size=700, font_size=13, font_weight="bold",
            edge_color="lightgray", width=1, style="dashed")
    # Highlight failed edge with X
    nx.draw_networkx_edges(G_fail, pos3,
                            edgelist=[(fail_u, fail_v)], ax=ax3b,
                            edge_color="red", width=2, style="dotted")
    nx.draw_networkx_edges(G_fail, pos3, edgelist=tree_edges_new, ax=ax3b,
                            edge_color="green", width=3)
    nx.draw_networkx_edge_labels(G_fail, pos3, edge_labels_new, font_size=11, ax=ax3b)
    ax3b.set_title(f"SPT after {fail_u}–{fail_v} failure", fontsize=13)
    plt.tight_layout()

    # Compare forwarding tables
    diff_rows = []
    for _dest in sorted(G.nodes()):
        if _dest == source:
            continue
        _path_orig = get_path(pred, source, _dest)
        _path_new = get_path(pred2, source, _dest)
        _nh_orig = _path_orig[1] if _path_orig and len(_path_orig) >= 2 else "—"
        _nh_new = _path_new[1] if _path_new and len(_path_new) >= 2 else "—"
        _cost_orig = int(dist[_dest])
        _cost_new = int(dist2[_dest])
        _changed = "changed" if _nh_orig != _nh_new or _cost_orig != _cost_new else ""
        _path_new_str = " → ".join(_path_new) if _path_new else "—"
        diff_rows.append(f"| {_dest} | {_nh_orig} | {_nh_new} | {_cost_orig} | {_cost_new} | {_path_new_str} | {_changed} |")

    diff_table = ("| Dest | Old Next Hop | New Next Hop | Old Cost | New Cost | New Path | Changed |\n"
                  "| --- | --- | --- | --- | --- | --- | --- |\n" + "\n".join(diff_rows))

    mo.vstack([
        fig3,
        mo.md(f"### Forwarding table comparison (link {fail_u}–{fail_v} failed)\n\n{diff_table}"),
    ])
    return (ax3a, ax3b, diff_rows, diff_table, dist2, edge_labels_new, edge_labels_orig,
            fail_u, fail_v, fig3, parts, pos3, pred2, tree_edges_new, tree_edges_orig, G_fail)


# ============================================================
# Part 5: OSPF Cost Calculator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 5: OSPF Cost Calculator

    OSPF computes link cost as: **cost = reference_bandwidth / link_bandwidth**

    The default reference bandwidth is 10⁸ b/s (100 Mb/s). Modern implementations
    often use 10⁹ or 10¹⁰ to distinguish Gigabit and 10-Gigabit links.
    """)
    return


@app.cell
def _(mo):
    ref_bw_dropdown = mo.ui.dropdown(
        options={"10⁸ (100 Mb/s, classic)": 1e8,
                 "10⁹ (1 Gb/s)": 1e9,
                 "10¹⁰ (10 Gb/s)": 1e10},
        value="10⁸ (100 Mb/s, classic)",
        label="Reference bandwidth:",
    )
    link_bw_input = mo.ui.text(value="100", label="Link bandwidth (Mb/s):")
    mo.hstack([ref_bw_dropdown, link_bw_input])
    return link_bw_input, ref_bw_dropdown


@app.cell
def _(link_bw_input, mo, ref_bw_dropdown):
    ref_bw = ref_bw_dropdown.value
    try:
        link_bw_mbps = float(link_bw_input.value)
        link_bw_bps = link_bw_mbps * 1e6
        ospf_cost = max(1, int(ref_bw / link_bw_bps))
    except (ValueError, ZeroDivisionError):
        link_bw_mbps = 0
        ospf_cost = "—"

    # Common link types table
    common_links = [
        ("T1", 1.544),
        ("10 Mb/s Ethernet", 10),
        ("100 Mb/s Fast Ethernet", 100),
        ("1 Gb/s Gigabit Ethernet", 1000),
        ("10 Gb/s 10GbE", 10000),
        ("100 Gb/s", 100000),
    ]

    common_rows = []
    for name, bw in common_links:
        bw_bps = bw * 1e6
        cost = max(1, int(ref_bw / bw_bps))
        common_rows.append(f"| {name} | {bw} Mb/s | {cost} |")

    ref_label = f"{ref_bw:.0e}"
    table = (f"| Link Type | Bandwidth | OSPF Cost (ref={ref_label}) |\n"
             f"| --- | --- | --- |\n" + "\n".join(common_rows))

    result = f"**Your link**: {link_bw_mbps} Mb/s → OSPF cost = **{ospf_cost}**" if link_bw_mbps > 0 else ""

    mo.vstack([
        mo.md(result),
        mo.md(f"### Common link types\n\n{table}"),
    ])
    return common_links, common_rows, link_bw_bps, link_bw_mbps, ospf_cost, ref_bw, ref_label, table


# ============================================================
# Part 6: Edge Weight Explorer
# ============================================================

@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 6: Edge Weight Explorer

    The same network topology can produce **different shortest paths** depending on
    what the edge weights represent. This section shows three weight schemes side by side:

    - **Hop count**: every edge costs 1 (used by RIP)
    - **Inverse bandwidth**: cost = 10⁸ / bandwidth (used by OSPF)
    - **Delay-proportional**: cost proportional to propagation delay

    All three use the same topology — only the weights differ.
    """)
    return


@app.cell
def _(G, get_path, get_tree_edges, mo, nx, plt):
    # Build three versions of the graph with different weight schemes
    schemes = {
        "Hop Count\n(all costs = 1)": {},
        "Inverse Bandwidth\n(OSPF default)": {},
        "Delay-Proportional": {},
    }

    # Assign realistic bandwidths and delays to each edge based on original costs
    edge_properties = {}
    for u_node, v_node, data in G.edges(data=True):
        orig = data["weight"]
        # Higher original cost = lower bandwidth, higher delay
        edge_properties[(u_node, v_node)] = {
            "hop": 1,
            "inv_bw": orig,  # use original weights as inverse-BW proxy
            "delay": orig * 2,  # scale for visual distinction
        }

    G_hop = G.copy()
    G_bw = G.copy()
    G_delay = G.copy()

    for (u_node, v_node), props in edge_properties.items():
        G_hop[u_node][v_node]["weight"] = props["hop"]
        G_bw[u_node][v_node]["weight"] = props["inv_bw"]
        G_delay[u_node][v_node]["weight"] = props["delay"]

    graphs = [G_hop, G_bw, G_delay]
    titles = list(schemes.keys())

    # Pick source (first node alphabetically)
    src = sorted(G.nodes())[0]

    fig4, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    pos4 = nx.spring_layout(G, seed=42)

    path_summaries = []

    for i, (graph, title) in enumerate(zip(graphs, titles)):
        ax = axes[i]
        lengths, paths = nx.single_source_dijkstra(graph, src, weight="weight")

        # Get pred from paths
        pred_dict = {v: None for v in graph.nodes()}
        for _dest, _path in paths.items():
            if len(_path) >= 2:
                pred_dict[_dest] = _path[-2]

        te = get_tree_edges(graph, pred_dict, src)
        el = {k: int(v) if v == int(v) else v
              for k, v in nx.get_edge_attributes(graph, "weight").items()}

        nx.draw(graph, pos4, ax=ax, with_labels=True, node_color="lightyellow",
                node_size=600, font_size=11, font_weight="bold",
                edge_color="lightgray", width=1, style="dashed")
        nx.draw_networkx_edges(graph, pos4, edgelist=te, ax=ax,
                                edge_color="red", width=3)
        nx.draw_networkx_edge_labels(graph, pos4, el, font_size=10, ax=ax)
        ax.set_title(title, fontsize=11)

        # Collect path summary
        summary_lines = []
        for _dest in sorted(graph.nodes()):
            if _dest == src:
                continue
            _p = paths[_dest]
            summary_lines.append(f"{src}→{_dest}: cost {int(lengths[_dest])}, path {' → '.join(_p)}")
        path_summaries.append((title.replace('\n', ' '), summary_lines))

    plt.tight_layout()

    # Build comparison text
    comparison_parts = []
    for title, lines in path_summaries:
        comparison_parts.append(f"**{title}**\n\n" + "\n".join(f"- {line}" for line in lines))

    mo.vstack([
        fig4,
        mo.md("### Path comparison\n\n" + "\n\n".join(comparison_parts)),
        mo.md("""
        **Key takeaway**: the "shortest path" depends entirely on what the weights represent.
        Hop count minimizes router traversals; inverse bandwidth maximizes capacity;
        delay-proportional minimizes latency. The algorithm is the same — only the input changes.
        """),
    ])
    return (G_bw, G_delay, G_hop, axes, edge_properties, fig4, graphs, path_summaries,
            pos4, schemes, src, titles)


@app.cell
def _(mo):
    mo.md("""
    ---
    *Exploration notebook for EC 441 Lecture 15, Boston University, Spring 2026.*

    **Shared scripts**: `demo_dijkstra_l15.py` (from-scratch Dijkstra with step-by-step trace)
    """)
    return


if __name__ == "__main__":
    app.run()
