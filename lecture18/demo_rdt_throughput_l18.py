"""
demo_rdt_throughput_l18.py
==========================
EC 441 – Introduction to Computer Networking
Lecture 18: Transport Layer, UDP, and Reliable Data Transfer
Boston University, Spring 2026

Standalone demo illustrating reliable data transfer concepts:
  1. Bandwidth-delay product analysis across link types
  2. Stop-and-Wait event trace simulation (normal, data loss, ACK loss)
  3. Theoretical throughput vs. loss rate for S&W, GBN, and SR

No external libraries required — stdlib only.
Run with:  python -u demo_rdt_throughput_l18.py
"""

import math
import random

SEP = "-" * 65


# ──────────────────────────────────────────────────────────────────────
# 1. Bandwidth-Delay Product Analysis
# ──────────────────────────────────────────────────────────────────────
print(SEP)
print("1. Bandwidth-Delay Product and Stop-and-Wait Utilization")
print(SEP)
print()
print("  Stop-and-Wait utilization: U = t_tx / (RTT + t_tx)")
print("  where  t_tx = (packet_size × 8) / bandwidth")
print()

PACKET_SIZE_BYTES = 1500   # bytes (Ethernet MTU)
PACKET_BITS = PACKET_SIZE_BYTES * 8

link_types = [
    ("Local LAN",          1_000,  0.1),    # 1 Gb/s, 0.1 ms RTT
    ("Campus network",     1_000,  5.0),    # 1 Gb/s, 5 ms RTT
    ("Cross-country fiber",1_000, 40.0),    # 1 Gb/s, 40 ms RTT
    ("Geostationary sat.", 1_000,600.0),    # 1 Gb/s, 600 ms RTT
    ("Undersea cable",    10_000, 80.0),    # 10 Gb/s, 80 ms RTT
]

print(f"  Packet size: {PACKET_SIZE_BYTES} bytes = {PACKET_BITS:,} bits")
print()
print(f"  {'Link Type':<22}  {'BW (Mb/s)':>9}  {'RTT (ms)':>8}  "
      f"{'t_tx (µs)':>9}  {'BDP (pkts)':>10}  {'S&W Util':>8}")
print(f"  {'-'*22}  {'-'*9}  {'-'*8}  {'-'*9}  {'-'*10}  {'-'*8}")

for name, bw_mbps, rtt_ms in link_types:
    bw_bps = bw_mbps * 1e6
    rtt_s  = rtt_ms / 1000.0
    t_tx_s = PACKET_BITS / bw_bps
    t_tx_us = t_tx_s * 1e6

    bdp_bits    = bw_bps * rtt_s
    bdp_packets = bdp_bits / PACKET_BITS

    utilization = t_tx_s / (rtt_s + t_tx_s)

    print(f"  {name:<22}  {bw_mbps:>9,}  {rtt_ms:>8.1f}  "
          f"{t_tx_us:>9.3f}  {bdp_packets:>10.1f}  {utilization:>7.3%}")

print()
print("  Key takeaway:")
print("    On a geostationary satellite link (RTT = 600 ms, BW = 1 Gb/s),")
print(f"    Stop-and-Wait achieves only ~0.002% utilization.")
print(f"    The BDP is {1e9 * 0.6 / 1e6:.0f} Mb — the pipe holds {1e9 * 0.6 / PACKET_BITS:,.0f} packets.")
print(f"    The window must be at least that large to fill it.")


# ──────────────────────────────────────────────────────────────────────
# 2. Stop-and-Wait Event Trace Simulation
# ──────────────────────────────────────────────────────────────────────
print()
print(SEP)
print("2. Stop-and-Wait Event Trace (with sequence numbers)")
print(SEP)
print()

def simulate_saw(num_packets, p_data_loss, p_ack_loss, seed=42):
    """
    Simulate Stop-and-Wait ARQ for `num_packets` deliveries.

    Parameters
    ----------
    num_packets   : number of distinct data packets to deliver
    p_data_loss   : probability that a data packet is lost in transit
    p_ack_loss    : probability that an ACK is lost in transit

    Prints a step-by-step trace of events and returns the total number
    of transmissions used (including retransmits).
    """
    rng = random.Random(seed)
    seq = 0          # 1-bit sequence number (0 or 1)
    transmitted = 0  # total transmissions (new + retransmit)
    delivered = 0    # distinct packets delivered to the application

    print(f"  Delivering {num_packets} packets, "
          f"P(data loss)={p_data_loss:.0%}, P(ACK loss)={p_ack_loss:.0%}")
    print()

    pkt = 0   # packet index (0-based), not the seq num
    while delivered < num_packets:
        attempt = 1
        while True:
            transmitted += 1
            data_lost = rng.random() < p_data_loss
            if data_lost:
                print(f"  pkt {pkt}  seq={seq}  attempt {attempt}:  "
                      f"DATA LOST → timeout → retransmit")
                attempt += 1
                continue

            # Data arrived at receiver
            ack_lost = rng.random() < p_ack_loss
            if ack_lost:
                print(f"  pkt {pkt}  seq={seq}  attempt {attempt}:  "
                      f"data ok, ACK LOST → timeout → retransmit "
                      f"(receiver will see seq={seq} again → discard dup)")
                attempt += 1
                continue

            # Both data and ACK arrived
            if attempt == 1:
                print(f"  pkt {pkt}  seq={seq}  attempt {attempt}:  "
                      f"data ok, ACK ok → delivered ✓")
            else:
                print(f"  pkt {pkt}  seq={seq}  attempt {attempt}:  "
                      f"data ok, ACK ok → delivered ✓  (after {attempt} attempts)")
            break

        delivered += 1
        seq ^= 1   # flip the 1-bit sequence number
        pkt += 1

    efficiency = num_packets / transmitted
    print()
    print(f"  Packets to deliver:   {num_packets}")
    print(f"  Total transmissions:  {transmitted}  (includes retransmits)")
    print(f"  Delivery efficiency:  {efficiency:.1%}")
    return transmitted


print("  --- Scenario A: No loss ---")
simulate_saw(6, p_data_loss=0.0, p_ack_loss=0.0, seed=1)

print()
print("  --- Scenario B: 20% data loss, no ACK loss ---")
simulate_saw(6, p_data_loss=0.2, p_ack_loss=0.0, seed=2)

print()
print("  --- Scenario C: no data loss, 30% ACK loss ---")
simulate_saw(6, p_data_loss=0.0, p_ack_loss=0.3, seed=3)

print()
print("  --- Scenario D: 15% data loss, 15% ACK loss ---")
simulate_saw(6, p_data_loss=0.15, p_ack_loss=0.15, seed=4)


# ──────────────────────────────────────────────────────────────────────
# 3. Theoretical Throughput vs. Loss Rate: S&W, GBN, SR
# ──────────────────────────────────────────────────────────────────────
print()
print(SEP)
print("3. Theoretical Throughput vs. Loss Rate: S&W, GBN, SR")
print(SEP)
print()
print("  Assumes window is large enough to fill the pipe (utilization = 1 without loss).")
print("  p = probability a single transmitted packet is lost.")
print()
print("  Formulas:")
print("    S&W (N=1):   T = (1 − p)")
print("    GBN  (N):    T = (1 − p) / (1 + (N−1)·p)   [retransmit N on any loss]")
print("    SR   (N):    T = (1 − p)                     [retransmit only the lost pkt]")
print()
print("  Note: S&W and SR have the same delivery efficiency formula — the difference")
print("  is that SR achieves it with N packets in flight (high utilization), while")
print("  S&W needs N=1 (low utilization on high-BDP paths).")
print()


def throughput_sw(p):
    return 1.0 - p

def throughput_gbn(p, N):
    if p == 0:
        return 1.0
    return min(1.0, (1 - p) / (1 + (N - 1) * p))

def throughput_sr(p, N):
    # Same formula as S&W in terms of delivery efficiency (min with 1)
    return min(1.0, (1 - p))


loss_rates = [0.0, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
window_sizes = [4, 8, 16]

for N in window_sizes:
    print(f"  Window size N = {N}")
    print(f"  {'Loss p':>6}   {'S&W':>6}   {'GBN':>6}   {'SR':>6}   "
          f"{'GBN/SR ratio':>12}")
    print(f"  {'------':>6}   {'---':>6}   {'---':>6}   {'--':>6}   "
          f"{'------------':>12}")
    for p in loss_rates:
        t_sw  = throughput_sw(p)
        t_gbn = throughput_gbn(p, N)
        t_sr  = throughput_sr(p, N)
        ratio = t_gbn / t_sr if t_sr > 0 else 0.0
        print(f"  {p:>6.0%}   {t_sw:>6.3f}   {t_gbn:>6.3f}   {t_sr:>6.3f}   "
              f"{ratio:>12.3f}")
    print()

print("  Key observations:")
print("  • At p=0, all protocols achieve throughput=1.0 (no loss, full efficiency).")
print("  • As p increases, GBN degrades quickly — it retransmits the full window.")
print("  • SR's throughput equals S&W's delivery efficiency, but SR keeps the pipe")
print("    full because N packets are always in flight.")
print("  • At p=10%, N=8: GBN throughput ≈ 0.53, SR ≈ 0.90 — SR is 1.7× better.")
print()

# Find the crossover loss rate where GBN hits half of SR's throughput
print("  Loss rate at which GBN drops below half of SR (for each window size):")
print(f"  {'N':>4}   {'p (GBN = SR/2)':>16}")
print(f"  {'--':>4}   {'----------------':>16}")
for N in window_sizes:
    # GBN = SR/2  =>  (1-p)/(1+(N-1)*p) = (1-p)/2
    # => 1+(N-1)*p = 2  => (N-1)*p = 1  => p = 1/(N-1)
    if N > 1:
        p_cross = 1.0 / (N - 1)
        print(f"  {N:>4}   {p_cross:>15.1%}")
    else:
        print(f"  {N:>4}   (N=1: GBN = SR always)")
