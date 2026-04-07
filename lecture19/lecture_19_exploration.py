import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    return GridSpec, math, mo, mpatches, np, plt


@app.cell
def _(mo):
    mo.md("""
# Lecture 19: TCP Part 1 — Connections, Sequencing, and Flow Control — Interactive Exploration

**EC 441 - Introduction to Computer Networking**
Boston University, Spring 2026

This notebook has three interactive parts:

1. **RTT Estimator Simulator** — watch EWMA + RTTVAR + RTO adapt to changing network conditions
2. **TCP 3-Way Handshake Visualizer** — step through SYN/SYN-ACK/ACK with sequence numbers
3. **Flow Control Simulator** — watch rwnd and bytes-in-flight interact
""")
    return


# ============================================================
# Part 1: RTT Estimator Simulator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 1: RTT Estimator Simulator

TCP uses an **Exponentially Weighted Moving Average (EWMA)** to estimate round-trip time and set the
retransmission timeout (RTO). The RFC 6298 algorithm:

$$\\text{SRTT} \\leftarrow (1-\\alpha)\\cdot\\text{SRTT} + \\alpha\\cdot R \\qquad (\\alpha = 1/8 \\text{ by default})$$

$$\\text{RTTVAR} \\leftarrow (1-\\beta)\\cdot\\text{RTTVAR} + \\beta\\cdot|\\text{SRTT} - R| \\qquad (\\beta = 1/4 \\text{ by default})$$

$$\\text{RTO} = \\text{SRTT} + 4\\cdot\\text{RTTVAR}$$

**SRTT** is a first-order IIR low-pass filter — it smooths out noise.
**RTTVAR** tracks the variance (noise power) of RTT samples.
The RTO adds a margin of 4·RTTVAR above the mean estimate to avoid spurious timeouts.
""")
    return


@app.cell
def _(mo):
    alpha_slider = mo.ui.slider(
        start=0.05, stop=0.5, step=0.05, value=0.125,
        label="α (EWMA weight for SRTT):", show_value=True
    )
    beta_slider = mo.ui.slider(
        start=0.05, stop=0.5, step=0.05, value=0.25,
        label="β (EWMA weight for RTTVAR):", show_value=True
    )
    scenario_dropdown = mo.ui.dropdown(
        options={
            "Stable (100 ms)": "stable",
            "Step change (50→150 ms at sample 20)": "step",
            "Periodic spikes (base 80 ms, spike to 300 ms every 10 samples)": "spikes",
            "Gradual drift (50→200 ms over 50 samples)": "drift",
            "Random walk (starts at 100 ms)": "randwalk",
        },
        value="Stable (100 ms)",
        label="RTT scenario:",
    )
    n_samples_slider = mo.ui.slider(
        start=20, stop=100, step=1, value=50,
        label="Number of RTT samples:", show_value=True
    )
    seed_slider = mo.ui.slider(
        start=0, stop=99, step=1, value=42,
        label="Random seed:", show_value=True
    )
    mo.vstack([
        mo.hstack([alpha_slider, beta_slider]),
        mo.hstack([scenario_dropdown, n_samples_slider, seed_slider]),
    ])
    return alpha_slider, beta_slider, n_samples_slider, scenario_dropdown, seed_slider


@app.cell
def _(alpha_slider, beta_slider, mo, n_samples_slider, np, plt, scenario_dropdown, seed_slider):
    _alpha = alpha_slider.value
    _beta = beta_slider.value
    _scenario = scenario_dropdown.value
    _n = n_samples_slider.value
    _seed = seed_slider.value

    _rng = np.random.default_rng(_seed)

    # Generate RTT samples
    if _scenario == "stable":
        _samples = _rng.normal(100, 5, _n).clip(1, None)
    elif _scenario == "step":
        _part1 = _rng.normal(50, 3, min(20, _n)).clip(1, None)
        _part2 = _rng.normal(150, 3, max(0, _n - 20)).clip(1, None)
        _samples = np.concatenate([_part1, _part2])
    elif _scenario == "spikes":
        _samples = _rng.normal(80, 5, _n).clip(1, None)
        for _i in range(0, _n, 10):
            _samples[_i] += 220
    elif _scenario == "drift":
        _base = np.linspace(50, 200, _n)
        _samples = (_base + _rng.normal(0, 8, _n)).clip(1, None)
    else:  # randwalk
        _samples = np.zeros(_n)
        _samples[0] = 100
        for _i in range(1, _n):
            _samples[_i] = (_samples[_i - 1] + _rng.normal(0, 10)).clip(10, 500)

    # Run EWMA filter
    _srtt_arr = np.zeros(_n)
    _rttvar_arr = np.zeros(_n)
    _rto_arr = np.zeros(_n)

    _srtt_arr[0] = _samples[0]
    _rttvar_arr[0] = _samples[0] / 2.0
    _rto_arr[0] = _srtt_arr[0] + 4.0 * _rttvar_arr[0]

    for _i in range(1, _n):
        _R = _samples[_i]
        _old_srtt = _srtt_arr[_i - 1]
        _old_rttvar = _rttvar_arr[_i - 1]
        _rttvar_arr[_i] = (1 - _beta) * _old_rttvar + _beta * abs(_old_srtt - _R)
        _srtt_arr[_i] = (1 - _alpha) * _old_srtt + _alpha * _R
        _rto_arr[_i] = max(_srtt_arr[_i] + 4.0 * _rttvar_arr[_i], 1.0)

    # Count spurious timeouts: raw RTT > RTO at that step
    _spurious = int(np.sum(_samples > _rto_arr))
    _time_constant = 1.0 / _alpha

    # Plot
    plt.close("all")
    _xs = np.arange(_n)
    _fig, _axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    # Top: raw RTT, SRTT, RTO
    _ax0 = _axes[0]
    _ax0.plot(_xs, _samples, color="gray", marker="o", markersize=3, linewidth=0.8, label="Raw RTT")
    _ax0.plot(_xs, _srtt_arr, color="blue", linewidth=2, label="SRTT")
    _ax0.plot(_xs, _rto_arr, color="red", linewidth=1.5, linestyle="--", label="RTO")
    _ax0.set_ylabel("RTT (ms)")
    _ax0.set_title("RTT Samples, SRTT, and RTO")
    _ax0.legend(loc="upper right", fontsize=8)
    _ax0.grid(True, alpha=0.3)

    # Middle: RTTVAR
    _ax1 = _axes[1]
    _ax1.plot(_xs, _rttvar_arr, color="orange", linewidth=2)
    _ax1.set_ylabel("RTTVAR (ms)")
    _ax1.set_title("RTTVAR (Variance Estimate)")
    _ax1.grid(True, alpha=0.3)

    # Bottom: RTO margin = 4·RTTVAR
    _ax2 = _axes[2]
    _margin = 4.0 * _rttvar_arr
    _ax2.fill_between(_xs, 0, _margin, color="green", alpha=0.4, label="4·RTTVAR")
    _ax2.plot(_xs, _margin, color="green", linewidth=1.5)
    _ax2.set_ylabel("RTO margin = 4·RTTVAR (ms)")
    _ax2.set_xlabel("Sample number")
    _ax2.set_title("RTO Safety Margin Above SRTT")
    _ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    _fig_out = plt.gcf()

    _stats = mo.md(f"""
**Final values** (sample {_n - 1}):
- SRTT = **{_srtt_arr[-1]:.1f} ms**
- RTTVAR = **{_rttvar_arr[-1]:.1f} ms**
- RTO = **{_rto_arr[-1]:.1f} ms**

**Filter time constant**: 1/α = {_time_constant:.1f} samples
(takes ~{_time_constant:.0f} samples to "forget" old data)

**Spurious RTO firings**: {_spurious} out of {_n} samples
(rounds where raw RTT > RTO — should be rare with a well-tuned estimator)
""")

    mo.vstack([_fig_out, _stats])


# ============================================================
# Part 2: TCP 3-Way Handshake Visualizer
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 2: TCP 3-Way Handshake Visualizer

The **3-way handshake** establishes a TCP connection and synchronizes Initial Sequence Numbers (ISNs)
in both directions. Each SYN consumes one sequence number (even though it carries no data).

Use the sliders to set the ISNs and the dropdown to step through the handshake.
""")
    return


@app.cell
def _(mo):
    client_isn_input = mo.ui.slider(
        start=0, stop=65535, step=1, value=1000,
        label="Client ISN (x):", show_value=True
    )
    server_isn_input = mo.ui.slider(
        start=0, stop=65535, step=1, value=5000,
        label="Server ISN (y):", show_value=True
    )
    show_step_dropdown = mo.ui.dropdown(
        options=["SYN sent", "SYN-ACK sent", "ACK sent (ESTABLISHED)"],
        value="ACK sent (ESTABLISHED)",
        label="Show through step:",
    )
    mo.vstack([
        mo.hstack([client_isn_input, server_isn_input]),
        show_step_dropdown,
    ])
    return client_isn_input, server_isn_input, show_step_dropdown


@app.cell
def _(client_isn_input, mo, plt, server_isn_input, show_step_dropdown):
    _x = client_isn_input.value
    _y = server_isn_input.value
    _step_label = show_step_dropdown.value

    _step_map = {
        "SYN sent": 1,
        "SYN-ACK sent": 2,
        "ACK sent (ESTABLISHED)": 3,
    }
    _max_step = _step_map[_step_label]

    plt.close("all")
    _fig2, _ax = plt.subplots(figsize=(8, 6))
    _ax.set_xlim(-0.3, 1.3)
    _ax.set_ylim(-0.2, 1.1)
    _ax.axis("off")

    # Time axis flows downward; y=1 is top, y=0 is bottom
    # Client at x=0, Server at x=1
    _t_start = 0.95
    _t_step = 0.28

    # Vertical timeline lines
    _ax.axvline(0, ymin=0.05, ymax=0.98, color="black", linewidth=2)
    _ax.axvline(1, ymin=0.05, ymax=0.98, color="black", linewidth=2)
    _ax.text(0, 1.05, "Client", ha="center", va="bottom", fontsize=12, fontweight="bold")
    _ax.text(1, 1.05, "Server", ha="center", va="bottom", fontsize=12, fontweight="bold")

    def _draw_arrow(ax, t_y, direction, label, annotation, color):
        if direction == "right":
            x0, x1 = 0.02, 0.98
        else:
            x0, x1 = 0.98, 0.02
        ax.annotate(
            "",
            xy=(x1, t_y),
            xytext=(x0, t_y),
            arrowprops=dict(arrowstyle="->", color=color, lw=2),
        )
        ax.text(0.5, t_y + 0.025, label, ha="center", va="bottom", fontsize=9,
                color=color, fontweight="bold")
        ax.text(0.5, t_y - 0.045, annotation, ha="center", va="top", fontsize=8,
                color="gray", style="italic")

    # Step 1: SYN
    _t1 = _t_start
    _draw_arrow(
        _ax, _t1, "right",
        f"SYN   seq={_x}   SYN=1",
        f"Consumes seq {_x}; next data byte = {_x + 1}",
        "steelblue",
    )

    # Step 2: SYN-ACK
    if _max_step >= 2:
        _t2 = _t1 - _t_step
        _draw_arrow(
            _ax, _t2, "left",
            f"SYN-ACK   seq={_y}   ack={_x + 1}",
            f"Server ISN={_y}; ACKs client SYN (ack={_x + 1})",
            "darkorange",
        )

    # Step 3: ACK
    if _max_step >= 3:
        _t3 = _t2 - _t_step
        _draw_arrow(
            _ax, _t3, "right",
            f"ACK   ack={_y + 1}",
            f"ACKs server SYN; connection ESTABLISHED",
            "steelblue",
        )
        # ESTABLISHED line
        _est_y = _t3 - 0.1
        _ax.axhline(_est_y, xmin=0.02, xmax=0.98, color="green",
                    linewidth=1.5, linestyle="--", alpha=0.7)
        _ax.text(0.5, _est_y - 0.02, "ESTABLISHED", ha="center", va="top",
                 fontsize=10, color="green", fontweight="bold")

    _ax.set_title("TCP 3-Way Handshake", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    _fig2_out = plt.gcf()

    _table_md = mo.md(f"""
| Field | Value |
|---|---|
| Client ISN | {_x} |
| Server ISN | {_y} |
| Client next seq (after SYN) | {_x + 1} |
| Server next seq (after SYN-ACK) | {_y + 1} |
| Client ACK field in step 3 | {_y + 1} |
""")

    mo.vstack([_fig2_out, _table_md])


# ============================================================
# Part 3: Flow Control Simulator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 3: Flow Control Simulator

TCP **flow control** prevents the sender from overwhelming the receiver's buffer.
The receiver advertises a **receive window** (rwnd) — how many bytes of free buffer space it has.
The sender may not have more than rwnd bytes unacknowledged at any time.

If rwnd drops to zero, the sender **stalls** until the receiver reads data and advertises space again.
""")
    return


@app.cell
def _(mo):
    buffer_size_slider = mo.ui.slider(
        start=4, stop=64, step=4, value=16,
        label="Receive buffer (KB):", show_value=True
    )
    app_read_rate_slider = mo.ui.slider(
        start=0.0, stop=1.0, step=0.05, value=0.3,
        label="App read rate (fraction of buffer/round):", show_value=True
    )
    segment_size_slider = mo.ui.slider(
        start=512, stop=4096, step=256, value=1460,
        label="Segment size (bytes):", show_value=True
    )
    n_rounds_slider = mo.ui.slider(
        start=5, stop=30, step=1, value=15,
        label="Rounds:", show_value=True
    )
    mo.vstack([
        mo.hstack([buffer_size_slider, app_read_rate_slider]),
        mo.hstack([segment_size_slider, n_rounds_slider]),
    ])
    return app_read_rate_slider, buffer_size_slider, n_rounds_slider, segment_size_slider


@app.cell
def _(app_read_rate_slider, buffer_size_slider, mo, n_rounds_slider, np, plt, segment_size_slider):
    _buf_kb = buffer_size_slider.value
    _buf_bytes = _buf_kb * 1024
    _read_rate = app_read_rate_slider.value
    _seg_size = segment_size_slider.value
    _n_rounds = n_rounds_slider.value

    # Simulate flow control rounds
    _buffered = np.zeros(_n_rounds)
    _rwnd = np.zeros(_n_rounds)
    _bytes_sent = np.zeros(_n_rounds)

    _cur_buffered = 0  # bytes currently in receiver buffer

    for _i in range(_n_rounds):
        # Receiver advertises rwnd = free space
        _free = max(0, _buf_bytes - _cur_buffered)
        _rwnd[_i] = _free

        # Sender sends up to min(rwnd, 3*seg_size) bytes this round
        _max_send = min(_free, 3 * _seg_size)
        # Quantize to whole segments
        _n_segs = int(_max_send // _seg_size)
        _sent = _n_segs * _seg_size
        _bytes_sent[_i] = _sent

        # Bytes arrive in buffer
        _cur_buffered = min(_cur_buffered + _sent, _buf_bytes)

        # App reads from buffer
        _app_read = int(_read_rate * _buf_bytes)
        _cur_buffered = max(0, _cur_buffered - _app_read)

        _buffered[_i] = _cur_buffered

    _stall_rounds = int(np.sum(_rwnd == 0))
    _avg_rwnd = float(np.mean(_rwnd))

    # Plot
    plt.close("all")
    _fig3, (_ax3l, _ax3r) = plt.subplots(1, 2, figsize=(12, 5))

    _rounds_x = np.arange(_n_rounds)
    _free_arr = np.maximum(0, _buf_bytes - _buffered)

    # Left: stacked bar — buffered (blue) + free/rwnd (green)
    _ax3l.bar(_rounds_x, _buffered / 1024, color="steelblue", label="Buffered (KB)", alpha=0.85)
    _ax3l.bar(_rounds_x, _free_arr / 1024, bottom=_buffered / 1024,
              color="mediumseagreen", label="Free / rwnd (KB)", alpha=0.85)
    _ax3l.axhline(_buf_kb, color="red", linestyle="--", linewidth=1.2, label=f"Buffer size ({_buf_kb} KB)")
    _ax3l.set_xlabel("Round")
    _ax3l.set_ylabel("KB")
    _ax3l.set_title("Receiver Buffer: Buffered vs. Free Space")
    _ax3l.legend(fontsize=8)
    _ax3l.grid(True, alpha=0.3, axis="y")

    # Annotate stalls on left plot
    for _i in range(_n_rounds):
        if _rwnd[_i] == 0:
            _ax3l.text(_i, _buf_kb + 0.3, "STALL", ha="center", va="bottom",
                       fontsize=7, color="red", fontweight="bold")

    # Right: line plot of rwnd and bytes sent
    _ax3r.plot(_rounds_x, _rwnd / 1024, color="darkorange", linewidth=2, marker="o",
               markersize=4, label="rwnd (KB)")
    _ax3r.plot(_rounds_x, _bytes_sent / 1024, color="steelblue", linewidth=1.5,
               linestyle="--", marker="s", markersize=4, label="Bytes sent (KB)")
    _ax3r.set_xlabel("Round")
    _ax3r.set_ylabel("KB")
    _ax3r.set_title("rwnd and Bytes Sent per Round")
    _ax3r.legend(fontsize=8)
    _ax3r.grid(True, alpha=0.3)

    # Annotate stalls on right plot
    for _i in range(_n_rounds):
        if _rwnd[_i] == 0:
            _ax3r.axvspan(_i - 0.4, _i + 0.4, alpha=0.2, color="red")
            _ax3r.text(_i, _ax3r.get_ylim()[1] * 0.95, "STALL", ha="center",
                       va="top", fontsize=7, color="red", fontweight="bold")

    plt.tight_layout()
    _fig3_out = plt.gcf()

    _summary3 = mo.md(f"""
**Flow Control Summary** ({_n_rounds} rounds, buffer = {_buf_kb} KB, segment = {_seg_size} B):
- Rounds sender **stalled** (rwnd = 0): **{_stall_rounds}**
- Average rwnd: **{_avg_rwnd / 1024:.1f} KB**
- App read rate: **{_read_rate * 100:.0f}%** of buffer per round
  ({int(_read_rate * _buf_bytes)} bytes/round = {_read_rate * _buf_bytes / _seg_size:.1f} segments/round)

*Tip: reduce the app read rate to see more stalls; increase it to keep the pipe flowing.*
""")

    mo.vstack([_fig3_out, _summary3])


if __name__ == "__main__":
    app.run()
