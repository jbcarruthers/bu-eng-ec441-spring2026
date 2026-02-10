"""
BER Comparison Visualization for EC 441 Lectures 05-06.

Compares error detection, error correction, and repetition coding:
- Utilization (throughput efficiency)
- Residual probability of bit error
Parameters: n=1000, BER=10^-6

Usage:
    python plot_ber_comparison.py
"""

import matplotlib.pyplot as plt
from math import comb, log10


def compute_methods(n_frame=1000, ber=1e-6):
    """Compute utilization and residual P_e for three error control methods."""
    # Block error probabilities (binomial)
    f = {}
    for w in range(6):
        f[w] = comb(n_frame, w) * (ber ** w) * ((1 - ber) ** (n_frame - w))

    results = {}

    # Method 1: Single-bit error detection (parity bit)
    n_k_det = 1
    k_det = n_frame - n_k_det
    # Geometric retransmission: E[M] = 1/(1 - P(1+ errors))
    p_retransmit = 1 - f[0]
    e_m = 1 / (1 - p_retransmit) if p_retransmit < 1 else float('inf')
    # But parity detects odd errors only; even errors sneak through
    # For simplicity and matching the lecture: approximate
    u_det = k_det / (n_frame * e_m)
    # Residual: frames with 2+ errors that pass parity (even number of errors)
    # P_e ≈ sum of q*f(q)/N for q≥2
    pe_det = sum(q * f[q] for q in range(2, 6)) / n_frame
    results['Single-bit\nError Detection'] = {
        'U': u_det, 'P_e': pe_det, 'check_bits': n_k_det,
        'color': '#4CAF50', 'method': 'Parity bit (ARQ)'
    }

    # Method 2: Single-bit error correction
    # Solve (n+1) <= 2^(n-k): for k=1000, need n-k=10
    n_k_corr = 10
    k_corr = n_frame - n_k_corr
    u_corr = k_corr / n_frame
    # Residual: 2+ errors
    pe_corr = sum(q * f[q] for q in range(2, 6)) / n_frame
    results['Single-bit\nError Correction'] = {
        'U': u_corr, 'P_e': pe_corr, 'check_bits': n_k_corr,
        'color': '#2196F3', 'method': 'FEC (no retransmission)'
    }

    # Method 3: Rate 1/3 repetition coding
    k_rep = 333
    n_rep = 999
    u_rep = k_rep / n_rep
    # P_e: majority vote on 3 copies
    pe_rep = 3 * (ber ** 2) * (1 - ber) + ber ** 3
    results['Rate 1/3\nRepetition Code'] = {
        'U': u_rep, 'P_e': pe_rep, 'check_bits': n_rep - k_rep,
        'color': '#FF9800', 'method': 'Repetition + majority vote'
    }

    return results


def main():
    results = compute_methods()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    methods = list(results.keys())
    colors = [results[m]['color'] for m in methods]

    # --- Plot 1: Utilization bar chart ---
    ax1 = axes[0]
    u_values = [results[m]['U'] for m in methods]
    bars1 = ax1.bar(methods, u_values, color=colors, edgecolor='white', linewidth=1.5, width=0.6)
    for bar, val in zip(bars1, u_values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Utilization $U$', fontsize=12, fontweight='bold')
    ax1.set_title('Throughput Efficiency', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 1.15)
    ax1.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Ideal (no overhead)')
    ax1.legend(fontsize=9)
    ax1.grid(axis='y', alpha=0.3)

    # --- Plot 2: Residual P_e bar chart (log scale) ---
    ax2 = axes[1]
    pe_values = [results[m]['P_e'] for m in methods]
    bars2 = ax2.bar(methods, pe_values, color=colors, edgecolor='white', linewidth=1.5, width=0.6)
    ax2.set_yscale('log')
    for bar, val in zip(bars2, pe_values):
        exponent = log10(val) if val > 0 else 0
        ax2.text(bar.get_x() + bar.get_width() / 2, val * 2,
                 f'$10^{{{exponent:.1f}}}$', ha='center', va='bottom',
                 fontsize=12, fontweight='bold')
    ax2.set_ylabel('Residual $P_e$', fontsize=12, fontweight='bold')
    ax2.set_title('Residual Bit Error Rate', fontsize=14, fontweight='bold')
    ax2.set_ylim(1e-14, 1e-6)
    ax2.grid(axis='y', alpha=0.3, which='both')

    # --- Plot 3: Summary table ---
    ax3 = axes[2]
    ax3.axis('off')

    table_data = [
        ['Method', 'Check\nBits', '$U$', '$P_e$', 'Approach'],
    ]
    for m in methods:
        r = results[m]
        pe_str = f'{r["P_e"]:.1e}'
        table_data.append([
            m.replace('\n', ' '),
            str(r['check_bits']),
            f'{r["U"]:.3f}',
            pe_str,
            r['method']
        ])

    # Header
    header_color = '#1565C0'
    cell_colors = [['white'] * 5 for _ in range(len(table_data))]
    cell_colors[0] = [header_color] * 5

    table = ax3.table(
        cellText=table_data,
        cellLoc='center',
        loc='center',
        cellColours=cell_colors
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.8)

    # Style header row
    for j in range(5):
        cell = table[0, j]
        cell.set_text_props(fontweight='bold', color='white')
        cell.set_facecolor(header_color)
        cell.set_edgecolor('white')

    # Alternating row colors
    for i in range(1, len(table_data)):
        row_color = '#f0f0f0' if i % 2 == 0 else 'white'
        for j in range(5):
            table[i, j].set_facecolor(row_color)
            table[i, j].set_edgecolor('#dddddd')

    ax3.set_title('Comparison Summary\n($n=1000$, $BER=10^{-6}$)',
                  fontsize=14, fontweight='bold')

    fig.suptitle('EC 441: Error Control Method Comparison',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('ber_comparison.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Saved: ber_comparison.png")


if __name__ == '__main__':
    main()
