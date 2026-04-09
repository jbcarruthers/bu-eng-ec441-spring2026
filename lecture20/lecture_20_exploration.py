import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    return GridSpec, mo, mpatches, np, plt


@app.cell
def _(mo):
    mo.md(
        """
        # Lecture 20: TCP Part 2 — Congestion Control and the Modern Picture
        EC 441 - Introduction to Computer Networking, Boston University, Spring 2026

        Three interactive parts:
        1. **TCP Congestion Control Simulator** — watch cwnd and ssthresh evolve through slow start, congestion avoidance, and loss events
        2. **TCP Throughput Formula** — explore how bandwidth scales with RTT and loss rate; find the loss rate required for a target throughput
        3. **AIMD Fairness** — watch two competing flows converge to equal shares under AIMD
        """
    )


@app.cell
def _(mo):
    mo.md(
        """
        ## Part 1: TCP Congestion Control Simulator

        TCP congestion control operates in two phases:

        - **Slow Start**: cwnd starts at 1 MSS and **doubles** each RTT (exponential growth) until it reaches ssthresh.
        - **Congestion Avoidance**: cwnd increases by +1 MSS per RTT (linear growth).

        On a **loss event**:
        - *3 duplicate ACKs* → Fast Recovery: ssthresh = cwnd/2, cwnd = ssthresh (stay in CA)
        - *Timeout* → ssthresh = cwnd/2, cwnd = 1 (restart Slow Start — more severe)
        """
    )


@app.cell
def _(mo):
    ssthresh_init = mo.ui.slider(4, 24, value=8, step=1, label="Initial ssthresh (MSS)")
    n_rounds = mo.ui.slider(20, 60, value=40, step=5, label="Simulation rounds")
    loss_scenario = mo.ui.dropdown(
        options={
            "3 dup ACKs at round 11": "dup11",
            "Timeout at round 11": "timeout11",
            "3 dup ACKs at round 11, then timeout at round 22": "dup11_timeout22",
            "No loss (pure slow start + CA)": "noloss",
        },
        value="3 dup ACKs at round 11",
        label="Loss scenario",
    )
    mo.vstack([ssthresh_init, n_rounds, loss_scenario])
    return loss_scenario, n_rounds, ssthresh_init


@app.cell
def _(GridSpec, loss_scenario, n_rounds, ssthresh_init, mo, mpatches, plt):
    _scenario = loss_scenario.value
    _n = n_rounds.value
    _ssthresh_start = ssthresh_init.value

    # --- Simulation ---
    _cwnd = [0.0] * (_n + 1)
    _ssthresh = [0.0] * (_n + 1)
    _phase = [""] * (_n + 1)
    _loss_events = []  # list of (round_index, type)

    _cwnd[0] = 1.0
    _ssthresh[0] = float(_ssthresh_start)
    _phase[0] = "SS"

    for _r in range(1, _n + 1):
        _cw = _cwnd[_r - 1]
        _st = _ssthresh[_r - 1]

        # Determine phase and advance cwnd BEFORE applying loss
        if _cw < _st:
            _new_cw = min(_cw * 2, _st)
            _new_phase = "SS" if _new_cw < _st else "CA"
        else:
            _new_cw = _cw + 1.0
            _new_phase = "CA"

        _new_st = _st

        # Apply loss events
        if _scenario == "dup11" and _r == 11:
            _loss_events.append((_r, "3 dup ACKs"))
            _new_st = max(1.0, _new_cw // 2)
            _new_cw = _new_st
            _new_phase = "CA"
        elif _scenario == "timeout11" and _r == 11:
            _loss_events.append((_r, "Timeout"))
            _new_st = max(1.0, _new_cw // 2)
            _new_cw = 1.0
            _new_phase = "SS"
        elif _scenario == "dup11_timeout22":
            if _r == 11:
                _loss_events.append((_r, "3 dup ACKs"))
                _new_st = max(1.0, _new_cw // 2)
                _new_cw = _new_st
                _new_phase = "CA"
            elif _r == 22:
                _loss_events.append((_r, "Timeout"))
                _new_st = max(1.0, _new_cw // 2)
                _new_cw = 1.0
                _new_phase = "SS"

        _cwnd[_r] = _new_cw
        _ssthresh[_r] = _new_st
        _phase[_r] = _new_phase

    _rounds = list(range(_n + 1))

    # --- Plot ---
    _fig = plt.figure(figsize=(10, 5))
    _gs = GridSpec(2, 1, figure=_fig, height_ratios=[4, 1], hspace=0.35)

    _ax1 = _fig.add_subplot(_gs[0])
    _ax2 = _fig.add_subplot(_gs[1])

    # Shade SS / CA regions on top panel
    _i = 0
    while _i <= _n:
        _j = _i
        _ph = _phase[_i]
        while _j <= _n and _phase[_j] == _ph:
            _j += 1
        _color = "#d0e8ff" if _ph == "SS" else "#ffe8c0"
        _ax1.axvspan(_i - 0.5, _j - 0.5, color=_color, alpha=0.5, zorder=0)
        _i = _j

    # cwnd line
    _ax1.plot(_rounds, _cwnd, "b-o", markersize=4, linewidth=1.8, label="cwnd (MSS)", zorder=3)
    # ssthresh step line
    _ax1.step(_rounds, _ssthresh, where="post", color="orange", linestyle="--",
              linewidth=1.5, label="ssthresh (MSS)", zorder=2)

    # Loss event markers
    for _lr, _ltype in _loss_events:
        _ax1.axvline(_lr, color="red", linestyle=":", linewidth=1.5, zorder=4)
        _ax1.text(_lr + 0.3, max(_cwnd) * 0.92, _ltype, color="red", fontsize=8,
                  rotation=90, va="top")

    _ax1.set_xlabel("Round (RTT)", fontsize=10)
    _ax1.set_ylabel("Window size (MSS)", fontsize=10)
    _ax1.set_title("TCP Congestion Window Evolution", fontsize=11)
    _ax1.legend(fontsize=9, loc="upper left")
    _ax1.set_xlim(-0.5, _n + 0.5)
    _ax1.grid(True, alpha=0.3)

    # Add legend patches for shading
    _ss_patch = mpatches.Patch(color="#d0e8ff", alpha=0.7, label="Slow Start")
    _ca_patch = mpatches.Patch(color="#ffe8c0", alpha=0.7, label="Congestion Avoidance")
    _ax1.legend(handles=[_ax1.get_lines()[0], _ax1.get_lines()[1], _ss_patch, _ca_patch],
                fontsize=9, loc="upper left")

    # Phase bar (bottom panel)
    _bar_colors = ["#4a90d9" if _p == "SS" else "#e8960c" for _p in _phase]
    for _ri, _bc in enumerate(_bar_colors):
        _ax2.bar(_ri, 1, color=_bc, width=1.0, align="center")

    _ax2.set_xlim(-0.5, _n + 0.5)
    _ax2.set_ylim(0, 1)
    _ax2.set_yticks([])
    _ax2.set_xlabel("Round (RTT)", fontsize=10)
    _ax2.set_title("Phase", fontsize=10)
    _ss_bar = mpatches.Patch(color="#4a90d9", label="Slow Start")
    _ca_bar = mpatches.Patch(color="#e8960c", label="Congestion Avoidance")
    _ax2.legend(handles=[_ss_bar, _ca_bar], fontsize=8, loc="upper right")

    plt.tight_layout()
    _out_fig = plt.gcf()
    plt.close()

    mo.vstack([mo.md("### Congestion Window Evolution"), _out_fig])


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part 2: TCP Throughput Formula

        The approximate TCP throughput formula (Mathis et al.) is:

        $$\text{BW} \approx \frac{\text{MSS}}{\text{RTT}} \cdot \frac{1}{\sqrt{p}}$$

        Key insights:
        - Throughput is **inversely proportional to RTT** — long fat pipes are hard to fill.
        - Throughput falls as **1/√p** with loss rate — even a small loss rate severely limits throughput.
        - High-speed, long-RTT paths (e.g., trans-oceanic 10 Gb/s links) require **extremely** low loss rates (p ~ 10⁻⁹ or better).
        """
    )


@app.cell
def _(mo):
    mss_bytes = mo.ui.slider(512, 9000, value=1460, step=128, label="MSS (bytes)")
    rtt_ms = mo.ui.slider(1, 500, value=100, step=1, label="RTT (ms)")
    target_bw_mbps = mo.ui.slider(10, 10000, value=1000, step=10, label="Target BW (Mb/s)")
    mo.vstack([mss_bytes, rtt_ms, target_bw_mbps])
    return mss_bytes, rtt_ms, target_bw_mbps


@app.cell
def _(mss_bytes, rtt_ms, target_bw_mbps, mo, np, plt):
    _mss = mss_bytes.value
    _rtt = rtt_ms.value
    _target = target_bw_mbps.value

    _p_range = np.logspace(-6, -1, 400)
    _rtt_range = np.linspace(1, 500, 400)  # ms

    def _bw_mbps(mss_b, rtt_s, p):
        return (mss_b * 8.0 / rtt_s) * (1.0 / np.sqrt(p)) / 1e6

    # Left panel: BW vs p for three RTTs
    _rtts_left = [10, _rtt, 500]
    _rtt_labels = [f"RTT = 10 ms", f"RTT = {_rtt} ms (slider)", "RTT = 500 ms"]
    _colors_left = ["#2196F3", "#FF5722", "#9C27B0"]

    # Right panel: BW vs RTT for three loss rates
    _ps_right = [1e-5, 1e-4, 1e-3]
    _p_labels = ["p = 10⁻⁵", "p = 10⁻⁴", "p = 10⁻³"]
    _colors_right = ["#4CAF50", "#FF9800", "#F44336"]

    _fig2, (_axL, _axR) = plt.subplots(1, 2, figsize=(11, 4))

    # Left panel
    for _rtt_v, _lab, _col in zip(_rtts_left, _rtt_labels, _colors_left):
        _bw_v = _bw_mbps(_mss, _rtt_v / 1000.0, _p_range)
        _axL.loglog(_p_range, _bw_v, color=_col, linewidth=1.8, label=_lab)

    # Required p for target BW at slider RTT
    # BW = (MSS*8 / RTT) / sqrt(p)  =>  sqrt(p) = MSS*8 / (RTT * BW)  =>  p = (MSS*8 / (RTT * BW))^2
    _bw_target_bps = _target * 1e6
    _rtt_s = _rtt / 1000.0
    _req_p = (_mss * 8.0 / (_rtt_s * _bw_target_bps)) ** 2
    _req_p_clipped = float(np.clip(_req_p, _p_range[0], _p_range[-1]))
    _axL.axvline(_req_p_clipped, color="black", linestyle="--", linewidth=1.5,
                 label=f"Required p for {_target} Mb/s\n(p = {_req_p:.2e})")
    _axL.set_xlabel("Loss rate p", fontsize=10)
    _axL.set_ylabel("Throughput (Mb/s)", fontsize=10)
    _axL.set_title("BW vs. Loss Rate", fontsize=11)
    _axL.legend(fontsize=8)
    _axL.grid(True, which="both", alpha=0.3)
    _axL.set_xlim(_p_range[0], _p_range[-1])

    # Right panel
    for _p_v, _lab, _col in zip(_ps_right, _p_labels, _colors_right):
        _bw_v2 = _bw_mbps(_mss, _rtt_range / 1000.0, _p_v)
        _axR.plot(_rtt_range, _bw_v2, color=_col, linewidth=1.8, label=_lab)

    _axR.set_xlabel("RTT (ms)", fontsize=10)
    _axR.set_ylabel("Throughput (Mb/s)", fontsize=10)
    _axR.set_title("BW vs. RTT", fontsize=11)
    _axR.legend(fontsize=9)
    _axR.grid(True, alpha=0.3)
    _axR.set_yscale("log")

    plt.tight_layout()
    _out_fig2 = plt.gcf()
    plt.close()

    # Summary stats
    _bw_at_001 = _bw_mbps(_mss, _rtt_s, 0.0001)  # p = 0.01%
    _bdp_bits = _bw_target_bps * _rtt_s
    _bdp_kb = _bdp_bits / 8.0 / 1024.0
    _bdp_mb = _bdp_kb / 1024.0
    _bdp_str = f"{_bdp_mb:.2f} MB" if _bdp_mb >= 0.1 else f"{_bdp_kb:.1f} KB"

    _stats_md = mo.md(
        f"""
        **Summary (MSS = {_mss} bytes, RTT = {_rtt} ms):**
        - BW at p = 0.01%: **{_bw_at_001:.1f} Mb/s**
        - Required p for {_target} Mb/s target: **p = {_req_p:.2e}** {"⚠️ out of plot range" if _req_p < _p_range[0] or _req_p > _p_range[-1] else ""}
        - Bandwidth-delay product at target BW: **{_bdp_str}** (= window size needed to fill the pipe)
        """
    )

    mo.vstack([_out_fig2, _stats_md])


@app.cell
def _(mo):
    mo.md(
        """
        ## Part 3: AIMD Fairness Simulator

        **Additive Increase, Multiplicative Decrease (AIMD)**:
        - Each RTT with no loss: each flow's rate increases by +Δ (additive increase).
        - When total rate exceeds link capacity C: both flows halve (multiplicative decrease).

        Two flows starting from different initial rates converge to **equal shares** (x₁ = x₂ = C/2).
        The phase-space diagram shows why: the AIMD trajectory is always driven toward the
        intersection of the **efficiency line** (x₁ + x₂ = C) and the **fairness line** (x₁ = x₂).
        """
    )


@app.cell
def _(mo):
    capacity = mo.ui.slider(10, 100, value=100, step=10, label="Link capacity C (Mb/s)")
    x1_init = mo.ui.slider(1, 80, value=10, step=1, label="Flow 1 initial rate (Mb/s)")
    x2_init = mo.ui.slider(1, 80, value=70, step=1, label="Flow 2 initial rate (Mb/s)")
    delta = mo.ui.slider(1, 10, value=5, step=1, label="Additive increase Δ (Mb/s)")
    n_steps = mo.ui.slider(10, 100, value=40, step=5, label="Number of AIMD steps")
    mo.vstack([capacity, mo.hstack([x1_init, x2_init]), mo.hstack([delta, n_steps])])
    return capacity, delta, n_steps, x1_init, x2_init


@app.cell
def _(capacity, delta, n_steps, x1_init, x2_init, mo, np, plt):
    _C = capacity.value
    _x1 = float(x1_init.value)
    _x2 = float(x2_init.value)
    _d = float(delta.value)
    _n = n_steps.value

    # Simulate AIMD
    _traj_x1 = [_x1]
    _traj_x2 = [_x2]
    for _s in range(_n):
        _x1 += _d
        _x2 += _d
        if _x1 + _x2 > _C:
            _x1 /= 2.0
            _x2 /= 2.0
        _traj_x1.append(_x1)
        _traj_x2.append(_x2)

    _tx1 = np.array(_traj_x1)
    _tx2 = np.array(_traj_x2)
    _steps_arr = np.arange(_n + 1)

    _fig3, (_axP, _axT) = plt.subplots(1, 2, figsize=(11, 5))

    # --- Left: Phase space ---
    _lim = _C + 5
    _axP.set_xlim(0, _lim)
    _axP.set_ylim(0, _lim)

    # Efficiency line x1+x2 = C
    _ev = np.linspace(0, _C, 100)
    _axP.plot(_ev, _C - _ev, color="gray", linewidth=1.5, label=f"x₁+x₂ = {_C} (efficiency)")
    # Fairness line x1=x2
    _axP.plot([0, _lim], [0, _lim], color="gray", linestyle="--", linewidth=1.5,
              label="x₁ = x₂ (fairness)")
    # Ideal point
    _axP.plot(_C / 2, _C / 2, "k*", markersize=12, zorder=5, label=f"Ideal ({_C/2:.0f}, {_C/2:.0f})")

    # Trajectory with color gradient
    _cmap = plt.cm.Blues
    _norm_vals = _steps_arr / max(_steps_arr[-1], 1)
    for _i in range(len(_tx1) - 1):
        _col = _cmap(0.25 + 0.75 * _norm_vals[_i])
        _axP.annotate("", xy=(_tx1[_i + 1], _tx2[_i + 1]),
                      xytext=(_tx1[_i], _tx2[_i]),
                      arrowprops=dict(arrowstyle="->", color=_col, lw=1.2))

    _axP.scatter(_tx1, _tx2, c=_norm_vals, cmap="Blues", s=20, vmin=0, vmax=1, zorder=4)
    # Start and end markers
    _axP.plot(_tx1[0], _tx2[0], "go", markersize=10, zorder=6, label="Start")
    _axP.plot(_tx1[-1], _tx2[-1], "r*", markersize=12, zorder=6, label="Current position")

    _axP.set_xlabel("Flow 1 rate (Mb/s)", fontsize=10)
    _axP.set_ylabel("Flow 2 rate (Mb/s)", fontsize=10)
    _axP.set_title("AIMD Phase Space", fontsize=11)
    _axP.legend(fontsize=8, loc="upper right")
    _axP.grid(True, alpha=0.3)
    _axP.set_aspect("equal")

    # --- Right: Time series ---
    _axT.plot(_steps_arr, _tx1, color="#2196F3", linewidth=1.8, label="Flow 1")
    _axT.plot(_steps_arr, _tx2, color="#FF5722", linewidth=1.8, label="Flow 2")
    _axT.axhline(_C / 2, color="black", linestyle="--", linewidth=1.2,
                 label=f"Ideal C/2 = {_C/2:.0f} Mb/s")
    # Stacked area: total utilization
    _total = _tx1 + _tx2
    _axT.fill_between(_steps_arr, 0, np.minimum(_total, _C), alpha=0.12, color="green",
                      label="Utilized capacity")
    _axT.axhline(_C, color="green", linestyle=":", linewidth=1.2, label=f"Capacity C = {_C} Mb/s")
    _axT.set_xlabel("Step", fontsize=10)
    _axT.set_ylabel("Rate (Mb/s)", fontsize=10)
    _axT.set_title("Flow Rates Over Time", fontsize=11)
    _axT.legend(fontsize=8, loc="upper right")
    _axT.grid(True, alpha=0.3)
    _axT.set_ylim(0, _C * 1.15)

    plt.tight_layout()
    _out_fig3 = plt.gcf()
    plt.close()

    _summary_md = mo.md(
        f"After **{_n} steps**: x₁ = **{_x1:.1f} Mb/s**, x₂ = **{_x2:.1f} Mb/s** | "
        f"|x₁ − x₂| = **{abs(_x1 - _x2):.1f} Mb/s** (fairness gap) | "
        f"total = **{_x1 + _x2:.1f}/{_C} Mb/s**"
    )

    mo.vstack([_out_fig3, _summary_md])


if __name__ == "__main__":
    app.run()
