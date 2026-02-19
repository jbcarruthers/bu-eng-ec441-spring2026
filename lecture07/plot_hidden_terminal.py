"""
Hidden Terminal Problem: Diagrams for EC 441 Lecture 07.

Saves two separate figures:
  hidden_terminal_spatial.png   — nodes A, B, C with transmission range circles.
  hidden_terminal_spacetime.png — space-time diagram showing collision at B.

Usage:
    python plot_hidden_terminal.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTDIR = '/Users/jeffreycarruthers/networking/notes/topic6_mac/'
colors = {'A': '#3a86ff', 'B': '#2d6a4f', 'C': '#e76f51'}

# ─────────────────────────────────────────────
# FIGURE 1: spatial layout
# ─────────────────────────────────────────────
fig1, ax_top = plt.subplots(figsize=(7, 4))

pos = {'A': (0.0, 0.5), 'B': (1.0, 0.5), 'C': (2.0, 0.5)}
range_radius = 1.05   # just over 1 unit so A↔B and B↔C are in range; A↔C are not

for node, (x, y) in pos.items():
    circle = plt.Circle((x, y), range_radius,
                         color=colors[node], fill=False,
                         linestyle='--', linewidth=1.5, alpha=0.55)
    ax_top.add_patch(circle)
    ax_top.plot(x, y, 'o', color=colors[node], markersize=14, zorder=5)
    ax_top.text(x, y, node, ha='center', va='center',
                fontsize=11, fontweight='bold', color='white', zorder=6)

# "In range" annotations
ax_top.annotate('', xy=(pos['B'][0] - 0.05, 0.55),
                xytext=(pos['A'][0] + 0.05, 0.55),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
ax_top.text(0.5, 0.62, 'in range', ha='center', fontsize=8.5, color='gray')

ax_top.annotate('', xy=(pos['C'][0] - 0.05, 0.55),
                xytext=(pos['B'][0] + 0.05, 0.55),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
ax_top.text(1.5, 0.62, 'in range', ha='center', fontsize=8.5, color='gray')

# "Out of range" annotation
ax_top.annotate('', xy=(pos['C'][0] - 0.05, 0.38),
                xytext=(pos['A'][0] + 0.05, 0.38),
                arrowprops=dict(arrowstyle='<->', color='#c1121f', lw=1.5,
                                linestyle='dashed'))
ax_top.text(1.0, 0.30, 'out of range  (hidden from each other)',
            ha='center', fontsize=8.5, color='#c1121f')

ax_top.set_xlim(-1.2, 3.2)
ax_top.set_ylim(-0.65, 1.65)
ax_top.set_aspect('equal')
ax_top.axis('off')
ax_top.set_title('Hidden Terminal Problem: Spatial Layout',
                 fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTDIR + 'hidden_terminal_spatial.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved hidden_terminal_spatial.png")

# ─────────────────────────────────────────────
# FIGURE 2: space-time diagram
# ─────────────────────────────────────────────
fig2, ax_bot = plt.subplots(figsize=(7, 5.5))

tau = 1.0    # propagation delay between adjacent nodes (A→B or B→C)
T = 3.5      # frame transmission time
x_A, x_B, x_C = 0.0, 1.0, 2.0

# A's frame: t=0 to T, propagates right toward B (reaches B at tau)
A_verts = [(x_A, 0), (x_B, tau), (x_B, T + tau), (x_A, T)]
ax_bot.add_patch(plt.Polygon(A_verts, closed=True,
                              facecolor='#3a86ff', edgecolor='#023e8a',
                              alpha=0.35, linewidth=1.5))

# C's frame: t=0 to T, propagates left toward B (reaches B at tau)
C_verts = [(x_C, 0), (x_B, tau), (x_B, T + tau), (x_C, T)]
ax_bot.add_patch(plt.Polygon(C_verts, closed=True,
                              facecolor='#e76f51', edgecolor='#9d0208',
                              alpha=0.35, linewidth=1.5))

# Highlight collision zone at B (from tau to T+tau)
ax_bot.fill_betweenx([tau, T + tau], x_B - 0.03, x_B + 0.03,
                      color='#c1121f', alpha=0.7, zorder=3)

# Key horizontal lines
ax_bot.axhline(y=0,         color='gray', linestyle=':', alpha=0.5, linewidth=0.8)
ax_bot.axhline(y=tau,       color='#c1121f', linestyle=':', alpha=0.5, linewidth=0.8)
ax_bot.axhline(y=T + tau,   color='gray', linestyle=':', alpha=0.5, linewidth=0.8)

ax_bot.text(-0.08, 0,       't = 0', ha='right', va='center', fontsize=8.5)
ax_bot.text(-0.08, tau,     't = τ', ha='right', va='center', fontsize=8.5, color='#c1121f')
ax_bot.text(-0.08, T + tau, 't = T+τ', ha='right', va='center', fontsize=8.5)

# Node vertical guides
for x, lbl, col in [(x_A, 'A', '#3a86ff'), (x_B, 'B', '#2d6a4f'), (x_C, 'C', '#e76f51')]:
    ax_bot.axvline(x=x, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)
    ax_bot.text(x, -0.3, f'Node {lbl}', ha='center', va='top',
                fontsize=10, fontweight='bold', color=col)

# Annotations
ax_bot.annotate("A senses idle,\ntransmits to B",
                xy=(x_A, 0.1), xytext=(-0.55, 0.5),
                fontsize=8, ha='center', color='#023e8a',
                arrowprops=dict(arrowstyle='->', color='#023e8a', lw=0.8))

ax_bot.annotate("C senses idle,\ntransmits to B\n(can't hear A!)",
                xy=(x_C, 0.1), xytext=(2.55, 0.5),
                fontsize=8, ha='center', color='#9d0208',
                arrowprops=dict(arrowstyle='->', color='#9d0208', lw=0.8))

ax_bot.annotate("Collision!\nNeither A nor C\ndetects it.",
                xy=(x_B, (tau + T + tau) / 2),
                xytext=(1.55, (tau + T + tau) / 2),
                fontsize=8.5, ha='left', color='#c1121f',
                arrowprops=dict(arrowstyle='->', color='#c1121f', lw=0.8))

ax_bot.set_xlim(-0.7, 2.7)
ax_bot.set_ylim(-0.5, T + tau + 0.4)
ax_bot.invert_yaxis()
ax_bot.set_xlabel('Position', fontsize=10)
ax_bot.set_ylabel('Time  (increasing downward)', fontsize=10)
ax_bot.set_title('Hidden Terminal: Space–Time Diagram\n'
                 'A and C both transmit; collision at B goes undetected',
                 fontsize=11, fontweight='bold')
ax_bot.set_xticks([x_A, x_B, x_C])
ax_bot.set_xticklabels(['A', 'B', 'C'], fontsize=11)
ax_bot.set_yticks([])

legend_handles = [
    mpatches.Patch(facecolor='#3a86ff', alpha=0.5, edgecolor='#023e8a', label="A's frame"),
    mpatches.Patch(facecolor='#e76f51', alpha=0.5, edgecolor='#9d0208', label="C's frame"),
    mpatches.Patch(facecolor='#c1121f', alpha=0.8, label='Collision zone at B'),
]
ax_bot.legend(handles=legend_handles, loc='lower right', fontsize=8.5)

plt.tight_layout()
plt.savefig(OUTDIR + 'hidden_terminal_spacetime.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved hidden_terminal_spacetime.png")
