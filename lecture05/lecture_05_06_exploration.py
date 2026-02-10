import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from math import comb
    return comb, mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Lectures 5 & 6: Error Control Coding — Interactive Exploration

    **EC 441 - Introduction to Computer Networking**

    This notebook contains interactive demonstrations for error control coding concepts
    including Hamming distance, minimum distance, the $d_{\min}$ theorem,
    block error probabilities, BER comparison, and CRC encoding/decoding.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 1: Hamming Distance Calculator

    Enter two binary codewords to compute their Hamming distance and visualize differing bits.
    """)
    return


@app.cell
def _(mo):
    cw1_input = mo.ui.text(
        value="1011001",
        label="Codeword 1 (binary):",
    )
    cw2_input = mo.ui.text(
        value="1100011",
        label="Codeword 2 (binary):",
    )
    mo.vstack([cw1_input, cw2_input])
    return cw1_input, cw2_input


@app.cell
def _(cw1_input, cw2_input, mo, np, plt):
    _cw1_str = cw1_input.value.strip()
    _cw2_str = cw2_input.value.strip()

    _valid = True
    _error_msg = ""
    if not all(_c in '01' for _c in _cw1_str) or not all(_c in '01' for _c in _cw2_str):
        _valid = False
        _error_msg = "Codewords must contain only 0s and 1s."
    elif len(_cw1_str) != len(_cw2_str):
        _valid = False
        _error_msg = "Codewords must have the same length."
    elif len(_cw1_str) == 0:
        _valid = False
        _error_msg = "Codewords cannot be empty."

    if _valid:
        _cw1_bits = [int(_b) for _b in _cw1_str]
        _cw2_bits = [int(_b) for _b in _cw2_str]
        _n_bits = len(_cw1_bits)
        _diffs = [_idx for _idx in range(_n_bits) if _cw1_bits[_idx] != _cw2_bits[_idx]]
        _hamming_dist = len(_diffs)

        _fig, _ax = plt.subplots(figsize=(max(8, _n_bits * 1.2), 4))
        _x = np.arange(_n_bits)
        _bar_w = 0.35

        for _idx in range(_n_bits):
            _clr = '#f8d7da' if _idx in _diffs else '#d4edda'
            _ax.axvspan(_idx - 0.45, _idx + 0.45, alpha=0.4, color=_clr, zorder=0)

        _bars1 = _ax.bar(_x - _bar_w / 2, _cw1_bits, _bar_w,
                         label='Codeword 1', color='#2196F3', edgecolor='white', linewidth=1.5)
        _bars2 = _ax.bar(_x + _bar_w / 2, _cw2_bits, _bar_w,
                         label='Codeword 2', color='#FF9800', edgecolor='white', linewidth=1.5)

        for _bar_group in [_bars1, _bars2]:
            for _b in _bar_group:
                _h = _b.get_height()
                _ax.text(_b.get_x() + _b.get_width() / 2, _h / 2,
                         f'{int(_h)}', ha='center', va='center',
                         fontsize=11, fontweight='bold', color='white')

        for _idx in _diffs:
            _ax.text(_idx, 1.15, '×', ha='center', fontsize=16, fontweight='bold', color='red')

        _ax.set_title(f'Hamming Distance = {_hamming_dist}', fontsize=14, fontweight='bold')
        _ax.set_xticks(_x)
        _ax.set_xticklabels([f'b{_idx}' for _idx in range(_n_bits)])
        _ax.set_ylim(-0.1, 1.4)
        _ax.set_yticks([0, 1])
        _ax.set_xlabel('Bit Position', fontsize=12)
        _ax.legend(loc='upper right')
        _ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()

        _result = mo.vstack([
            mo.md(f"**Hamming distance:** d({_cw1_str}, {_cw2_str}) = **{_hamming_dist}**"),
            mo.md(f"**Differing positions:** {_diffs if _diffs else 'None (identical)'}"),
            plt.gca()
        ])
    else:
        _result = mo.md(f"**Error:** {_error_msg}")

    _result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 2: Code Distance Explorer

    Enter a set of codewords (one per line) to compute all pairwise Hamming distances and $d_{\min}$.
    """)
    return


@app.cell
def _(mo):
    codewords_input = mo.ui.text_area(
        value="00000\n11100\n11011\n00111",
        label="Codewords (one per line, binary):",
    )
    codewords_input
    return (codewords_input,)


@app.cell
def _(codewords_input, mo, np, plt):
    _lines = [_ln.strip() for _ln in codewords_input.value.strip().split('\n') if _ln.strip()]

    _valid_code = True
    _code_error = ""
    if len(_lines) < 2:
        _valid_code = False
        _code_error = "Need at least 2 codewords."
    elif len(set(len(_ln) for _ln in _lines)) > 1:
        _valid_code = False
        _code_error = "All codewords must have the same length."
    elif not all(all(_c in '01' for _c in _ln) for _ln in _lines):
        _valid_code = False
        _code_error = "Codewords must contain only 0s and 1s."

    if _valid_code:
        _codewords = _lines
        _num_cw = len(_codewords)

        _dist_matrix = np.zeros((_num_cw, _num_cw), dtype=int)
        _all_distances = []
        for _i in range(_num_cw):
            for _j in range(_i + 1, _num_cw):
                _d = sum(_a != _b for _a, _b in zip(_codewords[_i], _codewords[_j]))
                _dist_matrix[_i][_j] = _d
                _dist_matrix[_j][_i] = _d
                _all_distances.append((_codewords[_i], _codewords[_j], _d))

        _d_min = min(_d for _, _, _d in _all_distances)

        _table_rows = []
        for _cw_i, _cw_j, _d in _all_distances:
            _marker = " ← d_min" if _d == _d_min else ""
            _table_rows.append(f"| `{_cw_i}` | `{_cw_j}` | {_d}{_marker} |")

        _table_md = "| Codeword $C_i$ | Codeword $C_j$ | Distance |\n"
        _table_md += "|:---:|:---:|:---:|\n"
        _table_md += "\n".join(_table_rows)

        _fig, _ax = plt.subplots(figsize=(max(5, _num_cw * 1.2), max(4, _num_cw)))
        _im = _ax.imshow(_dist_matrix, cmap='YlOrRd', aspect='equal')
        _ax.set_xticks(range(_num_cw))
        _ax.set_yticks(range(_num_cw))
        _ax.set_xticklabels(_codewords, fontsize=9, rotation=45, ha='right')
        _ax.set_yticklabels(_codewords, fontsize=9)
        for _i in range(_num_cw):
            for _j in range(_num_cw):
                _clr = 'white' if _dist_matrix[_i][_j] > (_d_min + max(_d for _, _, _d in _all_distances)) / 2 else 'black'
                _ax.text(_j, _i, str(_dist_matrix[_i][_j]), ha='center', va='center',
                         fontsize=12, fontweight='bold', color=_clr)
        _ax.set_title('Pairwise Hamming Distance Matrix', fontsize=13, fontweight='bold')
        _fig.colorbar(_im, ax=_ax, label='Hamming Distance')
        plt.tight_layout()

        _e_d_max = _d_min - 1
        _e_c_max = (_d_min - 1) // 2
        _n = len(_codewords[0])
        _k_approx = int(np.log2(_num_cw)) if _num_cw > 0 else 0

        _caps = f"""**Code parameters:** $n = {_n}$, $|\\mathcal{{C}}| = {_num_cw}$ codewords"""
        if _num_cw > 0 and (_num_cw & (_num_cw - 1)) == 0:
            _caps += f", $k = {_k_approx}$, Rate $R_c = {_k_approx}/{_n} = {_k_approx/_n:.3f}$"
        _caps += f"\n\n**Minimum distance:** $d_{{\\min}} = {_d_min}$"
        _caps += f"\n\n**Max error detection** ($e_c = 0$): $e_d = {_e_d_max}$ errors"
        _caps += f"\n\n**Max error correction** ($e_c = e_d$): $e_c = {_e_c_max}$ errors"

        _code_result = mo.vstack([
            mo.md(_table_md),
            mo.md(_caps),
            plt.gca()
        ])
    else:
        _code_result = mo.md(f"**Error:** {_code_error}")

    _code_result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 3: Error Detection vs. Correction Tradeoff

    Explore how $d_{\min}$ constrains the valid $(e_c, e_d)$ pairs.

    **The $d_{\min}$ theorem:** $e_c + e_d \le d_{\min} - 1$ and $e_c \le e_d$.
    """)
    return


@app.cell
def _(mo):
    dmin_slider = mo.ui.slider(
        start=2,
        stop=15,
        step=1,
        value=7,
        label="Minimum distance d_min:",
        show_value=True
    )
    dmin_slider
    return (dmin_slider,)


@app.cell
def _(dmin_slider, mo, np, plt):
    _d_min_val = dmin_slider.value

    _valid_pairs = []
    for _ec in range(_d_min_val):
        for _ed in range(_ec, _d_min_val):
            if _ec + _ed <= _d_min_val - 1:
                _valid_pairs.append((_ec, _ed))

    _table_lines = "| $e_c$ | $e_d$ | Note |\n|:---:|:---:|:---|\n"
    for _ec, _ed in _valid_pairs:
        _note = ""
        if _ec == 0 and _ed == _d_min_val - 1:
            _note = "← Max detection $(e_d)_{\\max}$"
        elif _ec == _ed and _ec == (_d_min_val - 1) // 2:
            _note = "← Max correction $(e_c)_{\\max}$"
        _table_lines += f"| {_ec} | {_ed} | {_note} |\n"

    _fig, _ax = plt.subplots(figsize=(8, 6))

    _ec_range = np.linspace(0, _d_min_val - 1, 200)
    _ed_upper = _d_min_val - 1 - _ec_range
    _ax.fill_between(_ec_range, _ec_range, np.minimum(_ed_upper, _d_min_val),
                     where=(_ed_upper >= _ec_range),
                     alpha=0.2, color='#2196F3', label='Valid region')

    for _ec, _ed in _valid_pairs:
        _mc = '#F44336' if (_ec == 0 and _ed == _d_min_val - 1) or (_ec == _ed and _ec == (_d_min_val - 1) // 2) else '#2196F3'
        _ms = 120 if _mc == '#F44336' else 80
        _ax.scatter(_ec, _ed, color=_mc, s=_ms, zorder=5, edgecolors='white', linewidth=1.5)

    _ax.plot([0, (_d_min_val - 1) / 2], [_d_min_val - 1, (_d_min_val - 1) / 2],
             'b--', linewidth=1.5, label='$e_c + e_d = d_{\\min} - 1$')
    _ax.plot([0, _d_min_val], [0, _d_min_val],
             'g--', linewidth=1.5, label='$e_c = e_d$')

    _ax.set_xlabel('$e_c$ (errors corrected)', fontsize=12, fontweight='bold')
    _ax.set_ylabel('$e_d$ (errors detected)', fontsize=12, fontweight='bold')
    _ax.set_title(f'Valid $(e_c, e_d)$ Pairs for $d_{{\\min}} = {_d_min_val}$',
                  fontsize=14, fontweight='bold')
    _ax.set_xlim(-0.5, _d_min_val)
    _ax.set_ylim(-0.5, _d_min_val)
    _ax.set_aspect('equal')
    _ax.legend(loc='upper right', fontsize=10)
    _ax.grid(alpha=0.3)
    plt.tight_layout()

    _tradeoff_result = mo.vstack([
        mo.md(f"**$d_{{\\min}} = {_d_min_val}$:** There are **{len(_valid_pairs)}** valid $(e_c, e_d)$ pairs."),
        mo.md(_table_lines),
        plt.gca()
    ])

    _tradeoff_result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 4: Block Error Probability Calculator

    Given a channel BER and block size $n$, compute $P(w \text{ errors})$ using the binomial distribution:

    $$f(w) = \binom{n}{w} p^w (1-p)^{n-w}$$
    """)
    return


@app.cell
def _(mo):
    block_n = mo.ui.slider(
        start=10,
        stop=10000,
        step=10,
        value=1000,
        label="Block size n:",
        show_value=True
    )
    ber_exp = mo.ui.slider(
        start=-9,
        stop=-1,
        step=1,
        value=-6,
        label="BER exponent (10^x):",
        show_value=True
    )
    max_errors = mo.ui.slider(
        start=1,
        stop=10,
        step=1,
        value=5,
        label="Show up to w errors:",
        show_value=True
    )
    mo.vstack([block_n, ber_exp, max_errors])
    return ber_exp, block_n, max_errors


@app.cell
def _(ber_exp, block_n, comb, max_errors, mo, np, plt):
    _n_val = block_n.value
    _p_val = 10.0 ** ber_exp.value
    _w_max = max_errors.value

    _probs = []
    for _w in range(_w_max + 1):
        _fw = comb(_n_val, _w) * (_p_val ** _w) * ((1 - _p_val) ** (_n_val - _w))
        _probs.append(_fw)

    _fig, _ax = plt.subplots(figsize=(10, 5))
    _w_values = list(range(_w_max + 1))
    _colors = ['#4CAF50' if _w == 0 else '#2196F3' if _w == 1 else '#FF9800' for _w in _w_values]
    _bars = _ax.bar(_w_values, _probs, color=_colors, edgecolor='white', linewidth=1.5, width=0.6)

    for _bar, _prob in zip(_bars, _probs):
        if _prob > 0:
            _label = f'{_prob:.2e}'
            _y_pos = _bar.get_height() * 1.1 if _bar.get_height() > 0 else 0.01 * max(_probs)
            _ax.text(_bar.get_x() + _bar.get_width() / 2, _y_pos,
                     _label, ha='center', va='bottom', fontsize=10, fontweight='bold')

    _ax.set_xlabel('Number of Errors $w$', fontsize=12, fontweight='bold')
    _ax.set_ylabel('$P(w$ errors$)$', fontsize=12, fontweight='bold')
    _ax.set_title(f'Block Error Probability ($n = {_n_val}$, $BER = 10^{{{ber_exp.value}}}$)',
                  fontsize=14, fontweight='bold')
    _ax.set_yscale('log')
    _min_nonzero = min(_p for _p in _probs if _p > 0) if any(_p > 0 for _p in _probs) else 1e-20
    _ax.set_ylim(_min_nonzero / 100, 10)
    _ax.set_xticks(_w_values)
    _ax.grid(axis='y', alpha=0.3, which='both')
    plt.tight_layout()

    _table_md = "| $w$ | $f(w) = P(w \\text{ errors})$ |\n|:---:|:---:|\n"
    for _w, _fw in zip(_w_values, _probs):
        if _fw > 1e-3:
            _table_md += f"| {_w} | {_fw:.6f} |\n"
        elif _fw > 0:
            _exp = np.log10(_fw) if _fw > 0 else float('-inf')
            _table_md += f"| {_w} | $10^{{{_exp:.1f}}}$ |\n"
        else:
            _table_md += f"| {_w} | ≈ 0 |\n"

    _block_result = mo.vstack([
        mo.md(_table_md),
        plt.gca()
    ])

    _block_result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 5: BER Comparison — Detection vs. Correction vs. Repetition

    Compare utilization and residual $P_e$ for three error control methods.
    """)
    return


@app.cell
def _(mo):
    comp_n = mo.ui.slider(
        start=100,
        stop=10000,
        step=100,
        value=1000,
        label="Frame size n:",
        show_value=True
    )
    comp_ber_exp = mo.ui.slider(
        start=-9,
        stop=-3,
        step=1,
        value=-6,
        label="BER exponent (10^x):",
        show_value=True
    )
    mo.vstack([comp_n, comp_ber_exp])
    return comp_ber_exp, comp_n


@app.cell
def _(comb, comp_ber_exp, comp_n, mo, np, plt):
    _n_comp = comp_n.value
    _ber_comp = 10.0 ** comp_ber_exp.value

    _f_vals = []
    for _w in range(6):
        _fw = comb(_n_comp, _w) * (_ber_comp ** _w) * ((1 - _ber_comp) ** (_n_comp - _w))
        _f_vals.append(_fw)

    _k_det = _n_comp - 1
    _p_error_in_block = 1 - _f_vals[0]
    _em_det = 1 / (1 - _p_error_in_block) if _p_error_in_block < 1 else float('inf')
    _u_det = _k_det / (_n_comp * _em_det)
    _pe_det = sum(_q * _f_vals[_q] for _q in range(2, min(6, _n_comp + 1))) / _n_comp

    _n_k_corr = 1
    while (_n_comp + 1) > 2 ** _n_k_corr:
        _n_k_corr += 1
    _k_corr = _n_comp - _n_k_corr
    _u_corr = _k_corr / _n_comp
    _pe_corr = sum(_q * _f_vals[_q] for _q in range(2, min(6, _n_comp + 1))) / _n_comp

    _k_rep = _n_comp // 3
    _u_rep = _k_rep / (_k_rep * 3) if _k_rep > 0 else 0
    _pe_rep = 3 * (_ber_comp ** 2) * (1 - _ber_comp) + _ber_comp ** 3

    _methods = ['Single-bit\nDetection', 'Single-bit\nCorrection', 'Rate 1/3\nRepetition']
    _u_vals = [_u_det, _u_corr, _u_rep]
    _pe_vals = [_pe_det, _pe_corr, _pe_rep]
    _colors_comp = ['#4CAF50', '#2196F3', '#FF9800']

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(14, 5))

    _bars1 = _ax1.bar(_methods, _u_vals, color=_colors_comp, edgecolor='white', linewidth=1.5, width=0.5)
    for _bar, _val in zip(_bars1, _u_vals):
        _ax1.text(_bar.get_x() + _bar.get_width() / 2, _bar.get_height() + 0.01,
                  f'{_val:.3f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    _ax1.set_ylabel('Utilization $U$', fontsize=12, fontweight='bold')
    _ax1.set_title('Throughput Efficiency', fontsize=14, fontweight='bold')
    _ax1.set_ylim(0, 1.15)
    _ax1.grid(axis='y', alpha=0.3)

    _bars2 = _ax2.bar(_methods, _pe_vals, color=_colors_comp, edgecolor='white', linewidth=1.5, width=0.5)
    _ax2.set_yscale('log')
    for _bar, _val in zip(_bars2, _pe_vals):
        if _val > 0:
            _exp = np.log10(_val)
            _ax2.text(_bar.get_x() + _bar.get_width() / 2, _val * 2,
                      f'$10^{{{_exp:.1f}}}$', ha='center', va='bottom',
                      fontsize=11, fontweight='bold')
    _ax2.set_ylabel('Residual $P_e$', fontsize=12, fontweight='bold')
    _ax2.set_title('Residual Bit Error Rate', fontsize=14, fontweight='bold')
    _ax2.grid(axis='y', alpha=0.3, which='both')
    plt.tight_layout()

    _table_md = f"**Parameters:** $n = {_n_comp}$, $BER = 10^{{{comp_ber_exp.value}}}$\n\n"
    _table_md += "| Method | Check Bits | $U$ | $P_e$ |\n|:---|:---:|:---:|:---:|\n"
    _check_bits = [1, _n_k_corr, _n_comp - _k_rep]
    for _m, _cb, _u, _pe in zip(['Detection (parity)', 'Correction (FEC)', 'Repetition (1/3)'],
                                 _check_bits, _u_vals, _pe_vals):
        _pe_str = f'{_pe:.2e}' if _pe > 0 else '≈ 0'
        _table_md += f"| {_m} | {_cb} | {_u:.3f} | {_pe_str} |\n"

    _comp_result = mo.vstack([
        mo.md(_table_md),
        plt.gca()
    ])

    _comp_result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 6: CRC Encoder/Decoder

    Enter a message and generator polynomial (as binary strings) to see the CRC encoding step by step.
    """)
    return


@app.cell
def _(mo):
    msg_input = mo.ui.text(
        value="1101",
        label="Message M (binary):",
    )
    gen_input = mo.ui.text(
        value="1011",
        label="Generator G (binary):",
    )
    mo.vstack([msg_input, gen_input])
    return gen_input, msg_input


@app.cell
def _(gen_input, mo, msg_input):
    _msg_str = msg_input.value.strip()
    _gen_str = gen_input.value.strip()

    _valid_crc = True
    _crc_error_msg = ""
    if not all(_c in '01' for _c in _msg_str) or not all(_c in '01' for _c in _gen_str):
        _valid_crc = False
        _crc_error_msg = "Inputs must contain only 0s and 1s."
    elif len(_msg_str) < 1 or len(_gen_str) < 2:
        _valid_crc = False
        _crc_error_msg = "Message must be at least 1 bit; generator at least 2 bits."
    elif _gen_str[0] != '1':
        _valid_crc = False
        _crc_error_msg = "Generator must start with 1."

    if _valid_crc:
        _msg_bits = [int(_b) for _b in _msg_str]
        _gen_bits = [int(_b) for _b in _gen_str]
        _r_crc = len(_gen_bits) - 1
        _k_crc = len(_msg_bits)

        _padded_bits = _msg_bits + [0] * _r_crc
        _padded_str = ''.join(map(str, _padded_bits))

        _working = list(_padded_bits)
        _quotient_bits = []

        for _i in range(len(_padded_bits) - _r_crc):
            if _working[_i] == 1:
                _quotient_bits.append(1)
                for _j in range(len(_gen_bits)):
                    _working[_i + _j] ^= _gen_bits[_j]
            else:
                _quotient_bits.append(0)

        _remainder_bits = _working[-_r_crc:] if _r_crc > 0 else []
        _remainder_str = ''.join(map(str, _remainder_bits))
        _transmitted_bits = _msg_bits + _remainder_bits
        _transmitted_str = ''.join(map(str, _transmitted_bits))
        _quotient_str = ''.join(map(str, _quotient_bits))

        def _bits_to_poly(bits):
            terms = []
            deg = len(bits) - 1
            for idx, b in enumerate(bits):
                if b == 1:
                    power = deg - idx
                    if power == 0:
                        terms.append("1")
                    elif power == 1:
                        terms.append("x")
                    else:
                        terms.append(f"x^{power}")
            return " + ".join(terms) if terms else "0"

        _msg_poly = _bits_to_poly(_msg_bits)
        _gen_poly = _bits_to_poly(_gen_bits)
        _rem_poly = _bits_to_poly(_remainder_bits) if _remainder_bits else "0"
        _tx_poly = _bits_to_poly(_transmitted_bits)

        _output_md = f"""### CRC Encoding Result

**Message $M(x)$:** `{_msg_str}` = ${_msg_poly}$ ($k = {_k_crc}$)

**Generator $G(x)$:** `{_gen_str}` = ${_gen_poly}$ ($r = {_r_crc}$)

**Step 1:** Append {_r_crc} zeros → $x^{_r_crc} M(x)$ = `{_padded_str}`

**Step 2:** Divide `{_padded_str}` by `{_gen_str}`

**Quotient:** `{_quotient_str}`

**Remainder $R(x)$:** `{_remainder_str}` = ${_rem_poly}$

**Step 3: Transmitted frame $T(x)$:** `{_transmitted_str}` = ${_tx_poly}$ ($n = {_k_crc + _r_crc}$ bits)

---

**Verification:** `{_transmitted_str}` ÷ `{_gen_str}` → remainder = `{''.join(['0'] * _r_crc)}` ✓
"""
        _crc_result = mo.md(_output_md)
    else:
        _crc_result = mo.md(f"**Error:** {_crc_error_msg}")

    _crc_result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Cell 7: CRC Error Detection Demo

    Introduce bit errors into a transmitted frame and see if CRC catches them.
    """)
    return


@app.cell
def _(mo):
    demo_msg = mo.ui.text(
        value="11010011",
        label="Message M (binary):",
    )
    demo_gen = mo.ui.text(
        value="10011",
        label="Generator G (binary):",
    )
    error_positions = mo.ui.text(
        value="2,5",
        label="Error bit positions (comma-separated, 0-indexed):",
    )
    mo.vstack([demo_msg, demo_gen, error_positions])
    return demo_gen, demo_msg, error_positions


@app.cell
def _(demo_gen, demo_msg, error_positions, mo):
    _dm_str = demo_msg.value.strip()
    _dg_str = demo_gen.value.strip()
    _ep_str = error_positions.value.strip()

    _valid_demo = True
    _demo_err = ""

    if not all(_c in '01' for _c in _dm_str) or not all(_c in '01' for _c in _dg_str):
        _valid_demo = False
        _demo_err = "Message and generator must contain only 0s and 1s."
    elif len(_dm_str) < 1 or len(_dg_str) < 2 or _dg_str[0] != '1':
        _valid_demo = False
        _demo_err = "Invalid message or generator."

    if _valid_demo:
        _dm_bits = [int(_b) for _b in _dm_str]
        _dg_bits = [int(_b) for _b in _dg_str]
        _r_demo = len(_dg_bits) - 1

        _padded_demo = _dm_bits + [0] * _r_demo
        _working_demo = list(_padded_demo)
        for _i in range(len(_padded_demo) - _r_demo):
            if _working_demo[_i] == 1:
                for _j in range(len(_dg_bits)):
                    _working_demo[_i + _j] ^= _dg_bits[_j]
        _rem_demo = _working_demo[-_r_demo:] if _r_demo > 0 else []
        _tx_demo = _dm_bits + _rem_demo
        _tx_str_demo = ''.join(map(str, _tx_demo))

        try:
            if _ep_str:
                _err_pos = [int(_x.strip()) for _x in _ep_str.split(',') if _x.strip()]
                _err_pos = [_p for _p in _err_pos if 0 <= _p < len(_tx_demo)]
            else:
                _err_pos = []
        except ValueError:
            _err_pos = []

        _rx_demo = list(_tx_demo)
        for _p in _err_pos:
            _rx_demo[_p] ^= 1
        _rx_str_demo = ''.join(map(str, _rx_demo))

        _working_rx = list(_rx_demo)
        for _i in range(len(_rx_demo) - _r_demo):
            if _working_rx[_i] == 1:
                for _j in range(len(_dg_bits)):
                    if _i + _j < len(_working_rx):
                        _working_rx[_i + _j] ^= _dg_bits[_j]
        _rx_rem = _working_rx[-_r_demo:] if _r_demo > 0 else []
        _rx_rem_str = ''.join(map(str, _rx_rem))
        _detected = any(_b == 1 for _b in _rx_rem)

        _error_pattern = [0] * len(_tx_demo)
        for _p in _err_pos:
            _error_pattern[_p] = 1

        _tx_visual = '  '.join(map(str, _tx_demo))
        _err_visual = '  '.join('×' if _error_pattern[_idx] else '·' for _idx in range(len(_tx_demo)))
        _rx_visual = '  '.join(map(str, _rx_demo))

        _status_icon = "**Error DETECTED**" if _detected else "**No error detected**"
        _status_note = "(CRC remainder ≠ 0 → reject frame)" if _detected else "(CRC remainder = 0 → accept frame)"
        if not _err_pos:
            _status_note = "(No errors introduced)"

        _num_errors = len(_err_pos)
        _burst_len = (max(_err_pos) - min(_err_pos) + 1) if _err_pos else 0

        _demo_md = f"""### CRC Error Detection Demo

**Transmitted:** `{_tx_str_demo}`

**Error positions:** {_err_pos if _err_pos else 'None'} ({_num_errors} error{'s' if _num_errors != 1 else ''}{f', burst length {_burst_len}' if _burst_len > 1 else ''})

```
TX:     {_tx_visual}
Errors: {_err_visual}
RX:     {_rx_visual}
```

**Received:** `{_rx_str_demo}`

**CRC check remainder:** `{_rx_rem_str}`

### Result: {_status_icon}
{_status_note}
"""
        _demo_result = mo.md(_demo_md)
    else:
        _demo_result = mo.md(f"**Error:** {_demo_err}")

    _demo_result
    return


if __name__ == "__main__":
    app.run()
