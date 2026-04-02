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
    return math, mo, mpatches, np, plt


@app.cell
def _(mo):
    mo.md("""
# Lecture 18: Transport Layer, UDP, and Reliable Data Transfer — Interactive Exploration

**EC 441 - Introduction to Computer Networking**
Boston University, Spring 2026

This notebook has three interactive parts:

1. **Link Utilization Explorer** — see why Stop-and-Wait starves high-BDP links and how window size fixes it
2. **Stop-and-Wait Trace Simulator** — step through packet loss and ACK loss scenarios with timing diagrams
3. **GBN vs SR Throughput** — compare effective throughput vs. loss rate for Go-Back-N and Selective Repeat
""")
    return


# ============================================================
# Part 1: Link Utilization Explorer
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 1: Link Utilization Explorer

Drag the sliders to see how bandwidth, RTT, packet size, and window size affect link utilization.
The key insight: Stop-and-Wait (window = 1) wastes almost all of a high-bandwidth × long-delay link.
The **Bandwidth-Delay Product (BDP)** tells you how many packets must be "in flight" to fill the pipe.
""")
    return


@app.cell
def _(mo):
    bw_slider = mo.ui.slider(1, 10000, value=1000, step=1, label="Bandwidth (Mb/s):", show_value=True)
    rtt_slider = mo.ui.slider(1, 1000, value=100, step=1, label="RTT (ms):", show_value=True)
    pkt_slider = mo.ui.slider(64, 9000, value=1500, step=64, label="Packet size (bytes):", show_value=True)
    win_slider = mo.ui.slider(1, 500, value=1, step=1, label="Window size (packets):", show_value=True)
    mo.vstack([
        mo.hstack([bw_slider, rtt_slider], justify="start"),
        mo.hstack([pkt_slider, win_slider], justify="start"),
    ])
    return bw_slider, pkt_slider, rtt_slider, win_slider


@app.cell
def _(bw_slider, math, mo, mpatches, pkt_slider, plt, rtt_slider, win_slider):
    _bw_bps = bw_slider.value * 1e6          # bits per second
    _rtt_s = rtt_slider.value / 1000.0       # seconds
    _pkt_bytes = pkt_slider.value
    _pkt_bits = _pkt_bytes * 8
    _win = win_slider.value

    # Transmit time for one packet
    _t_tx = _pkt_bits / _bw_bps              # seconds
    _t_tx_us = _t_tx * 1e6                   # microseconds

    # BDP
    _bdp_bits = _bw_bps * _rtt_s
    _bdp_packets = _bdp_bits / _pkt_bits

    # Stop-and-Wait utilization (window=1)
    _u_sw = _t_tx / (_rtt_s + _t_tx)

    # Current window utilization
    _u_win = min(1.0, _win * _t_tx / (_rtt_s + _t_tx))

    # Packets needed to fill pipe
    _n_fill = math.ceil((_rtt_s + _t_tx) / _t_tx)

    # --- Matplotlib bar chart ---
    plt.close("all")
    _fig, _ax = plt.subplots(figsize=(7, 3))

    _labels = ["Stop-and-Wait\n(window = 1)", f"Window = {_win}"]
    _values = [_u_sw * 100, _u_win * 100]
    _colors = ["#5B9BD5", "#ED7D31"]

    _bars = _ax.barh(_labels, _values, color=_colors, height=0.4, edgecolor="black", linewidth=0.7)
    _ax.axvline(100, color="green", linestyle="--", linewidth=1.5, label="100% (full pipe)")
    _ax.set_xlim(0, 115)
    _ax.set_xlabel("Link Utilization (%)")
    _ax.set_title("Link Utilization: Stop-and-Wait vs. Current Window")
    _ax.legend(loc="lower right")

    for _bar, _val in zip(_bars, _values):
        _ax.text(_val + 1.5, _bar.get_y() + _bar.get_height() / 2,
                 f"{_val:.1f}%", va="center", fontsize=10)

    _fig.tight_layout()

    _text = mo.md(f"""
### Results

| Parameter | Value |
|---|---|
| Transmit time (t_tx) | {_t_tx_us:.2f} µs |
| RTT | {rtt_slider.value} ms |
| BDP | {_bdp_bits/1e3:.1f} kbits ≈ **{_bdp_packets:.1f} packets** |
| Stop-and-Wait utilization | **{_u_sw*100:.2f}%** |
| Window = {_win} utilization | **{_u_win*100:.2f}%** |
| **Window needed to fill pipe** | **{_n_fill} packets** |

{"✅ Window already fills the pipe." if _win >= _n_fill else f"⚠ Increase window to **{_n_fill}** packets to reach 100% utilization."}
""")

    mo.vstack([_text, _fig])
    return


# ============================================================
# Part 2: Stop-and-Wait Trace Simulator
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 2: Stop-and-Wait Trace Simulator

Step through a timing (ladder) diagram showing how Stop-and-Wait RDT handles packet loss
and ACK loss. Time flows downward. Diagonal arrows show packets (blue) and ACKs (orange).
""")
    return


@app.cell
def _(mo):
    scenario_select = mo.ui.dropdown(
        {
            "Normal (no loss)": "normal",
            "Data packet lost": "data_lost",
            "ACK lost": "ack_lost",
        },
        value="Normal (no loss)",
        label="Scenario:",
    )
    npkts_slider = mo.ui.slider(2, 8, value=4, step=1, label="Packets to send:", show_value=True)
    mo.hstack([scenario_select, npkts_slider], justify="start")
    return npkts_slider, scenario_select


@app.cell
def _(mo, mpatches, npkts_slider, plt, scenario_select):
    _scenario = scenario_select.value
    _n_pkts = npkts_slider.value

    # Layout constants
    _SENDER_X = 0.1
    _RECV_X = 0.9
    _PROP_DELAY = 0.25      # fraction of a slot consumed by one-way propagation
    _TX_SLOT = 1.0          # y-units per full RTT slot
    _TIMEOUT_EXTRA = 0.5    # additional y-units added when a timeout occurs

    plt.close("all")
    _fig, _ax = plt.subplots(figsize=(8, max(6, _n_pkts * 1.8 + 2)))
    _ax.set_xlim(0, 1)
    _ax.invert_yaxis()
    _ax.axis("off")

    # Draw timeline vertical bars
    _y_max_estimate = _n_pkts * (_TX_SLOT + _TIMEOUT_EXTRA) + 1.5
    _ax.plot([_SENDER_X, _SENDER_X], [0, _y_max_estimate], color="black", lw=2)
    _ax.plot([_RECV_X, _RECV_X], [0, _y_max_estimate], color="black", lw=2)
    _ax.text(_SENDER_X, -0.3, "Sender", ha="center", fontsize=12, fontweight="bold")
    _ax.text(_RECV_X, -0.3, "Receiver", ha="center", fontsize=12, fontweight="bold")

    def _draw_arrow(ax, x0, y0, x1, y1, color, label, linestyle="-", lost=False, lost_label=None):
        """Draw a diagonal arrow with an optional label. If lost=True, stop halfway and mark X."""
        if lost:
            _xm = (x0 + x1) / 2
            _ym = (y0 + y1) / 2
            ax.annotate("", xy=(_xm, _ym), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-", color=color, lw=1.5,
                                        linestyle=linestyle))
            ax.plot(_xm, _ym, "rx", markersize=14, markeredgewidth=2.5)
            if lost_label:
                ax.text(_xm + 0.02, _ym + 0.05, lost_label, color="red", fontsize=9)
        else:
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5,
                                        linestyle=linestyle))
        # Label near midpoint (or near send point if lost)
        _lx = (x0 + x1) / 2 if not lost else (x0 + (x0 + x1) / 2) / 2
        _ly = (y0 + y1) / 2 if not lost else (y0 + (y0 + y1) / 2) / 2
        _ha = "left" if x0 < x1 else "right"
        ax.text(_lx + (0.02 if x0 < x1 else -0.02), _ly - 0.08,
                label, ha=_ha, fontsize=9, color=color)

    def _draw_timeout(ax, x, y_start, y_end, label="timeout"):
        ax.annotate("", xy=(x, y_end), xytext=(x, y_start),
                    arrowprops=dict(arrowstyle="-", color="gray", lw=1.2,
                                    linestyle="dotted"))
        ax.text(x - 0.08, (y_start + y_end) / 2, label,
                ha="right", va="center", fontsize=8, color="gray",
                bbox=dict(boxstyle="round,pad=0.2", fc="lightyellow", ec="gray", lw=0.7))

    _y = 0.0  # current time pointer (top of diagram)

    # Each packet is seq 0 or 1 (alternating bit protocol)
    for _i in range(_n_pkts):
        _seq = _i % 2
        _is_first = (_i == 0)

        _y_send = _y

        if _scenario == "data_lost" and _is_first:
            # First packet is lost midway
            _draw_arrow(_ax, _SENDER_X, _y_send, _RECV_X, _y_send + _PROP_DELAY,
                        color="#5B9BD5", label=f"pkt {_i} [seq={_seq}]",
                        linestyle="--", lost=True, lost_label="lost")
            # Timeout
            _y_timeout = _y_send + _PROP_DELAY + _TIMEOUT_EXTRA
            _draw_timeout(_ax, _SENDER_X, _y_send, _y_timeout)
            _y = _y_timeout
            # Retransmit
            _y_resend = _y
            _draw_arrow(_ax, _SENDER_X, _y_resend, _RECV_X, _y_resend + _PROP_DELAY,
                        color="#5B9BD5", label=f"pkt {_i} [seq={_seq}] (retx)",
                        linestyle="-")
            _y_recv = _y_resend + _PROP_DELAY
            # ACK back
            _y_ack_arrive = _y_recv + _PROP_DELAY
            _draw_arrow(_ax, _RECV_X, _y_recv, _SENDER_X, _y_ack_arrive,
                        color="#ED7D31", label=f"ACK {_seq}")
            _ax.plot(_RECV_X, _y_recv, "go", markersize=7)
            _y = _y_ack_arrive + 0.15

        elif _scenario == "ack_lost" and _is_first:
            # Packet arrives fine; ACK is lost
            _y_recv = _y_send + _PROP_DELAY
            _draw_arrow(_ax, _SENDER_X, _y_send, _RECV_X, _y_recv,
                        color="#5B9BD5", label=f"pkt {_i} [seq={_seq}]")
            _ax.plot(_RECV_X, _y_recv, "go", markersize=7)
            # ACK is lost
            _y_ack_mid = _y_recv + _PROP_DELAY
            _draw_arrow(_ax, _RECV_X, _y_recv, _SENDER_X, _y_recv + _PROP_DELAY * 2,
                        color="#ED7D31", label=f"ACK {_seq}",
                        linestyle="--", lost=True, lost_label="lost")
            # Timeout at sender
            _y_timeout = _y_recv + _PROP_DELAY + _TIMEOUT_EXTRA
            _draw_timeout(_ax, _SENDER_X, _y_send, _y_timeout)
            _y = _y_timeout
            # Retransmit packet
            _y_resend = _y
            _draw_arrow(_ax, _SENDER_X, _y_resend, _RECV_X, _y_resend + _PROP_DELAY,
                        color="#5B9BD5", label=f"pkt {_i} [seq={_seq}] (retx)",
                        linestyle="--")
            _y_recv2 = _y_resend + _PROP_DELAY
            _ax.plot(_RECV_X, _y_recv2, "yo", markersize=7)
            _ax.text(_RECV_X + 0.02, _y_recv2, "dup — discard", fontsize=8, color="goldenrod", va="center")
            # Receiver sends ACK again
            _y_ack2_arrive = _y_recv2 + _PROP_DELAY
            _draw_arrow(_ax, _RECV_X, _y_recv2, _SENDER_X, _y_ack2_arrive,
                        color="#ED7D31", label=f"ACK {_seq} (again)")
            _y = _y_ack2_arrive + 0.15

        else:
            # Normal packet exchange
            _y_recv = _y_send + _PROP_DELAY
            _draw_arrow(_ax, _SENDER_X, _y_send, _RECV_X, _y_recv,
                        color="#5B9BD5", label=f"pkt {_i} [seq={_seq}]")
            _ax.plot(_RECV_X, _y_recv, "go", markersize=7)
            _y_ack_arrive = _y_recv + _PROP_DELAY
            _draw_arrow(_ax, _RECV_X, _y_recv, _SENDER_X, _y_ack_arrive,
                        color="#ED7D31", label=f"ACK {_seq}")
            _y = _y_ack_arrive + 0.15

    # Legend
    _legend_handles = [
        mpatches.Patch(color="#5B9BD5", label="Data packet (→ Receiver)"),
        mpatches.Patch(color="#ED7D31", label="ACK (→ Sender)"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="green",
                   markersize=8, label="Packet received (good)"),
        plt.Line2D([0], [0], marker="x", color="red", markersize=9,
                   markeredgewidth=2, linestyle="none", label="Lost (dropped)"),
    ]
    if _scenario == "ack_lost":
        _legend_handles.append(
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="gold",
                       markersize=8, label="Duplicate — discarded")
        )
    _ax.legend(handles=_legend_handles, loc="lower right", fontsize=9,
               bbox_to_anchor=(1.0, 0.0))

    _ax.set_title(
        f"Stop-and-Wait Timing Diagram — {scenario_select.value} ({_n_pkts} packets)",
        fontsize=12
    )
    _fig.tight_layout()
    _fig
    return


# ============================================================
# Part 3: GBN vs SR Throughput Comparison
# ============================================================

@app.cell
def _(mo):
    mo.md("""
---
## Part 3: GBN vs SR Throughput Comparison

How does effective throughput (normalized to link capacity) degrade with packet loss rate?
Go-Back-N must retransmit the entire window on a loss; Selective Repeat only retransmits the
lost packet. The gap between them grows with window size.

**Formulas used (standard textbook results):**
- Stop-and-Wait: T = 1 − p
- Go-Back-N: T = N(1−p) / (1 + (N−1)p), capped at 1
- Selective Repeat: T = N(1−p), capped at 1
""")
    return


@app.cell
def _(mo):
    gbn_n_slider = mo.ui.slider(1, 64, value=8, step=1, label="Window size N:", show_value=True)
    gbn_n_slider
    return (gbn_n_slider,)


@app.cell
def _(gbn_n_slider, mo, np, plt):
    _N = gbn_n_slider.value
    _p = np.linspace(0, 0.30, 300)

    # Throughput formulas
    _T_sw = 1.0 - _p

    # GBN: N(1-p) / (1 + (N-1)*p), capped at 1
    _denom_gbn = 1.0 + (_N - 1) * _p
    _T_gbn = np.clip(_N * (1.0 - _p) / _denom_gbn, 0.0, 1.0)

    # SR: N*(1-p), capped at 1
    _T_sr = np.clip(_N * (1.0 - _p), 0.0, 1.0)

    # Find where GBN throughput equals SR/2 (qualitative annotation)
    # T_gbn == T_sr/2  =>  N(1-p)/(1+(N-1)p) == N(1-p)/2  =>  1+(N-1)p == 2  =>  p == 1/(N-1)
    _p_crossover = None
    if _N > 1:
        _p_crossover = 1.0 / (_N - 1)

    plt.close("all")
    _fig, _ax = plt.subplots(figsize=(8, 5))

    _ax.plot(_p * 100, _T_sw, color="gray", linestyle="--", linewidth=1.8, label="Stop-and-Wait (N=1)")
    _ax.plot(_p * 100, _T_gbn, color="#5B9BD5", linewidth=2.2, label=f"Go-Back-N (N={_N})")
    _ax.plot(_p * 100, _T_sr, color="#ED7D31", linewidth=2.2, label=f"Selective Repeat (N={_N})")

    _ax.set_xlabel("Loss probability p (%)", fontsize=12)
    _ax.set_ylabel("Normalized throughput", fontsize=12)
    _ax.set_title(f"Throughput vs. Loss Rate (Window N={_N})", fontsize=13)
    _ax.set_xlim(0, 30)
    _ax.set_ylim(0, 1.05)
    _ax.grid(True, alpha=0.35)
    _ax.legend(fontsize=11)

    # Annotation: crossover where GBN = SR/2
    if _p_crossover is not None and 0 < _p_crossover < 0.30:
        _pc_pct = _p_crossover * 100
        _T_at = float(np.clip(_N * (1.0 - _p_crossover) / (1.0 + (_N - 1) * _p_crossover), 0, 1))
        _ax.axvline(_pc_pct, color="red", linestyle=":", linewidth=1.2, alpha=0.7)
        _ax.annotate(
            f"GBN = SR/2\nat p ≈ {_pc_pct:.1f}%",
            xy=(_pc_pct, _T_at),
            xytext=(_pc_pct + 2, _T_at + 0.12),
            fontsize=9, color="red",
            arrowprops=dict(arrowstyle="->", color="red", lw=1.0),
        )

    _fig.tight_layout()

    # Summary text
    _at_10 = float(np.clip(_N * 0.9 / (1.0 + (_N - 1) * 0.1), 0, 1))
    _sr_at_10 = float(np.clip(_N * 0.9, 0, 1))
    _note = mo.md(f"""
**At p = 10% loss:**
- Stop-and-Wait: {(1-0.1)*100:.0f}% throughput
- Go-Back-N (N={_N}): {_at_10*100:.1f}%
- Selective Repeat (N={_N}): {_sr_at_10*100:.1f}%

{"**N=1:** all three protocols are identical — window size has no effect." if _N == 1 else
 f"SR retains {_sr_at_10/_at_10:.1f}× the throughput of GBN at 10% loss."}
""")

    mo.vstack([_fig, _note])
    return


@app.cell
def _(mo):
    mo.md("""
---
*EC 441 — Introduction to Computer Networking, Boston University, Spring 2026*
""")
    return


if __name__ == "__main__":
    app.run()
