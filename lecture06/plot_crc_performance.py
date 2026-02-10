"""
CRC Performance Visualization for EC 441 Lecture 06.

Generates two subplots:
1. CRC polynomial division visualization
2. Burst error detection capability chart for standard CRC polynomials

Usage:
    python plot_crc_performance.py
"""

import numpy as np
import matplotlib.pyplot as plt


def gf2_divide(dividend, divisor):
    """Perform GF(2) polynomial long division.

    Args:
        dividend: list of bits (MSB first)
        divisor: list of bits (MSB first)

    Returns:
        (quotient, remainder) as lists of bits
    """
    dividend = list(dividend)
    divisor = list(divisor)
    r = len(divisor) - 1  # degree of divisor

    working = list(dividend)
    quotient = []

    for i in range(len(dividend) - r):
        if working[i] == 1:
            quotient.append(1)
            for j in range(len(divisor)):
                working[i + j] ^= divisor[j]
        else:
            quotient.append(0)

    remainder = working[-(r):]  if r > 0 else []
    return quotient, remainder


def plot_crc_division(ax):
    """Subplot 1: CRC polynomial division visualization."""
    message = [1, 1, 0, 1]       # M(x) = x^3 + x^2 + 1
    generator = [1, 0, 1, 1]     # G(x) = x^3 + x + 1
    r = len(generator) - 1       # r = 3

    # x^r * M(x): append r zeros
    padded = message + [0] * r   # 1101000

    quotient, remainder = gf2_divide(padded, generator)
    transmitted = message + remainder  # T(x)

    ax.axis('off')

    # Title and key info
    msg_str = ''.join(map(str, message))
    gen_str = ''.join(map(str, generator))
    rem_str = ''.join(map(str, remainder))
    tx_str = ''.join(map(str, transmitted))
    padded_str = ''.join(map(str, padded))

    info_lines = [
        f'Message $M$: {msg_str}  ($x^3 + x^2 + 1$)',
        f'Generator $G$: {gen_str}  ($x^3 + x + 1$, $r = {r}$)',
        f'$x^r M(x)$: {padded_str}  (append {r} zeros)',
        f'Remainder $R$: {rem_str}',
        f'Transmitted $T$: {tx_str}  ($M$ | $R$)',
    ]

    y_start = 0.95
    for i, line in enumerate(info_lines):
        color = '#1565C0' if i == 4 else 'black'
        weight = 'bold' if i == 4 else 'normal'
        ax.text(0.05, y_start - i * 0.065, line,
                transform=ax.transAxes, fontsize=11,
                fontfamily='monospace', color=color, fontweight=weight,
                verticalalignment='top')

    # Show the long division
    y_div = y_start - 0.4
    ax.text(0.05, y_div, 'GF(2) Long Division:', transform=ax.transAxes,
            fontsize=12, fontweight='bold', verticalalignment='top')

    # Perform step-by-step division display
    div_str = gen_str

    step_lines = []
    step_lines.append(f'       {" ".join(map(str, quotient))}')
    step_lines.append(f'      {"─" * (2 * len(padded) + 1)}')
    step_lines.append(f'{div_str} ) {" ".join(map(str, padded))}')

    # Simulate division steps
    w = list(padded)
    for i in range(len(padded) - r):
        if w[i] == 1:
            xor_line = [' '] * (2 * len(padded) + 8)
            for j in range(len(generator)):
                pos = 8 + 2 * (i + j)
                xor_line[pos] = str(generator[j])
            step_lines.append(''.join(xor_line))

            # Show separator
            sep_line = [' '] * (2 * len(padded) + 8)
            for j in range(len(generator)):
                pos = 8 + 2 * (i + j)
                sep_line[pos] = '─'
            step_lines.append(''.join(sep_line))

            # Perform XOR
            for j in range(len(generator)):
                w[i + j] ^= generator[j]

            # Show result
            result_line = [' '] * (2 * len(padded) + 8)
            for j in range(i, min(i + len(generator) + 1, len(padded))):
                pos = 8 + 2 * j
                result_line[pos] = str(w[j])
            step_lines.append(''.join(result_line))

    y_pos = y_div - 0.06
    for line in step_lines:
        ax.text(0.08, y_pos, line, transform=ax.transAxes,
                fontsize=9, fontfamily='monospace', verticalalignment='top')
        y_pos -= 0.042

    # Verification note
    ax.text(0.05, 0.02, f'Verify: {tx_str} ÷ {gen_str} → remainder = 000 ✓',
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            color='#4CAF50', verticalalignment='bottom')

    ax.set_title('CRC Encoding: Polynomial Division Example',
                 fontsize=14, fontweight='bold')


def plot_burst_detection(ax):
    """Subplot 2: Burst error detection capability chart for standard CRCs."""
    crcs = {
        'CRC-8\n(ATM)': {
            'r': 8,
            'guaranteed': 8,
            'prob_r1': 1 - 2**(-7),
            'prob_longer': 1 - 2**(-8),
            'color': '#4CAF50'
        },
        'CRC-16\n(USB)': {
            'r': 16,
            'guaranteed': 16,
            'prob_r1': 1 - 2**(-15),
            'prob_longer': 1 - 2**(-16),
            'color': '#2196F3'
        },
        'CRC-CCITT\n(HDLC)': {
            'r': 16,
            'guaranteed': 16,
            'prob_r1': 1 - 2**(-15),
            'prob_longer': 1 - 2**(-16),
            'color': '#9C27B0'
        },
        'CRC-32\n(Ethernet)': {
            'r': 32,
            'guaranteed': 32,
            'prob_r1': 1 - 2**(-31),
            'prob_longer': 1 - 2**(-32),
            'color': '#FF9800'
        },
    }

    names = list(crcs.keys())
    guaranteed = [crcs[n]['guaranteed'] for n in names]
    colors = [crcs[n]['color'] for n in names]
    probs = [crcs[n]['prob_longer'] for n in names]

    x = np.arange(len(names))

    # Bar chart of guaranteed burst detection length
    bars = ax.bar(x, guaranteed, color=colors, edgecolor='white',
                  linewidth=1.5, width=0.6, alpha=0.85)

    for bar, val, prob in zip(bars, guaranteed, probs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f'{val} bits', ha='center', va='bottom',
                fontsize=12, fontweight='bold')
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                '100%\ndetection',
                ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylabel('Max Guaranteed Burst Length (bits)', fontsize=12, fontweight='bold')
    ax.set_title('CRC Burst Error Detection Capability', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 40)
    ax.grid(axis='y', alpha=0.3)

    # Add annotation about longer bursts
    ax.text(0.98, 0.95,
            'Longer bursts:\n'
            'CRC-16: 99.998% detected\n'
            'CRC-32: 99.99999998% detected',
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                      edgecolor='gray', alpha=0.9))

    # Additional detection capabilities
    capabilities = [
        'All single-bit errors',
        'All double-bit errors',
        'All odd numbers of errors',
        'All burst errors \u2264 r bits',
    ]
    cap_text = 'Also detects:\n' + '\n'.join(f'  • {c}' for c in capabilities)
    ax.text(0.02, 0.95, cap_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E3F2FD',
                      edgecolor='#2196F3', alpha=0.9))


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    plot_crc_division(ax1)
    plot_burst_detection(ax2)

    fig.suptitle('EC 441: CRC Error Detection Performance',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('crc_performance.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Saved: crc_performance.png")


if __name__ == '__main__':
    main()
