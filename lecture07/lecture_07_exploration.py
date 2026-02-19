import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from scipy import special
    return mo, mpatches, np, plt, special


@app.cell
def _(mo):
    mo.md(r"""
    # Lecture 7: Multiple Access Protocols — Interactive Exploration

    **EC 441 - Introduction to Computer Networking**

    This notebook explores MAC protocol concepts interactively:

    1. **ALOHA Throughput** — S vs. G curves, operating point breakdown
    2. **CSMA/CD Efficiency** — how the ratio $a = \tau/T$ controls performance
    3. **Ethernet Minimum Frame Size** — the $L \ge 2\tau R$ constraint
    4. **Collision Space–Time Diagram** — interactive parallelogram view
    5. **Collision BER Simulator** — frame error rate as a function of timing and overlap
    """)
    return


# ─────────────────────────────────────────────────────────────────────────────
# PART 1: ALOHA THROUGHPUT
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part 1: ALOHA Throughput

    For Poisson-distributed transmission attempts with offered load $G$ (attempts per frame-time $T$):

    $$S_{\text{pure}} = G e^{-2G} \qquad \text{(collision window } 2T\text{)}$$

    $$S_{\text{slotted}} = G e^{-G} \qquad \text{(collision window } T\text{)}$$

    Move the slider to explore how the operating point and slot-outcome breakdown change with $G$.
    """)
    return


@app.cell
def _(mo):
    aloha_g = mo.ui.slider(
        start=0.05, stop=2.5, step=0.05, value=1.0,
        label="Offered load G (attempts per frame-time):", show_value=True
    )
    aloha_g
    return (aloha_g,)


@app.cell
def _(aloha_g, mo, np, plt):
    _G_range = np.linspace(0.001, 2.5, 600)
    _S_pure    = _G_range * np.exp(-2 * _G_range)
    _S_slotted = _G_range * np.exp(-_G_range)

    _g = aloha_g.value
    _s_pure_pt    = _g * np.exp(-2 * _g)
    _s_slotted_pt = _g * np.exp(-_g)

    # Slot-outcome breakdown for slotted ALOHA (Poisson)
    _p1 = _g * np.exp(-_g)           # P(exactly 1 attempt) = success
    _p0 = np.exp(-_g)                 # P(0 attempts)        = empty
    _p2p = max(0.0, 1 - _p0 - _p1)   # P(2+ attempts)       = collision

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: throughput curves
    _ax1.plot(_G_range, _S_slotted, color='#3a86ff', linewidth=2.5,
              label=f'Slotted  (max {1/np.e:.3f} at G=1)')
    _ax1.plot(_G_range, _S_pure,    color='#ff6b6b', linewidth=2.5,
              label=f'Pure     (max {1/(2*np.e):.3f} at G=½)')
    _ax1.axhline(1/np.e,     color='#3a86ff', linestyle=':', alpha=0.45, linewidth=1)
    _ax1.axhline(1/(2*np.e), color='#ff6b6b', linestyle=':', alpha=0.45, linewidth=1)
    _ax1.axvline(_g, color='#2d6a4f', linestyle='--', alpha=0.6, linewidth=1.4,
                 label=f'G = {_g:.2f}')
    _ax1.plot(_g, _s_slotted_pt, 'o', color='#3a86ff', markersize=10, zorder=5)
    _ax1.plot(_g, _s_pure_pt,    'o', color='#ff6b6b', markersize=10, zorder=5)
    _ax1.text(1.02, 1/np.e + 0.008,     f'1/e ≈ {1/np.e:.3f}',
              color='#3a86ff', fontsize=8.5)
    _ax1.text(0.52, 1/(2*np.e) + 0.008, f'1/2e ≈ {1/(2*np.e):.3f}',
              color='#ff6b6b', fontsize=8.5)
    _ax1.set_xlabel('Offered Load $G$', fontsize=11)
    _ax1.set_ylabel('Throughput $S$', fontsize=11)
    _ax1.set_title('ALOHA Throughput vs. Offered Load', fontsize=12, fontweight='bold')
    _ax1.legend(fontsize=9.5)
    _ax1.set_xlim(0, 2.5); _ax1.set_ylim(0, 0.42)
    _ax1.grid(alpha=0.3)

    # Right: pie chart — slotted ALOHA slot outcomes
    _labels_pie  = [f'Success\n{100*_p1:.1f}%',
                    f'Empty\n{100*_p0:.1f}%',
                    f'Collision\n{100*_p2p:.1f}%']
    _sizes_pie   = [_p1, _p0, _p2p]
    _colors_pie  = ['#3a86ff', '#adb5bd', '#ff6b6b']
    _ax2.pie(_sizes_pie, labels=_labels_pie, colors=_colors_pie,
             explode=(0.04, 0.04, 0.04),
             autopct='', startangle=90, textprops={'fontsize': 11})
    _ax2.set_title(f'Slotted ALOHA slot outcomes  (G = {_g:.2f})',
                   fontsize=12, fontweight='bold')

    plt.tight_layout()

    _result = mo.vstack([
        mo.md(f"""
**At G = {_g:.2f}:**
| | Slotted ALOHA | Pure ALOHA |
|---|---|---|
| Throughput $S$ | **{_s_slotted_pt:.4f}** ({100*_s_slotted_pt:.1f}%) | **{_s_pure_pt:.4f}** ({100*_s_pure_pt:.1f}%) |
| Formula | $Ge^{{-G}}$ | $Ge^{{-2G}}$ |

**Slotted ALOHA slot breakdown (Poisson model):**
$P(\\text{{success}}) = Ge^{{-G}} = {_p1:.4f}$ — $P(\\text{{empty}}) = e^{{-G}} = {_p0:.4f}$ — $P(\\text{{collision}}) = {_p2p:.4f}$

At peak efficiency ($G=1$): ≈ 37% success / 37% empty / 26% collision.
        """),
        _fig
    ])
    _result
    return


# ─────────────────────────────────────────────────────────────────────────────
# PART 2: CSMA/CD EFFICIENCY
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part 2: CSMA/CD Efficiency

    CSMA/CD efficiency depends on the ratio $a = \tau / T$, where $\tau$ is the
    one-way propagation delay and $T = L/R$ is the frame transmission time.

    $$\eta = \frac{1}{1 + 5a}$$

    As $a \to 0$ (short network or long frames) $\eta \to 1$.
    As $a \to \infty$ (large network or tiny frames) $\eta \to 0$.

    Use the sliders below to explore this relationship with physical parameters.
    """)
    return


@app.cell
def _(mo):
    csma_L = mo.ui.slider(
        start=64, stop=12000, step=64, value=1500,
        label="Frame size L (bytes):", show_value=True
    )
    csma_R = mo.ui.slider(
        start=1, stop=1000, step=1, value=100,
        label="Data rate R (Mb/s):", show_value=True
    )
    csma_d = mo.ui.slider(
        start=10, stop=2500, step=10, value=500,
        label="Segment length d (m):", show_value=True
    )
    mo.vstack([csma_L, csma_R, csma_d])
    return csma_L, csma_R, csma_d


@app.cell
def _(csma_L, csma_R, csma_d, mo, np, plt):
    _L  = csma_L.value * 8          # bits
    _R  = csma_R.value * 1e6        # bits/s
    _d  = csma_d.value              # metres
    _v  = 2e8                       # propagation speed (m/s)
    _tau = _d / _v                  # one-way delay (s)
    _T   = _L / _R                  # frame time (s)
    _a   = _tau / _T

    _eta = 1 / (1 + 5 * _a)

    # Sweep over a
    _a_range = np.logspace(-3, 1, 400)
    _eta_range = 1 / (1 + 5 * _a_range)

    # Also ALOHA reference
    _S_slotted_ref = np.full_like(_a_range, 1/np.e)
    _S_pure_ref    = np.full_like(_a_range, 1/(2*np.e))

    _fig, (_axL, _axR) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: η vs. a on log scale
    _axL.semilogx(_a_range, _eta_range, color='#2d6a4f', linewidth=2.5,
                  label=r'CSMA/CD  $\eta = 1/(1+5a)$')
    _axL.axhline(1/np.e,     color='#3a86ff', linestyle='--', alpha=0.6,
                 linewidth=1.5, label=f'Slotted ALOHA max (1/e ≈ {1/np.e:.2f})')
    _axL.axhline(1/(2*np.e), color='#ff6b6b', linestyle='--', alpha=0.6,
                 linewidth=1.5, label=f'Pure ALOHA max (1/2e ≈ {1/(2*np.e):.2f})')
    _axL.axvline(_a, color='#e76f51', linestyle=':', linewidth=2,
                 label=f'Current a = {_a:.4f}')
    _axL.plot(_a, _eta, 'o', color='#e76f51', markersize=11, zorder=5)
    _axL.set_xlabel(r'$a = \tau / T$  (log scale)', fontsize=11)
    _axL.set_ylabel(r'Efficiency $\eta$', fontsize=11)
    _axL.set_title('CSMA/CD Efficiency vs. $a$', fontsize=12, fontweight='bold')
    _axL.set_xlim(1e-3, 10); _axL.set_ylim(0, 1.05)
    _axL.legend(fontsize=9)
    _axL.grid(alpha=0.3, which='both')

    # Right: efficiency vs. data rate for several segment lengths
    _R_range_mbs = np.logspace(0, 4, 300)   # 1 Mb/s to 10 Gb/s
    _T_of_R = (_L / (_R_range_mbs * 1e6))
    _seg_lengths = [100, 500, 1000, 2500]
    _seg_colors  = ['#3a86ff', '#2d6a4f', '#e76f51', '#9d4edd']
    for _dl, _col in zip(_seg_lengths, _seg_colors):
        _tau_dl = _dl / _v
        _a_dl   = _tau_dl / _T_of_R
        _eta_dl = 1 / (1 + 5 * _a_dl)
        _axR.semilogx(_R_range_mbs, _eta_dl, color=_col, linewidth=2,
                      label=f'd = {_dl} m')
    _axR.axvline(csma_R.value, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
    _axR.axhline(_eta, color='#e76f51', linestyle=':', linewidth=1.5, alpha=0.7)
    _axR.set_xlabel('Data Rate R (Mb/s, log scale)', fontsize=11)
    _axR.set_ylabel(r'Efficiency $\eta$', fontsize=11)
    _axR.set_title(f'Efficiency vs. Rate  (L = {csma_L.value} bytes)', fontsize=12,
                   fontweight='bold')
    _axR.set_xlim(1, 1e4); _axR.set_ylim(0, 1.05)
    _axR.legend(fontsize=9)
    _axR.grid(alpha=0.3, which='both')

    plt.tight_layout()

    _result = mo.vstack([
        mo.md(f"""
**Current parameters:**
$L = {csma_L.value}$ bytes = {_L:.0f} bits — $R = {csma_R.value}$ Mb/s — $d = {_d:.0f}$ m

$\\tau = {_tau*1e6:.2f}\\,\\mu\\text{{s}}$ — $T = {_T*1e6:.2f}\\,\\mu\\text{{s}}$ — $a = \\tau/T = {_a:.5f}$

**CSMA/CD efficiency: $\\eta = 1/(1+5a) =$ {_eta:.4f} ({100*_eta:.1f}%)**

{"⚠️ Low efficiency — try longer frames or a shorter segment." if _eta < 0.7 else "✓ Good efficiency." if _eta > 0.9 else "Moderate efficiency."}
        """),
        _fig
    ])
    _result
    return


# ─────────────────────────────────────────────────────────────────────────────
# PART 3: ETHERNET MINIMUM FRAME SIZE
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part 3: Ethernet Minimum Frame Size

    For CSMA/CD collision detection to work, a transmitting node must still be
    sending when the collision echo returns. This requires:

    $$T \ge 2\tau \quad\Longrightarrow\quad L \ge 2\tau R$$

    Vary the data rate and segment length below. The required minimum frame size
    updates in real time — and you can see why **64 bytes** was chosen for
    10 Mb/s Ethernet over a 2500 m segment.
    """)
    return


@app.cell
def _(mo):
    eth_R = mo.ui.slider(
        start=1, stop=10000, step=1, value=10,
        label="Data rate R (Mb/s):", show_value=True
    )
    eth_d = mo.ui.slider(
        start=10, stop=5000, step=10, value=2500,
        label="Max segment length d (m):", show_value=True
    )
    eth_v = mo.ui.slider(
        start=100, stop=300, step=5, value=200,
        label="Propagation speed v (×10⁶ m/s):", show_value=True
    )
    mo.vstack([eth_R, eth_d, eth_v])
    return eth_R, eth_d, eth_v


@app.cell
def _(eth_R, eth_d, eth_v, mo, np, plt):
    _R  = eth_R.value * 1e6      # bits/s
    _d  = eth_d.value            # m
    _v  = eth_v.value * 1e6      # m/s
    _tau = _d / _v               # one-way delay (s)
    _L_min_bits  = 2 * _tau * _R
    _L_min_bytes = _L_min_bits / 8

    # Sweep: L_min vs data rate for several segment lengths
    _R_sweep = np.logspace(0, 4, 400) * 1e6   # 1 Mb/s to 10 Gb/s
    _seg_choices = [100, 500, 1000, 2500]
    _seg_colors  = ['#3a86ff', '#2d6a4f', '#e76f51', '#9d4edd']

    _fig, (_axL, _axR) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: L_min (bytes) vs R (Mb/s) for several d
    for _di, _ci in zip(_seg_choices, _seg_colors):
        _tau_i   = _di / (_v)
        _Lmin_i  = 2 * _tau_i * _R_sweep / 8   # bytes
        _axL.loglog(_R_sweep / 1e6, _Lmin_i, color=_ci, linewidth=2,
                    label=f'd = {_di} m')

    _axL.axhline(64, color='gray', linestyle='--', linewidth=1.5, alpha=0.7,
                 label='64 bytes (classic Ethernet)')
    _axL.axvline(eth_R.value, color='#023e8a', linestyle=':', linewidth=1.5, alpha=0.7)
    _axL.plot(eth_R.value, _L_min_bytes, 'o', color='#023e8a', markersize=12, zorder=5,
              label=f'Current: {_L_min_bytes:.1f} bytes')
    _axL.set_xlabel('Data Rate R (Mb/s)', fontsize=11)
    _axL.set_ylabel('Minimum Frame Size $L_{\\min}$ (bytes)', fontsize=11)
    _axL.set_title('Ethernet Minimum Frame Size', fontsize=12, fontweight='bold')
    _axL.set_xlim(1, 1e4); _axL.set_ylim(1, 1e7)
    _axL.legend(fontsize=9)
    _axL.grid(alpha=0.3, which='both')

    # Right: Gantt-style round-trip timing diagram
    _T_min   = _L_min_bits / _R     # minimum frame time = 2*tau
    _tau_us  = _tau * 1e6
    _T_us    = _T_min * 1e6         # = 2 * tau_us by definition

    _row_tx = 2.5   # "A transmitting" row y-centre
    _row_ab = 1.5   # "Signal A→B"    row y-centre
    _row_ba = 0.5   # "Echo B→A"      row y-centre
    _bar_h  = 0.5

    # Row 1: A's frame spans full T_min = 2τ
    _axR.barh(_row_tx, _T_us, height=_bar_h, left=0,
              color='#3a86ff', alpha=0.75, edgecolor='#023e8a', linewidth=1.5,
              label="A's frame  (T = 2τ)")

    # Row 2: outbound signal A→B (0 → τ)
    _axR.barh(_row_ab, _tau_us, height=_bar_h, left=0,
              color='#2d6a4f', alpha=0.70, edgecolor='#1b4332', linewidth=1.5,
              label='Signal A→B  (τ)')

    # Row 3: collision echo B→A (τ → 2τ)
    _axR.barh(_row_ba, _tau_us, height=_bar_h, left=_tau_us,
              color='#e76f51', alpha=0.75, edgecolor='#9d0208', linewidth=1.5,
              label='Echo B→A  (τ)')

    # Vertical event lines + top labels
    for _t_ev, _lbl, _col in [
        (0,          f't = 0\nA starts\ntransmitting',      '#023e8a'),
        (_tau_us,    f't = τ = {_tau_us:.1f} µs\nCollision at B', '#2d6a4f'),
        (2*_tau_us,  f't = 2τ = {2*_tau_us:.1f} µs\nEcho arrives\nat A', '#e76f51'),
    ]:
        _axR.axvline(_t_ev, color=_col, linestyle='--', linewidth=1.4, alpha=0.6, zorder=1)
        _axR.text(_t_ev, 3.28, _lbl, ha='center', va='bottom', fontsize=7.5, color=_col)

    # Diamond marker at the critical moment: echo arrives exactly as A finishes its last bit
    _axR.plot(2*_tau_us, _row_tx, 'D', color='#e76f51', markersize=9, zorder=5)
    _axR.annotate('A must still be\ntransmitting here!',
                  xy=(2*_tau_us, _row_tx),
                  xytext=(2*_tau_us + _tau_us * 0.7, _row_tx + 0.65),
                  fontsize=8, color='#e76f51', ha='center',
                  arrowprops=dict(arrowstyle='->', color='#e76f51', lw=1.0))

    # Double-arrow showing T_min = 2τ beneath the rows
    _axR.annotate('', xy=(2*_tau_us, -0.12), xytext=(0, -0.12),
                  arrowprops=dict(arrowstyle='<->', color='#023e8a', lw=1.8))
    _axR.text(_tau_us, -0.38,
              f'$T_{{\\min}} = 2\\tau = {_T_us:.1f}$ µs',
              ha='center', va='top', fontsize=9, color='#023e8a', fontweight='bold')

    _axR.set_yticks([_row_ba, _row_ab, _row_tx])
    _axR.set_yticklabels(['Echo B→A', 'Signal A→B', 'A transmitting'], fontsize=9)
    _axR.set_xlabel('Time (µs)', fontsize=11)
    _axR.set_title('Round-Trip Timing Constraint\n'
                   r'$T \geq 2\tau$: A must detect collision while still transmitting',
                   fontsize=11, fontweight='bold')
    _axR.set_xlim(-_tau_us * 0.02, _T_us * 1.6)
    _axR.set_ylim(-0.65, 4.1)
    _axR.legend(fontsize=8.5, loc='lower right')
    _axR.grid(alpha=0.2, axis='x')

    plt.tight_layout()

    _flag = ""
    if _L_min_bytes < 64:
        _flag = "✓ Fits within standard 64-byte minimum."
    elif _L_min_bytes == 64:
        _flag = "✓ Exactly the classic Ethernet minimum."
    else:
        _flag = f"⚠️ Requires **{_L_min_bytes:.0f} bytes** — larger than the 64-byte standard minimum."

    _result = mo.vstack([
        mo.md(f"""
**Parameters:**  $R = {eth_R.value}$ Mb/s — $d = {_d:.0f}$ m — $v = {eth_v.value} \\times 10^6$ m/s

| Quantity | Value |
|---|---|
| One-way propagation delay $\\tau = d/v$ | **{_tau*1e6:.2f} µs** |
| Round-trip delay $2\\tau$ | **{2*_tau*1e6:.2f} µs** |
| Minimum frame size $L_{{\\min}} = 2\\tau R$ | **{_L_min_bits:.0f} bits = {_L_min_bytes:.1f} bytes** |
| Rounded up to whole byte | **{int(np.ceil(_L_min_bytes))} bytes** |

{_flag}

*Classic Ethernet: 10 Mb/s, 2500 m, v = 2×10⁸ m/s → τ ≈ 12.5 µs (with system margins, 25 µs) → L_min = 64 bytes.*
        """),
        _fig
    ])
    _result
    return


# ─────────────────────────────────────────────────────────────────────────────
# PART 4: COLLISION SPACE–TIME DIAGRAM
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part 4: Collision Space–Time Diagram

    In a space–time diagram (position on x-axis, time increasing downward),
    a transmitted frame propagates as a **parallelogram**.

    - **Node A** starts at $t = 0$.
    - **Node B** starts at $t = t_B$, where $t_B < \tau$ means B senses the channel idle
      (A's signal has not yet arrived).

    The overlap of the two parallelograms is the collision zone.
    With CSMA/CD, A detects the collision when B's signal arrives (at $t \approx t_B + \tau$)
    and aborts immediately.
    """)
    return


@app.cell
def _(mo):
    coll_tau = mo.ui.slider(
        start=0.2, stop=2.0, step=0.1, value=1.0,
        label="Propagation delay τ (normalized):", show_value=True
    )
    coll_T = mo.ui.slider(
        start=2.0, stop=8.0, step=0.5, value=4.0,
        label="Frame duration T (normalized):", show_value=True
    )
    coll_tB = mo.ui.slider(
        start=0.0, stop=3.0, step=0.05, value=0.85,
        label="B start time t_B (normalized):", show_value=True
    )
    coll_cd = mo.ui.checkbox(value=True, label="Show CSMA/CD abort (A detects & aborts at t_B + τ)")
    mo.vstack([coll_tau, coll_T, coll_tB, coll_cd])
    return coll_T, coll_cd, coll_tau, coll_tB


@app.cell
def _(coll_T, coll_cd, coll_tau, coll_tB, mo, mpatches, np, plt):
    _tau = coll_tau.value
    _T   = coll_T.value
    _tB  = coll_tB.value
    _cd  = coll_cd.value

    # A aborts (with CD) when B's signal reaches A: at t = tB + tau
    _t_abort = _tB + _tau   # A's abort time with CD
    _T_eff   = min(_T, _t_abort) if _cd else _T  # effective A transmission duration

    # Node positions
    _xA, _xB = 0.0, 1.0

    # A's parallelogram (transmits from 0 to T_eff at xA; leading edge reaches xB at tau)
    _A_verts = [(_xA, 0), (_xB, _tau), (_xB, _T_eff + _tau), (_xA, _T_eff)]

    # B's parallelogram (transmits from tB to tB+T at xB; leading edge reaches xA at tB+tau)
    _B_verts = [(_xB, _tB), (_xA, _tB + _tau),
                (_xA, _tB + _T + _tau), (_xB, _tB + _T)]

    # Collision zone (overlap of the two parallelograms at each node)
    _collision = (_tB < _tau)  # B starts before A's signal arrives → collision
    _no_collision = (_tB >= _tau)

    _fig, _ax = plt.subplots(figsize=(7.5, 7))

    _A_patch = plt.Polygon(_A_verts, closed=True,
                            facecolor='#3a86ff', edgecolor='#023e8a',
                            alpha=0.35, linewidth=1.8, zorder=2)
    _B_patch = plt.Polygon(_B_verts, closed=True,
                            facecolor='#ff6b6b', edgecolor='#9d0208',
                            alpha=0.35, linewidth=1.8, zorder=2)
    _ax.add_patch(_A_patch)
    _ax.add_patch(_B_patch)

    # Key horizontal reference lines
    for _t_ref, _lbl, _col in [
        (0,            't = 0',         '#023e8a'),
        (_tB,          f't_B = {_tB:.2f}', '#9d0208'),
        (_tau,         f'τ = {_tau:.1f}',  '#023e8a'),
        (_tB + _tau,   f't_B+τ = {_tB+_tau:.2f}', '#9d0208'),
    ]:
        _ax.axhline(_t_ref, color=_col, linestyle=':', alpha=0.5, linewidth=0.9)
        _ax.text(-0.07, _t_ref, _lbl, ha='right', va='center',
                 fontsize=8, color=_col)

    # CSMA/CD abort line for A
    if _cd and _collision:
        _ax.axhline(_t_abort, color='#e76f51', linestyle='--', linewidth=1.8, alpha=0.8)
        _ax.text(_xA + 0.02, _t_abort - 0.1,
                 f'A aborts at {_t_abort:.2f}\n(B\'s signal arrives)',
                 fontsize=8, color='#e76f51', va='top')

    # Node guides
    for _x, _lbl, _col in [(_xA, 'Node A', '#023e8a'), (_xB, 'Node B', '#9d0208')]:
        _ax.axvline(_x, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)
        _ax.text(_x, -0.3, _lbl, ha='center', va='top',
                 fontsize=10, fontweight='bold', color=_col)

    # Annotations
    _ax.annotate('A begins\ntransmitting', xy=(_xA, 0),
                 xytext=(-0.35, -0.15), fontsize=8, color='#023e8a', ha='center',
                 arrowprops=dict(arrowstyle='->', color='#023e8a', lw=0.9))
    if _collision:
        _ax.annotate("B starts before\nA's signal arrives!", xy=(_xB, _tB),
                     xytext=(1.3, _tB - 0.15), fontsize=8, color='#9d0208', ha='left',
                     arrowprops=dict(arrowstyle='->', color='#9d0208', lw=0.9))

    _y_max = max(_T + _tau, _tB + _T + _tau) + 0.5
    _ax.set_xlim(-0.5, 1.8)
    _ax.set_ylim(-0.5, _y_max)
    _ax.invert_yaxis()
    _ax.set_xlabel('Position', fontsize=11)
    _ax.set_ylabel('Time  (increasing downward)', fontsize=11)
    _cd_str = "with CSMA/CD abort" if _cd else "CSMA only (no abort)"
    _ax.set_title(f'Collision Space–Time  ({_cd_str})', fontsize=11, fontweight='bold')
    _ax.set_xticks([_xA, _xB])
    _ax.set_xticklabels(['A', 'B'], fontsize=11)
    _ax.set_yticks([])

    _legend_handles = [
        mpatches.Patch(facecolor='#3a86ff', alpha=0.45, edgecolor='#023e8a',
                       label="A's frame"),
        mpatches.Patch(facecolor='#ff6b6b', alpha=0.45, edgecolor='#9d0208',
                       label="B's frame"),
    ]
    _ax.legend(handles=_legend_handles, loc='lower right', fontsize=9)
    plt.tight_layout()

    if _no_collision:
        _status = f"✓ **No collision** — B starts at $t_B = {_tB:.2f} \\ge \\tau = {_tau:.2f}$. B heard A and deferred."
    elif _cd:
        _wasted_A = _t_abort          # A transmitted from 0 to t_abort
        _wasted_A_pct = 100 * _t_abort / _T
        _status = (f"💥 **Collision!** A detects at $t = t_B + \\tau = {_t_abort:.2f}$ and aborts.\n\n"
                   f"A transmitted **{_t_abort:.2f}** time units before aborting "
                   f"({_wasted_A_pct:.0f}% of $T = {_T:.1f}$). "
                   f"Without CD, waste would be **{100:.0f}%** of $T$.")
    else:
        _status = (f"💥 **Collision!** Both frames wasted for their **full duration $T = {_T:.1f}$**.\n\n"
                   f"Enable CSMA/CD to see how aborting reduces the waste to just {_t_abort:.2f} time units.")

    _result = mo.vstack([mo.md(_status), _fig])
    _result
    return


# ─────────────────────────────────────────────────────────────────────────────
# PART 5: COLLISION BER SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part 5: Collision Interference & Frame Error Rate Simulator

    When two frames overlap on the wire, the bits in the collision zone are
    received with signal-to-interference ratio:

    $$\text{SINR} = \frac{S}{I} \quad \text{(linear)}$$

    Each overlapping bit's error probability is approximately $Q\!\left(\sqrt{\text{SINR}}\right)$
    (much higher than the normal $Q\!\left(\sqrt{2 \cdot \text{SNR}}\right)$ in clean channel).

    The **frame error probability** is then:
    $$P_{\text{FER}} \approx 1 - (1 - \text{BER}_0)^{L - L_{\text{overlap}}}
                                  \cdot (1 - \text{BER}_c)^{L_{\text{overlap}}}$$

    Sweep $t_B$ across the collision window to see how timing affects the damage.
    """)
    return


@app.cell
def _(mo):
    sim_L = mo.ui.slider(
        start=64, stop=1500, step=64, value=1500,
        label="Frame size L (bytes):", show_value=True
    )
    sim_R = mo.ui.slider(
        start=1, stop=1000, step=1, value=10,
        label="Data rate R (Mb/s):", show_value=True
    )
    sim_d = mo.ui.slider(
        start=10, stop=2500, step=10, value=500,
        label="Segment half-length d (m):", show_value=True
    )
    sim_SNR = mo.ui.slider(
        start=0, stop=30, step=1, value=15,
        label="Per-signal SNR (dB) in clean channel:", show_value=True
    )
    sim_SIR = mo.ui.slider(
        start=-10, stop=20, step=1, value=0,
        label="Signal-to-interference ratio S/I (dB) during collision:", show_value=True
    )
    sim_tB_us = mo.ui.slider(
        start=0.0, stop=50.0, step=0.5, value=2.0,
        label="B start time t_B (µs):", show_value=True
    )
    mo.vstack([sim_L, sim_R, sim_d, sim_SNR, sim_SIR, sim_tB_us])
    return sim_L, sim_R, sim_d, sim_SNR, sim_SIR, sim_tB_us


@app.cell
def _(mo, np, plt, sim_L, sim_R, sim_SIR, sim_SNR, sim_d, sim_tB_us, special):
    def _qfunc(x):
        return 0.5 * special.erfc(x / np.sqrt(2))

    _L_bytes = sim_L.value
    _L_bits  = _L_bytes * 8
    _R_bps   = sim_R.value * 1e6
    _d_m     = sim_d.value
    _v_prop  = 2e8
    _tau_s   = _d_m / _v_prop          # one-way delay (s)
    _T_s     = _L_bits / _R_bps        # frame duration (s)
    _tB_s    = sim_tB_us.value * 1e-6  # B start time (s)

    _SNR_lin = 10**(sim_SNR.value / 10)
    _SIR_lin = 10**(sim_SIR.value / 10)

    # BERs
    _BER0 = _qfunc(np.sqrt(2 * _SNR_lin))    # clean channel
    _BERc = _qfunc(np.sqrt(_SIR_lin))         # during collision

    # Overlap analysis at A (bits during which B's signal is present at A)
    # B's signal arrives at A during [tB + tau, tB + T + tau]
    # A transmits during [0, T]
    # Overlap interval: [max(0, tB+tau), min(T, tB+T+tau)]
    _ov_start_A = max(0.0, _tB_s + _tau_s)
    _ov_end_A   = min(_T_s, _tB_s + _T_s + _tau_s)
    _ov_dur_A   = max(0.0, _ov_end_A - _ov_start_A)
    _L_ov_A     = int(round(_ov_dur_A * _R_bps))   # overlapping bits at A

    # Overlap analysis at B (bits during which A's signal is present at B)
    # A's signal arrives at B during [tau, T + tau]
    # B transmits during [tB, tB + T]
    _ov_start_B = max(_tB_s, _tau_s)
    _ov_end_B   = min(_tB_s + _T_s, _T_s + _tau_s)
    _ov_dur_B   = max(0.0, _ov_end_B - _ov_start_B)
    _L_ov_B     = int(round(_ov_dur_B * _R_bps))

    def _fer(L_total, L_overlap, ber0, berc):
        """Frame error rate given overlap bit count."""
        p_clean = (1 - ber0) ** max(0, L_total - L_overlap)
        p_coll  = (1 - berc) ** max(0, L_overlap)
        return 1 - p_clean * p_coll

    _FER_A = _fer(_L_bits, _L_ov_A, _BER0, _BERc)
    _FER_B = _fer(_L_bits, _L_ov_B, _BER0, _BERc)

    # Sweep t_B from 0 to 2*tau to show FER vs. timing
    _tB_sweep_s  = np.linspace(0, 2.5 * _tau_s, 400)
    _FER_A_sweep = np.zeros_like(_tB_sweep_s)
    _FER_B_sweep = np.zeros_like(_tB_sweep_s)
    for _i, _tb in enumerate(_tB_sweep_s):
        _os_A = max(0, _tb + _tau_s);  _oe_A = min(_T_s, _tb + _T_s + _tau_s)
        _od_A = max(0, _oe_A - _os_A); _lo_A = int(round(_od_A * _R_bps))
        _os_B = max(_tb, _tau_s);       _oe_B = min(_tb + _T_s, _T_s + _tau_s)
        _od_B = max(0, _oe_B - _os_B); _lo_B = int(round(_od_B * _R_bps))
        _FER_A_sweep[_i] = _fer(_L_bits, _lo_A, _BER0, _BERc)
        _FER_B_sweep[_i] = _fer(_L_bits, _lo_B, _BER0, _BERc)

    _fig, (_axL, _axR) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: FER vs. t_B sweep
    _tB_us_sweep = _tB_sweep_s * 1e6
    _axL.plot(_tB_us_sweep, _FER_A_sweep, color='#023e8a', linewidth=2.5, label="FER at A")
    _axL.plot(_tB_us_sweep, _FER_B_sweep, color='#9d0208', linewidth=2.5,
              linestyle='--', label="FER at B")
    _axL.axvline(sim_tB_us.value, color='#2d6a4f', linestyle=':', linewidth=2,
                 label=f't_B = {sim_tB_us.value:.1f} µs')
    _axL.axvline(_tau_s * 1e6, color='gray', linestyle='--', linewidth=1.2, alpha=0.6,
                 label=f'τ = {_tau_s*1e6:.1f} µs (CSMA threshold)')
    _axL.plot(sim_tB_us.value, _FER_A, 'o', color='#023e8a', markersize=10, zorder=5)
    _axL.plot(sim_tB_us.value, _FER_B, 'o', color='#9d0208', markersize=10, zorder=5)
    _axL.set_xlabel('B start time $t_B$ (µs)', fontsize=11)
    _axL.set_ylabel('Frame Error Rate (FER)', fontsize=11)
    _axL.set_title('Frame Error Rate vs. B Start Time', fontsize=12, fontweight='bold')
    _axL.set_xlim(0, _tB_us_sweep[-1])
    _axL.set_ylim(-0.02, 1.05)
    _axL.legend(fontsize=9)
    _axL.grid(alpha=0.3)

    # Right: bit-level diagram showing clean vs. collision zones for A's frame
    _L_clean_A = max(0, _L_bits - _L_ov_A)
    _L_clean_A_pre  = int(round(max(0, _ov_start_A) * _R_bps))   # bits before collision
    _L_clean_A_post = max(0, _L_clean_A - _L_clean_A_pre)         # bits after

    _ax_bit = _axR
    _bar_y = 0.5
    _bar_h = 0.4
    _bar_total_w = _L_bits

    # Pre-collision clean zone
    if _L_clean_A_pre > 0:
        _ax_bit.barh(_bar_y, _L_clean_A_pre, height=_bar_h, left=0,
                     color='#3a86ff', alpha=0.7, edgecolor='white', linewidth=0)
    # Collision zone
    if _L_ov_A > 0:
        _ax_bit.barh(_bar_y, _L_ov_A, height=_bar_h, left=_L_clean_A_pre,
                     color='#ff6b6b', alpha=0.85, edgecolor='white', linewidth=0)
    # Post-collision clean zone
    if _L_clean_A_post > 0:
        _ax_bit.barh(_bar_y, _L_clean_A_post, height=_bar_h,
                     left=_L_clean_A_pre + _L_ov_A,
                     color='#3a86ff', alpha=0.7, edgecolor='white', linewidth=0)

    # Labels on bars
    if _L_ov_A > 0:
        _ax_bit.text(_L_clean_A_pre + _L_ov_A / 2, _bar_y,
                     f'{_L_ov_A} bits\ncollision\nzone',
                     ha='center', va='center', fontsize=8.5, color='white',
                     fontweight='bold')
    if _L_clean_A_pre > _L_bits * 0.05:
        _ax_bit.text(_L_clean_A_pre / 2, _bar_y,
                     f'{_L_clean_A_pre}\nbits', ha='center', va='center',
                     fontsize=7.5, color='white')
    if _L_clean_A_post > _L_bits * 0.05:
        _ax_bit.text(_L_clean_A_pre + _L_ov_A + _L_clean_A_post / 2, _bar_y,
                     f'{_L_clean_A_post}\nbits', ha='center', va='center',
                     fontsize=7.5, color='white')

    _ax_bit.set_xlim(0, _L_bits)
    _ax_bit.set_ylim(0, 1.1)
    _ax_bit.set_yticks([])
    _ax_bit.set_xlabel("Bit position in A's frame", fontsize=11)
    _ax_bit.set_title(f"A's Frame: Clean vs. Collision Bits\n"
                      f"($t_B = {sim_tB_us.value:.1f}$ µs,  "
                      f"$\\tau = {_tau_s*1e6:.1f}$ µs)", fontsize=11, fontweight='bold')

    _legend_bars = [
        mpatches.Patch(color='#3a86ff', alpha=0.7, label='Clean bits (BER₀)'),
        mpatches.Patch(color='#ff6b6b', alpha=0.85, label='Collision bits (BERc)'),
    ]
    _ax_bit.legend(handles=_legend_bars, fontsize=9, loc='upper right')
    _ax_bit.grid(alpha=0.3, axis='x')

    plt.tight_layout()

    _collision_active = (_tB_s < _tau_s) and (_L_ov_A > 0 or _L_ov_B > 0)
    _status_str = "💥 Collision active." if _collision_active else "✓ No collision — t_B ≥ τ."

    _result = mo.vstack([
        mo.md(f"""
**Physical parameters:**  L = {_L_bytes} bytes ({_L_bits} bits) — R = {sim_R.value} Mb/s — d = {_d_m} m — τ = {_tau_s*1e6:.2f} µs — T = {_T_s*1e6:.2f} µs

**BERs:**  clean channel BER₀ = $Q(\\sqrt{{2\\cdot\\text{{SNR}}}})$ = {_BER0:.2e} — collision BERc = $Q(\\sqrt{{S/I}})$ = {_BERc:.4f}

{_status_str}

| | **At A** (A's frame damaged) | **At B** (B's frame damaged) |
|---|---|---|
| Overlapping bits | {_L_ov_A} of {_L_bits} ({100*_L_ov_A/_L_bits:.1f}%) | {_L_ov_B} of {_L_bits} ({100*_L_ov_B/_L_bits:.1f}%) |
| **Frame Error Rate** | **{_FER_A:.6f}** | **{_FER_B:.6f}** |
        """),
        _fig
    ])
    _result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    | Part | Key result |
    |---|---|
    | ALOHA throughput | Pure max = $1/(2e) \approx 18\%$; Slotted max = $1/e \approx 37\%$ |
    | CSMA/CD efficiency | $\eta = 1/(1+5a)$ where $a = \tau/T$; $\to 1$ as frames get longer |
    | Min frame size | $L_{\min} = 2\tau R$ bits — derived from physics, not arbitrary |
    | Collision space–time | Parallelogram overlap visualizes wasted capacity |
    | Collision BER | Even partial overlap causes near-100% FER for typical frame sizes |

    **Key insight from Part 5:** Because a typical Ethernet frame has thousands of bits
    and S/I ≈ 0 dB during a collision, even a *small* overlap zone destroys the frame.
    This is why CSMA/CD's early-abort is valuable — it limits wasted channel time,
    but the frame is already lost regardless.
    """)
    return


if __name__ == "__main__":
    app.run()
