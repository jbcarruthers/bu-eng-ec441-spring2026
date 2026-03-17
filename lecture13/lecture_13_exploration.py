import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import ipaddress
    import subprocess
    import sys
    import re
    return ipaddress, mo, mpatches, plt, re, subprocess, sys


@app.cell
def _(mo):
    mo.md("""
    # Lecture 13: The Network Layer — Interactive Exploration

    **EC 441 - Introduction to Computer Networking**
    Boston University, Spring 2026

    This notebook has five interactive parts:

    1. **The Narrow Waist** — IP as the universal substrate connecting all layers
    2. **Your Routing Table** — read the actual routing table on this machine
    3. **Longest Prefix Match** — interactive prefix matching visualizer
    4. **Traceroute Explorer** — visualize the path to a remote host
    5. **TTL Countdown** — simulate how TTL decrements across hops

    Work through these in order, or jump to any section that interests you.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 1: The Narrow Waist
    """)
    return


@app.cell
def _(plt):
    # Draw the hourglass / narrow waist diagram
    plt.close('all')
    fig1, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # Layer data: (label, color, half-width, y_center)
    layers = [
        ("Applications: HTTP, DNS, SMTP, SSH, video, ...", "#AED6F1", 3.2, 4.8),
        ("Transport: TCP, UDP, QUIC",                      "#5DADE2", 2.2, 3.7),
        ("IP  —  the narrow waist",                        "#E67E22", 1.1, 2.6),
        ("Link: Ethernet, WiFi, LTE, cable, ...",          "#82E0AA", 2.2, 1.5),
        ("Physical: copper, radio, fiber, ...",            "#D5F5E3", 3.2, 0.4),
    ]

    bar_height = 0.75
    center_x = 3.0

    for label, color, half_w, yc in layers:
        x0 = center_x - half_w
        x1 = center_x + half_w
        rect = plt.Rectangle((x0, yc - bar_height / 2), x1 - x0, bar_height,
                              facecolor=color, edgecolor='#555555', linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        fontweight = 'bold' if 'narrow waist' in label else 'normal'
        ax.text(center_x, yc, label, ha='center', va='center',
                fontsize=9.5, fontweight=fontweight, zorder=3, wrap=True)

    ax.set_title("The Internet Hourglass / Narrow Waist", fontsize=13, fontweight='bold', pad=8)

    # Arrows suggesting traffic flow
    for y in [4.2, 3.15, 2.05, 0.95]:
        ax.annotate('', xy=(center_x, y - 0.05), xytext=(center_x, y + 0.05),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5),
                    zorder=4)

    plt.tight_layout()
    fig1
    return


@app.cell
def _(mo):
    mo.md("""
    ### Why IP is the "narrow waist"

    The Internet protocol stack is deliberately shaped like an hourglass:

    - **Above IP**: every application protocol — HTTP, DNS, SMTP, SSH, BitTorrent, video streaming —
      is built on top of IP.  New applications require no changes to the network.
    - **IP itself**: one thin layer with a deliberately simple job — move packets from source to
      destination, best-effort, no guarantees.
    - **Below IP**: every link technology — Ethernet, WiFi, LTE, cable modem, fiber, satellite —
      can carry IP packets.  New physical media require no changes to the application layer.

    This is sometimes stated as: *everything runs over IP, and IP runs over everything.*

    The simplicity of IP is a **feature**, not a limitation.  Keeping the waist narrow means both
    innovation layers (applications and physical media) can evolve independently.  The cost is that
    reliability, ordering, and congestion control must be handled end-to-end (by TCP, QUIC, etc.),
    not by the network itself.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 2: Your Routing Table
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### What is a routing table?

    Every device that forwards IP packets — your laptop, a home router, or a backbone router —
    maintains a **routing table** (also called a Forwarding Information Base, or FIB).

    The routing table is the interface between the **control plane** (how routes are learned —
    RIP, OSPF, BGP, or static configuration) and the **data plane** (what happens to each
    arriving packet).

    Each entry in the table says: *"If the destination address matches this prefix, send the
    packet out this interface toward this next hop."*

    When multiple entries match, the router uses the **longest prefix** — the most specific
    route wins.  That rule is the topic of Part 3.
    """)
    return


@app.cell
def _(mo):
    read_rt_btn = mo.ui.run_button(label="Read Routing Table")
    read_rt_btn
    return (read_rt_btn,)


@app.cell
def _(mo, read_rt_btn, subprocess, sys):
    if not read_rt_btn.value:
        display_result = mo.md(
            "_Click **Read Routing Table** above to fetch the routing table on this machine._"
        )
    else:
        try:
            if sys.platform.startswith("linux"):
                _result = subprocess.run(
                    ["ip", "route", "show"],
                    capture_output=True, text=True, timeout=10
                )
            else:
                # macOS / BSD
                _result = subprocess.run(
                    ["netstat", "-rn"],
                    capture_output=True, text=True, timeout=10
                )

            if _result.returncode != 0 or not _result.stdout.strip():
                display_result = mo.md(
                    f"**Command failed or returned no output.**\n\n"
                    f"stderr: `{_result.stderr.strip()}`"
                )
            else:
                raw = _result.stdout.strip()
                cmd_name = "ip route show" if sys.platform.startswith("linux") else "netstat -rn"
                display_result = mo.vstack([
                    mo.md(f"### Routing table (`{cmd_name}`)"),
                    mo.md(f"```\n{raw}\n```"),
                    mo.md(
                        """
                        **How to read this table:**

                        | Column | Meaning |
                        |--------|---------|
                        | Destination | The network prefix (address/mask) this entry covers |
                        | Gateway / next hop | Where to forward the packet next |
                        | Flags | U = up, G = gateway, H = host route |
                        | Interface | Which NIC to send the packet out |

                        The entry with destination **0.0.0.0/0** (or `default`) is the **default route** —
                        it matches every address and is used when no more-specific prefix matches.
                        It points to your default gateway (usually your home router).
                        """
                    ),
                ])
        except FileNotFoundError as e:
            display_result = mo.md(f"**Command not found**: `{e}`. Try running this on a Linux or macOS machine.")
        except subprocess.TimeoutExpired:
            display_result = mo.md("**Timed out** reading the routing table.")
        except Exception as e:
            display_result = mo.md(f"**Unexpected error**: `{e}`")

    display_result
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 3: Longest Prefix Match Visualizer
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### The Longest Prefix Match (LPM) rule

    When a router looks up a destination address in its routing table, there may be
    **multiple matching entries**.  For example, the address `10.1.2.5` matches:

    - `0.0.0.0/0`  (default route — matches everything)
    - `10.0.0.0/8`  (covers all of 10.x.x.x)
    - `10.1.0.0/16`  (covers all of 10.1.x.x)
    - `10.1.2.0/24`  (covers only 10.1.2.x)

    The rule is: **always forward using the longest (most specific) matching prefix.**
    A /24 prefix is more specific than a /16, which is more specific than /8.

    This allows hierarchical routing: a campus or ISP can announce a large aggregate prefix
    to the world while using more-specific internal prefixes for local routing.

    Use the visualizer below to see which prefix wins for any destination address.
    """)
    return


@app.cell
def _():
    lpm_table = [
        ("0.0.0.0/0",       "203.0.113.1",  "eth0"),
        ("10.0.0.0/8",      "10.255.0.1",   "eth1"),
        ("10.1.0.0/16",     "10.1.255.1",   "eth2"),
        ("10.1.2.0/24",     "10.1.2.254",   "eth3"),
        ("192.168.0.0/16",  "192.168.0.1",  "eth4"),
    ]
    return (lpm_table,)


@app.cell
def _(mo):
    dest_input = mo.ui.text(value="10.1.2.5", label="Destination IP address:")
    dest_input
    return (dest_input,)


@app.cell
def _(dest_input, ipaddress, lpm_table, mo, mpatches, plt):
    dest_str = dest_input.value.strip()

    try:
        dest_ip = ipaddress.ip_address(dest_str)
        ip_valid = True
        ip_error = None
    except ValueError as e:
        dest_ip = None
        ip_valid = False
        ip_error = str(e)

    if not ip_valid:
        lpm_display = mo.md(f"**Invalid IP address**: `{dest_str}` — {ip_error}")
    else:
        # Check each entry
        matches = []
        results = []
        for prefix_str, next_hop, iface in lpm_table:
            network = ipaddress.ip_network(prefix_str, strict=False)
            is_match = (dest_ip in network)
            results.append((prefix_str, network.prefixlen, next_hop, iface, is_match))
            if is_match:
                matches.append((network.prefixlen, prefix_str, next_hop, iface))

        if matches:
            best_len, best_prefix, best_hop, best_iface = max(matches, key=lambda x: x[0])
        else:
            best_prefix = None

        # Build matplotlib table visualization
        plt.close('all')
        fig3, ax3 = plt.subplots(figsize=(8.5, 2.8))
        ax3.axis('off')

        col_labels = ["Prefix", "Prefix\nLength", "Next Hop", "Interface", "Match?"]
        table_data = []
        cell_colors = []

        WIN_COLOR  = "#A9DFBF"   # green  — winning match
        HIT_COLOR  = "#FAD7A0"   # yellow — other match
        MISS_COLOR = "#F2F3F4"   # gray   — no match

        for prefix_str, plen, next_hop, iface, is_match in results:
            is_winner = is_match and (prefix_str == best_prefix)
            if is_winner:
                status = "MATCH ★ (winner)"
                row_color = [WIN_COLOR] * 5
            elif is_match:
                status = "MATCH"
                row_color = [HIT_COLOR] * 5
            else:
                status = "no match"
                row_color = [MISS_COLOR] * 5
            table_data.append([prefix_str, f"/{plen}", next_hop, iface, status])
            cell_colors.append(row_color)

        tbl = ax3.table(
            cellText=table_data,
            colLabels=col_labels,
            cellLoc='center',
            loc='center',
            cellColours=cell_colors,
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9.5)
        tbl.scale(1, 1.6)

        ax3.set_title(f"LPM lookup for destination: {dest_str}", fontsize=11, fontweight='bold', pad=10)

        # Legend
        legend_handles = [
            mpatches.Patch(facecolor=WIN_COLOR,  label="Longest match (winner)"),
            mpatches.Patch(facecolor=HIT_COLOR,  label="Shorter match"),
            mpatches.Patch(facecolor=MISS_COLOR, label="No match"),
        ]
        ax3.legend(handles=legend_handles, loc='lower right', fontsize=8,
                   bbox_to_anchor=(1.0, -0.12), ncol=3, frameon=True)

        plt.tight_layout()

        # Summary text
        if best_prefix:
            summary_md = mo.md(
                f"**Result**: Destination `{dest_str}` → "
                f"longest match **{best_prefix}** (/{best_len}), "
                f"interface **{best_iface}**, "
                f"next hop **{best_hop}**"
            )
        else:
            summary_md = mo.md(f"**No match found** for `{dest_str}` — packet would be dropped (no default route).")

        lpm_display = mo.vstack([fig3, summary_md])

    lpm_display
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 4: Traceroute Explorer
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### How traceroute works

    Traceroute exploits the **Time-To-Live (TTL)** field in every IP packet.

    1. Send a probe packet with TTL = 1.  The first router decrements TTL to 0, discards
       the packet, and sends back an **ICMP Time Exceeded** message.  That reveals Hop 1.
    2. Send with TTL = 2 — Hop 2 is revealed.
    3. Continue until the destination replies (with ICMP Port Unreachable or ICMP Echo Reply).

    This is **purely normal data-plane behavior** — no special router support required.
    Every router in the Internet already implements TTL decrement and ICMP Time Exceeded.

    **`* * *` hops** are routers that have firewalls blocking outbound ICMP Time Exceeded.
    The path is not broken; those routers simply stay silent.
    """)
    return


@app.cell
def _(mo):
    trace_target = mo.ui.text(value="google.com", label="Target hostname or IP:")
    run_trace_btn = mo.ui.run_button(label="Run Traceroute")
    mo.vstack([trace_target, run_trace_btn])
    return run_trace_btn, trace_target


@app.cell
def _(mo, re, run_trace_btn, subprocess, sys, trace_target):
    if not run_trace_btn.value:
        trace_display = mo.md(
            "_Enter a hostname or IP address above, then click **Run Traceroute**._\n\n"
            "Traceroute may take 10–30 seconds depending on the target and network conditions."
        )
    else:
        target_host = trace_target.value.strip()
        if not target_host:
            trace_display = mo.md("**Please enter a target hostname or IP address.**")
        else:
            try:
                if sys.platform.startswith("linux"):
                    cmd = ["traceroute", "-n", "-m", "15", "-w", "2", target_host]
                else:
                    # macOS
                    cmd = ["traceroute", "-n", "-m", "15", "-w", "2", target_host]

                _result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=90
                )
                output = _result.stdout.strip()

                if not output:
                    trace_display = mo.md(
                        f"**No output from traceroute.**\n\n"
                        f"stderr: `{_result.stderr.strip()}`"
                    )
                else:
                    # Parse traceroute output
                    # Format: "  1  192.168.1.1  1.234 ms  1.100 ms  0.987 ms"
                    # or:     "  2  * * *"
                    rows = []
                    for line in output.splitlines():
                        # Skip header line
                        if re.match(r'^traceroute', line, re.IGNORECASE):
                            continue
                        m = re.match(
                            r'^\s*(\d+)\s+([\d.*]+(?:\s+[\d.*]+)*)\s*(.*)', line
                        )
                        if not m:
                            continue
                        hop_num = m.group(1)
                        rest = line.split()
                        if len(rest) < 2:
                            continue
                        hop_num = rest[0]
                        # Extract IP (or *)
                        ip_addr = rest[1] if len(rest) > 1 else "*"
                        # Extract RTT values — find all "X ms" patterns
                        rtts = re.findall(r'(\d+\.\d+)\s+ms', line)
                        if rtts:
                            rtt_str = " / ".join(rtts) + " ms"
                        elif ip_addr == "*":
                            rtt_str = "* * *"
                        else:
                            rtt_str = "(no RTT)"
                        rows.append((hop_num, ip_addr, rtt_str))

                    if rows:
                        table_header = "| Hop | IP Address | RTT |\n|-----|-----------|-----|\n"
                        table_body = "\n".join(
                            f"| {h} | `{ip}` | {rtt} |" for h, ip, rtt in rows
                        )
                        table_md = table_header + table_body
                    else:
                        table_md = "_Could not parse traceroute output._\n\n```\n" + output + "\n```"

                    trace_display = mo.vstack([
                        mo.md(f"### Traceroute to `{target_host}`"),
                        mo.md(table_md),
                        mo.md(
                            "> **Note:** Hops showing `* * *` have firewalls blocking ICMP Time Exceeded "
                            "— the path is not broken.  Traceroute simply cannot identify those routers."
                        ),
                        mo.md("**Raw output:**"),
                        mo.md(f"```\n{output}\n```"),
                    ])

            except FileNotFoundError:
                trace_display = mo.md(
                    "**`traceroute` not found** on this system.  "
                    "Install it with `brew install traceroute` (macOS) or `apt install traceroute` (Linux)."
                )
            except subprocess.TimeoutExpired:
                trace_display = mo.md(
                    "**Traceroute timed out** (90 s).  "
                    "Try a closer target, or check your network connection."
                )
            except Exception as e:
                trace_display = mo.md(f"**Unexpected error**: `{e}`")

    trace_display
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Part 5: TTL Countdown Simulator
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### TTL (Time-To-Live) and loop prevention

    Every IP packet carries a **TTL** field — an 8-bit integer.  Each router that forwards
    the packet **decrements TTL by 1** before sending it on.  If TTL reaches **0**, the
    packet is discarded and an ICMP Time Exceeded message is sent back to the source.

    **Why TTL exists:** Without it, a packet caught in a routing loop would circulate forever,
    wasting bandwidth.  TTL bounds the lifetime of any packet to at most 255 hops.

    **Typical starting values:**
    - Linux / macOS: **64**
    - Windows: **128**
    - Cisco IOS / network equipment: **255**

    **What an observed TTL tells you:** If you receive a packet with TTL = 55, and you know
    the source typically sets TTL = 64, the packet has traveled approximately 9 hops.
    This can be used to estimate path length — or detect TTL-spoofing attacks.

    Use the sliders to explore how TTL decrements with hop count.
    """)
    return


@app.cell
def _(mo):
    ttl_slider = mo.ui.slider(start=1, stop=255, step=1, value=64,
                               label="Initial TTL:", show_value=True)
    hops_slider = mo.ui.slider(start=1, stop=30, step=1, value=10,
                                label="Number of hops:", show_value=True)
    mo.vstack([ttl_slider, hops_slider])
    return hops_slider, ttl_slider


@app.cell
def _(hops_slider, mo, mpatches, plt, ttl_slider):
    initial_ttl = ttl_slider.value
    n_hops = hops_slider.value

    hops = list(range(n_hops + 1))          # 0 = source, 1..n_hops = routers
    ttl_values = [max(0, initial_ttl - h) for h in hops]

    # Determine drop hop (first hop where TTL would be 0 after decrement)
    drop_hop = None
    if initial_ttl <= n_hops:
        drop_hop = initial_ttl   # TTL hits 0 at this hop index

    # Bar colors
    def _bar_color(ttl_val, is_drop):
        if is_drop:
            return "#E74C3C"   # red — dropped
        elif ttl_val > 10:
            return "#2ECC71"   # green — healthy
        elif ttl_val > 0:
            return "#F39C12"   # yellow — low
        else:
            return "#E74C3C"   # red — zero

    bar_colors = [
        _bar_color(ttl_values[h], (drop_hop is not None and h == drop_hop))
        for h in hops
    ]

    plt.close('all')
    fig5, ax5 = plt.subplots(figsize=(9, 4.5))

    bars = ax5.bar(hops, ttl_values, color=bar_colors, edgecolor='#555555', linewidth=0.8)

    # Label each bar with its TTL value
    for h, tv in zip(hops, ttl_values):
        if tv > 0:
            ax5.text(h, tv + 1.5, str(tv), ha='center', va='bottom', fontsize=8)

    # Mark the drop hop
    if drop_hop is not None and drop_hop <= n_hops:
        ax5.annotate(
            "DROPPED\n(TTL=0)",
            xy=(drop_hop, 0),
            xytext=(drop_hop, initial_ttl * 0.25 + 10),
            ha='center',
            fontsize=9, fontweight='bold', color='#E74C3C',
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.8),
        )

    # Horizontal line at TTL=0
    ax5.axhline(y=0, color='#333333', linewidth=1.2)

    # Axis formatting
    ax5.set_xticks(hops)
    ax5.set_xticklabels(
        ["Source (Hop 0)"] + [f"Hop {h}" for h in range(1, n_hops + 1)],
        rotation=45, ha='right', fontsize=8
    )
    ax5.set_ylim(-5, 270)
    ax5.set_ylabel("TTL value", fontsize=10)
    ax5.set_title(
        f"TTL countdown: starts at {initial_ttl}, {n_hops} hops",
        fontsize=12, fontweight='bold'
    )

    # Legend
    legend_handles5 = [
        mpatches.Patch(facecolor="#2ECC71", label="TTL > 10 (healthy)"),
        mpatches.Patch(facecolor="#F39C12", label="TTL 1–10 (low)"),
        mpatches.Patch(facecolor="#E74C3C", label="TTL = 0 (dropped)"),
    ]
    ax5.legend(handles=legend_handles5, loc='upper right', fontsize=9)

    plt.tight_layout()

    # Build the note
    if drop_hop is None or drop_hop > n_hops:
        survival_note = (
            f"The packet **survives** all {n_hops} hops "
            f"(TTL remaining at destination: **{ttl_values[n_hops]}**)."
        )
    else:
        survival_note = (
            f"The packet is **dropped at hop {drop_hop}** "
            f"— it cannot reach a destination more than {initial_ttl} hops away."
        )

    # Observed TTL estimation examples
    common_ttls = [64, 128, 255]
    observed = max(1, initial_ttl - n_hops) if drop_hop is None else 0

    estimation_rows = "\n".join(
        f"| {c} | `{c}` | `{max(0, c - observed)}` hops |"
        for c in common_ttls
        if c >= observed
    )

    ttl_note = mo.md(
        f"""
        **Initial TTL: {initial_ttl}** (typical defaults: 64 = Linux/macOS, 128 = Windows, 255 = Cisco/network gear)

        {survival_note}

        **Estimating path length from an observed TTL:**
        If you receive a packet with TTL = `{observed}`, the source likely set one of these common defaults:

        | Observed TTL | Assumed source TTL | Estimated hops traveled |
        |---|---|---|
        {estimation_rows}

        This heuristic is useful for network diagnostics and detecting spoofed packets.
        """
    )

    mo.vstack([fig5, ttl_note])
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Summary

    In this notebook we explored five core concepts from Lecture 13:

    1. **The Narrow Waist**: IP occupies a single, thin layer between diverse physical media
       below and diverse applications above.  This architectural choice is why the Internet
       could absorb new link technologies (WiFi, LTE, fiber) and new applications (the Web,
       streaming, VoIP) without redesigning the core.

    2. **Your Routing Table**: Every forwarding device holds a table mapping destination
       prefixes to next hops and outgoing interfaces.  The table is the heart of the data
       plane.  You read the real table on this machine using `netstat -rn` or `ip route show`.

    3. **Longest Prefix Match**: When multiple prefixes match a destination, the most specific
       (longest) prefix wins.  This rule enables hierarchical routing and efficient aggregation.

    4. **Traceroute**: A clever trick using TTL to reveal the sequence of routers on a path.
       No special router support is needed — just normal IP forwarding plus ICMP Time Exceeded.

    5. **TTL Countdown**: TTL prevents packets from looping forever.  Observing the TTL in
       received packets can reveal approximate hop counts and detect anomalies.

    ---
    **Coming up:**

    - **L14** — IP addressing in depth: CIDR, subnetting, address allocation, NAT
    - **L15–L16** — Routing algorithms: link-state (Dijkstra / OSPF) and distance-vector (Bellman-Ford / RIP)
    - **L17** — Inter-domain routing and BGP: how the ~80,000 autonomous systems of the Internet
      exchange reachability information
    """)
    return


if __name__ == "__main__":
    app.run()
