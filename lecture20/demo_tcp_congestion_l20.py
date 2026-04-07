"""
demo_tcp_congestion_l20.py
==========================
EC 441 – Introduction to Computer Networking
Lecture 20: TCP Part 2 — Congestion Control and the Modern Picture
Boston University, Spring 2026

Three standalone demonstrations:
  1. TCP Congestion Control Simulator — cwnd/ssthresh trace through slow start,
     congestion avoidance, fast recovery, and timeout
  2. TCP Throughput Formula — BW vs. RTT and loss rate; required loss rate for
     a target throughput on high-speed paths
  3. AIMD Fairness — two competing flows converging to equal bandwidth shares

No external libraries required — stdlib only.
Run with:  python -u demo_tcp_congestion_l20.py
"""

import math

SEP = "-" * 65


# ──────────────────────────────────────────────────────────────────────
# 1. TCP Congestion Control Simulator
# ──────────────────────────────────────────────────────────────────────
print(SEP)
print("1. TCP Congestion Control Simulator")
print(SEP)
print()
print("  Rules:")
print("    Slow Start (cwnd < ssthresh):   cwnd doubles each RTT (+1 MSS per ACK)")
print("    Congestion Avoidance (cwnd >= ssthresh): cwnd += 1 MSS per RTT")
print("    3 dup ACKs → Fast Recovery:     ssthresh = cwnd//2; cwnd = ssthresh")
print("    Timeout → Slow Start restart:   ssthresh = cwnd//2; cwnd = 1")
print()


def simulate_cc(label, ssthresh_init, n_rounds, loss_events):
    """
    Simulate TCP Reno congestion control.

    Parameters
    ----------
    label         : description string
    ssthresh_init : initial ssthresh value (MSS)
    n_rounds      : number of transmission rounds to simulate
    loss_events   : dict mapping round → 'dup' | 'timeout'

    Prints a round-by-round trace and returns the final cwnd list.
    """
    print(f"  === {label} ===")
    print(f"  ssthresh₀ = {ssthresh_init} MSS")
    print()
    print(f"  {'Round':>5}  {'cwnd':>5}  {'ssthresh':>8}  {'Phase':<20}  {'Event'}")
    print(f"  {'-----':>5}  {'----':>5}  {'--------':>8}  {'-----':<20}  {'-----'}")

    cwnd     = 1
    ssthresh = ssthresh_init

    cwnd_history = []

    for rnd in range(1, n_rounds + 1):
        # Apply loss event BEFORE this round's growth
        event_label = ""
        if rnd in loss_events:
            kind = loss_events[rnd]
            if kind == "dup":
                ssthresh = max(cwnd // 2, 1)
                cwnd     = ssthresh
                event_label = "← 3 dup ACKs (fast recovery)"
            elif kind == "timeout":
                ssthresh = max(cwnd // 2, 1)
                cwnd     = 1
                event_label = "← timeout → restart SS"

        phase = "Slow Start" if cwnd < ssthresh else "Congestion Avoidance"
        print(f"  {rnd:>5}  {cwnd:>5}  {ssthresh:>8}  {phase:<20}  {event_label}")
        cwnd_history.append(cwnd)

        # Grow for next round
        if cwnd < ssthresh:
            cwnd = min(cwnd * 2, ssthresh)   # exponential, cap at ssthresh
        else:
            cwnd += 1                         # linear +1 MSS/RTT

    print()
    return cwnd_history


# Scenario A: 3 dup ACKs only
simulate_cc(
    "Scenario A: 3 dup ACKs at round 9 (ssthresh₀=16)",
    ssthresh_init=16,
    n_rounds=20,
    loss_events={9: "dup"},
)

# Scenario B: timeout only
simulate_cc(
    "Scenario B: Timeout at round 9 (ssthresh₀=16)",
    ssthresh_init=16,
    n_rounds=20,
    loss_events={9: "timeout"},
)

# Scenario C: textbook trace from master outline — dup then timeout
simulate_cc(
    "Scenario C: 3 dup ACKs at round 9, timeout at round 17 (ssthresh₀=8)",
    ssthresh_init=8,
    n_rounds=25,
    loss_events={9: "dup", 17: "timeout"},
)

print("  Key observations:")
print("  • Fast recovery (3 dup ACKs) keeps cwnd at ssthresh — avoids slow start.")
print("  • Timeout is severe: cwnd drops to 1, slow start restarts from scratch.")
print("  • After each loss, ssthresh = cwnd/2 records 'where the trouble was'.")
print("  • CA growth is linear (+1/RTT) — the 'additive' in AIMD.")
print("  • Loss response halves cwnd — the 'multiplicative' in AIMD.")
print()


# ──────────────────────────────────────────────────────────────────────
# 2. TCP Throughput Formula
# ──────────────────────────────────────────────────────────────────────
print(SEP)
print("2. TCP Throughput Formula")
print(SEP)
print()
print("  BW ≈ (MSS / RTT) × (1 / √p)     [Mathis et al. 1997]")
print()
print("  where  p   = packet loss probability")
print("         MSS = maximum segment size (bytes)")
print("         RTT = round-trip time (seconds)")
print()
print("  Key insight: throughput ∝ 1/RTT and ∝ 1/√p")
print("  Long-RTT paths and high-loss paths both suffer severely.")
print()

MSS_BYTES = 1460    # bytes — Ethernet MSS (1500 - 20 IP - 20 TCP)
MSS_BITS  = MSS_BYTES * 8


def tcp_throughput_mbps(mss_bits, rtt_s, p):
    """TCP Reno throughput formula in Mb/s."""
    if p <= 0:
        return float("inf")
    return (mss_bits / rtt_s) * (1.0 / math.sqrt(p)) / 1e6


def required_loss_rate(mss_bits, rtt_s, target_mbps):
    """Loss rate required to achieve target throughput."""
    target_bps = target_mbps * 1e6
    return (mss_bits / (rtt_s * target_bps)) ** 2


# Table: BW vs. loss rate for several RTTs
print(f"  MSS = {MSS_BYTES} bytes = {MSS_BITS} bits")
print()
print("  --- Throughput vs. Loss Rate (Mb/s) ---")
print()

rtts_ms = [10, 50, 100, 300]
loss_rates = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.05, 0.10]

header = f"  {'Loss p':>10}" + "".join(f"  {'RTT='+str(r)+'ms':>12}" for r in rtts_ms)
print(header)
print("  " + "-" * (10 + 14 * len(rtts_ms)))

for p in loss_rates:
    row = f"  {p:>10.2e}"
    for rtt_ms in rtts_ms:
        bw = tcp_throughput_mbps(MSS_BITS, rtt_ms / 1000.0, p)
        if bw >= 1e6:
            row += f"  {'> 1 Tb/s':>12}"
        elif bw >= 1000:
            row += f"  {bw/1000:>9.1f} Gb/s"
        elif bw >= 1:
            row += f"  {bw:>9.1f} Mb/s"
        else:
            row += f"  {bw*1000:>9.2f} kb/s"
    print(row)

print()

# Required loss rate for high-speed paths
print("  --- Required Loss Rate for Target Throughput ---")
print()
print(f"  MSS = {MSS_BYTES} bytes")
print()

targets = [
    ("100 Mb/s",  100,    [10, 50, 100]),
    ("1 Gb/s",   1000,    [10, 50, 100]),
    ("10 Gb/s",  10000,   [10, 50, 100]),
    ("100 Gb/s", 100000,  [10, 50, 100]),
]

print(f"  {'Target BW':>12}  {'RTT (ms)':>9}  {'Required p':>14}  {'1 loss per N segs':>20}")
print(f"  {'----------':>12}  {'--------':>9}  {'----------':>14}  {'------------------':>20}")

for label, target_mbps, rtt_list in targets:
    for rtt_ms in rtt_list:
        p = required_loss_rate(MSS_BITS, rtt_ms / 1000.0, target_mbps)
        n_segs = int(1.0 / p) if p > 0 else float("inf")
        print(f"  {label:>12}  {rtt_ms:>9}  {p:>14.3e}  {n_segs:>20,}")
    print()

print("  Striking result: to sustain 10 Gb/s over a 100 ms RTT, TCP Reno")
print("  requires fewer than 1 loss per ~7 billion segments.")
print("  This is why high-speed TCP variants (CUBIC, BBR) and explicit")
print("  congestion control (ECN) exist.")
print()

# BDP and window scaling
print("  --- Bandwidth-Delay Product and Window Scaling ---")
print()
print("  BDP = BW × RTT = bytes needed in flight to fill the pipe")
print("  TCP Window Size field: 16 bits → max 64 KB without options")
print()
print(f"  {'BW':>10}  {'RTT (ms)':>9}  {'BDP':>12}  {'64 KB util':>12}  {'wscale needed':>14}")
print(f"  {'--':>10}  {'--------':>9}  {'---':>12}  {'----------':>12}  {'-------------':>14}")

bdp_cases = [
    (100e6,   10,  "100 Mb/s",  "10 ms"),
    (1e9,     50,  "1 Gb/s",    "50 ms"),
    (1e9,    100,  "1 Gb/s",    "100 ms"),
    (10e9,   100,  "10 Gb/s",   "100 ms"),
    (100e9,   10,  "100 Gb/s",  "10 ms"),
]

for bw_bps, rtt_ms, bw_label, rtt_label in bdp_cases:
    rtt_s   = rtt_ms / 1000.0
    bdp_b   = bw_bps * rtt_s              # bytes
    max_win = 65535                        # 64 KB − 1
    util    = min(max_win / bdp_b, 1.0)   # fraction of pipe filled
    # Window Scale: need 2^n × 64 KB ≥ BDP
    n = 0
    while (65535 * (2 ** n)) < bdp_b and n < 14:
        n += 1
    if bdp_b < 65535:
        wscale_str = "none needed"
    else:
        wscale_str = f"n={n} (×{2**n})"

    if bdp_b >= 1e9:
        bdp_str = f"{bdp_b/1e9:.1f} GB"
    elif bdp_b >= 1e6:
        bdp_str = f"{bdp_b/1e6:.1f} MB"
    else:
        bdp_str = f"{bdp_b/1e3:.0f} KB"

    print(f"  {bw_label:>10}  {rtt_label:>9}  {bdp_str:>12}  {util:>11.2%}  {wscale_str:>14}")

print()
print("  Without Window Scale, a 10 Gb/s × 100 ms path can use only ~0.005%")
print("  of its capacity — the pipe is almost entirely empty.")
print()


# ──────────────────────────────────────────────────────────────────────
# 3. AIMD Fairness
# ──────────────────────────────────────────────────────────────────────
print(SEP)
print("3. AIMD Fairness")
print(SEP)
print()
print("  Two TCP flows share a single bottleneck link of capacity C.")
print("  AIMD rule each round:")
print("    - Both flows: rate += Δ  (additive increase)")
print("    - If rate₁ + rate₂ > C: both halve  (multiplicative decrease)")
print()
print("  Claim: the operating point (rate₁, rate₂) converges to (C/2, C/2).")
print()


def simulate_aimd(label, capacity, r1_init, r2_init, delta, n_steps):
    """
    Simulate AIMD for two flows sharing a bottleneck.

    Parameters
    ----------
    capacity : link capacity (Mb/s)
    r1_init  : flow 1 initial rate (Mb/s)
    r2_init  : flow 2 initial rate (Mb/s)
    delta    : additive increase step (Mb/s)
    n_steps  : number of AIMD rounds
    """
    print(f"  === {label} ===")
    print(f"  C={capacity} Mb/s, Δ={delta} Mb/s")
    print(f"  Initial: flow1={r1_init} Mb/s, flow2={r2_init} Mb/s  "
          f"(total={r1_init+r2_init}, fair share={capacity/2})")
    print()
    print(f"  {'Step':>5}  {'Flow 1':>8}  {'Flow 2':>8}  {'Total':>8}  "
          f"{'Util':>7}  {'|F1−F2|':>8}  {'Event'}")
    print(f"  {'----':>5}  {'------':>8}  {'------':>8}  {'-----':>8}  "
          f"{'----':>7}  {'-------':>8}  {'-----'}")

    r1, r2 = float(r1_init), float(r2_init)

    # Print every Nth step to keep output readable
    print_every = max(1, n_steps // 20)

    for step in range(1, n_steps + 1):
        # Additive increase
        r1 += delta
        r2 += delta
        event = "AI"

        # Multiplicative decrease if over capacity
        if r1 + r2 > capacity:
            r1 /= 2.0
            r2 /= 2.0
            event = "AI → MD"

        if step % print_every == 0 or step == 1 or step == n_steps:
            util = (r1 + r2) / capacity
            gap  = abs(r1 - r2)
            print(f"  {step:>5}  {r1:>8.2f}  {r2:>8.2f}  {r1+r2:>8.2f}  "
                  f"{util:>7.1%}  {gap:>8.2f}  {event}")

    print()
    print(f"  After {n_steps} steps:")
    print(f"    Flow 1: {r1:.3f} Mb/s   Flow 2: {r2:.3f} Mb/s")
    print(f"    Ideal:  {capacity/2:.3f} Mb/s each")
    print(f"    Fairness gap |F1−F2| = {abs(r1-r2):.3f} Mb/s  "
          f"({'converged' if abs(r1-r2) < 0.1*capacity else 'converging'})")
    print(f"    Utilization: {(r1+r2)/capacity:.1%}")
    print()


# Scenario A: very unequal start
simulate_aimd(
    "Scenario A: unequal start (10 + 80 Mb/s), C=100 Mb/s, Δ=5",
    capacity=100,
    r1_init=10,
    r2_init=80,
    delta=5,
    n_steps=60,
)

# Scenario B: both starting below capacity, Δ=2
simulate_aimd(
    "Scenario B: both start low (5 + 5 Mb/s), C=100 Mb/s, Δ=2",
    capacity=100,
    r1_init=5,
    r2_init=5,
    delta=2,
    n_steps=60,
)

# Scenario C: one greedy, one polite, fine-grained Δ
simulate_aimd(
    "Scenario C: very unequal (1 + 95 Mb/s), C=100 Mb/s, Δ=1",
    capacity=100,
    r1_init=1,
    r2_init=95,
    delta=1,
    n_steps=80,
)

print("  Key observations:")
print("  • Both flows converge to C/2 regardless of starting point.")
print("  • AI moves along (1,1) direction — parallel to the fairness line;")
print("    gap |F1−F2| does NOT change during AI.")
print("  • MD halves both rates → ratio F1/F2 is preserved, but the point")
print("    moves toward the origin, which is closer to the fairness line")
print("    (geometrically: the fairness gap shrinks relative to the capacity).")
print("  • Combined AI+MD spirals toward the intersection of the efficiency")
print("    line (F1+F2=C) and the fairness line (F1=F2) at (C/2, C/2).")
print()
print("  Caveat: this assumes equal RTTs. Reno gives shorter-RTT flows more")
print("  AIMD steps per second. CUBIC uses wall-clock time and is RTT-independent.")
