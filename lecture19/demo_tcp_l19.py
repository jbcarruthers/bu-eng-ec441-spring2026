"""
demo_tcp_l19.py
===============
EC 441 – Introduction to Computer Networking
Lecture 19: TCP Part 1 — Connections, Sequencing, and Flow Control
Boston University, Spring 2026

Three standalone demonstrations:
  1. TCP RTT Estimator — EWMA + RTTVAR + RTO (RFC 6298) across network scenarios
  2. TCP 3-Way Handshake — ISN arithmetic, seq/ACK number trace
  3. Flow Control — receive window (rwnd) / bytes-in-flight interaction

No external libraries required — stdlib only.
Run with:  python -u demo_tcp_l19.py
"""

import random

SEP = "-" * 65


# ──────────────────────────────────────────────────────────────────────
# 1. TCP RTT Estimator  (RFC 6298  /  Jacobson 1988)
# ──────────────────────────────────────────────────────────────────────
print(SEP)
print("1. TCP RTT Estimator: EWMA + RTTVAR + RTO  (RFC 6298)")
print(SEP)
print()
print("  SRTT   ← (1 − α) · SRTT   + α · R          α = 1/8")
print("  RTTVAR ← (1 − β) · RTTVAR + β · |SRTT − R| β = 1/4")
print("  RTO    = SRTT + 4 · RTTVAR")
print()
print("  SRTT is a first-order IIR low-pass filter.")
print("  Time constant ≈ 1/α = 8 samples;  α = 1/8 = 2⁻³ (right-shift on hardware).")
print("  RTTVAR tracks mean absolute deviation — a noise-power estimator.")
print("  RTO = SRTT + 4·RTTVAR is a confidence-interval bound.")
print()

ALPHA = 1 / 8   # EWMA weight for mean
BETA  = 1 / 4   # EWMA weight for variance


def run_rtt_estimator(label, rtt_samples, srtt0=None, rttvar0=None):
    """
    Simulate the RFC 6298 RTT estimator over a list of RTT samples.

    Initialization (RFC 6298 §2.2):
      After first measurement R:
        SRTT   = R
        RTTVAR = R / 2
        RTO    = SRTT + 4·RTTVAR = 3·R

    Parameters
    ----------
    label       : description string
    rtt_samples : list of RTT measurements in ms
    srtt0       : override initial SRTT (None = use first sample)
    rttvar0     : override initial RTTVAR (None = use first_sample/2)

    Returns final (srtt, rttvar, rto).
    """
    print(f"  === {label} ===")
    print(f"  {'Sample':>6}  {'R (ms)':>8}  {'SRTT':>8}  {'RTTVAR':>8}  "
          f"{'RTO formula':>12}  {'Note'}")
    print(f"  {'------':>6}  {'------':>8}  {'----':>8}  {'------':>8}  "
          f"{'(pre-floor)':>12}  {'----'}")

    srtt   = srtt0
    rttvar = rttvar0

    for i, r in enumerate(rtt_samples):
        if srtt is None:
            # First measurement: RFC 6298 §2.2 initialization
            srtt   = r
            rttvar = r / 2.0
        else:
            # RFC 6298 §2.3: RTTVAR updated using OLD srtt
            rttvar = (1 - BETA) * rttvar + BETA * abs(srtt - r)
            srtt   = (1 - ALPHA) * srtt  + ALPHA * r

        rto_raw = srtt + 4 * rttvar
        rto = max(rto_raw, 1000.0)   # RFC 6298: RTO floor = 1 s (1000 ms)

        note = ""
        if i == 0 and srtt0 is None:
            note = "← init"
        elif r > srtt + 2 * rttvar:
            note = "← spike"
        elif abs(r - srtt) < 2:
            note = "← stable"

        print(f"  {i+1:>6}  {r:>8.1f}  {srtt:>8.2f}  {rttvar:>8.2f}  "
              f"{rto_raw:>12.2f}  {note}")

    print()
    rto_formula = srtt + 4 * rttvar
    floor_note = f"  → effective RTO = {rto:.0f} ms  (RFC 6298 floor: max(formula, 1000 ms))" \
                 if rto > rto_formula else ""
    print(f"  Final:  SRTT = {srtt:.2f} ms,  RTTVAR = {rttvar:.2f} ms,  "
          f"RTO formula = {rto_formula:.2f} ms")
    if floor_note:
        print(floor_note)
    print()
    return srtt, rttvar, rto


# Scenario A: stable low-variance network
print("  Scenario A — Stable campus network (~100 ms, low variance)")
print()
run_rtt_estimator(
    "Stable: RTT ≈ 100 ms, σ ≈ 3 ms",
    [102, 98, 101, 100, 99, 103, 97, 101, 100, 102],
)

# Scenario B: step change (e.g., congestion kicks in, then clears)
print("  Scenario B — Step change: 50 ms → 200 ms → 50 ms")
print()
run_rtt_estimator(
    "Step change — slow filter response visible",
    [50, 50, 50, 200, 200, 200, 200, 50, 50, 50],
)

# Scenario C: periodic spikes (packet reordering or occasional queuing)
print("  Scenario C — Periodic spikes every 3rd sample")
print()
rng = random.Random(7)
spike_samples = [
    rng.gauss(80, 5) if (i % 3 != 0) else rng.gauss(300, 20)
    for i in range(12)
]
run_rtt_estimator(
    "Periodic spikes — RTTVAR rises, widens RTO safety margin",
    [round(x, 1) for x in spike_samples],
)

# Scenario D: the worked example from the lecture notes
print("  Scenario D — Lecture worked example  (SRTT₀=100, RTTVAR₀=10, R=150)")
print()
srtt, rttvar, rto = run_rtt_estimator(
    "Single sample: R = 150 ms",
    [150],
    srtt0=100.0,
    rttvar0=10.0,
)
print(f"  Formula check (pre-floor): SRTT=106.25, RTTVAR=20.00, "
      f"SRTT+4·RTTVAR=186.25  "
      f"({'PASS' if abs(srtt - 106.25) < 0.01 and abs(rttvar - 20.0) < 0.01 else 'FAIL'})")
print("  (RFC 6298 floor of 1000 ms applies here — formula value 186.25 < 1000)")
print()

# Show Karn's algorithm summary
print("  Karn's Algorithm:")
print("    When a retransmit occurs, the arriving ACK is ambiguous —")
print("    it could ACK the original or the retransmitted copy.")
print("    Rule: do NOT update SRTT/RTTVAR from any ACK following a retransmit.")
print("    Also: RTO ← 2 × RTO on each consecutive timeout (exponential backoff).")
print("    TCP Timestamps option (RFC 1323) removes the ambiguity entirely.")
print()

# Show exponential backoff table
print("  Exponential Backoff (consecutive timeouts, starting from 200 ms):")
print(f"  {'Timeout #':>10}  {'RTO (ms)':>10}")
print(f"  {'----------':>10}  {'--------':>10}")
rto = 200.0
for n in range(1, 8):
    print(f"  {n:>10}  {rto:>10.0f}")
    rto = min(rto * 2, 120_000.0)   # max ~120 s in Linux
print()


# ──────────────────────────────────────────────────────────────────────
# 2. TCP 3-Way Handshake and Teardown
# ──────────────────────────────────────────────────────────────────────
print(SEP)
print("2. TCP 3-Way Handshake and Teardown")
print(SEP)
print()
print("  Notation:  seq=X means the segment's Sequence Number field is X.")
print("             ack=Y means the Acknowledgment Number field is Y")
print("             (= 'send me byte Y next' = all bytes through Y−1 received).")
print("  SYN and FIN each consume one sequence number.")
print()


def tcp_handshake(client_isn, server_isn, data_bytes_c_to_s, data_bytes_s_to_c):
    """
    Trace a TCP connection: 3-way handshake, data exchange, and FIN teardown.

    client_isn        : client's initial sequence number
    server_isn        : server's initial sequence number
    data_bytes_c_to_s : bytes sent by client → server (one segment)
    data_bytes_s_to_c : bytes sent by server → client (one segment)
    """
    c_seq = client_isn
    s_seq = server_isn

    print(f"  Client ISN = {client_isn:,}   Server ISN = {server_isn:,}")
    print()
    print(f"  {'Step':<4}  {'Direction':<16}  {'Flags':<14}  {'seq':>12}  "
          f"{'ack':>12}  {'len':>5}  Meaning")
    print(f"  {'----':<4}  {'----------':<16}  {'-----':<14}  {'---':>12}  "
          f"{'---':>12}  {'---':>5}")

    def row(step, direction, flags, seq, ack, length, note):
        ack_str = f"{ack:,}" if ack is not None else "—"
        print(f"  {step:<4}  {direction:<16}  {flags:<14}  {seq:>12,}  "
              f"{ack_str:>12}  {length:>5}  {note}")

    # ── Handshake ──────────────────────────────────────────────────────
    # SYN
    row(1, "C → S", "SYN", c_seq, None, 0,
        "Client: 'I exist; my starting seq is this'")
    c_seq_after_syn = c_seq + 1      # SYN consumes one seq number

    # SYN-ACK
    row(2, "S → C", "SYN, ACK", s_seq, c_seq_after_syn, 0,
        "Server: 'OK; my starting seq is this; I expect your byte %s next'" % f"{c_seq_after_syn:,}")
    s_seq_after_syn = s_seq + 1

    # ACK
    row(3, "C → S", "ACK", c_seq_after_syn, s_seq_after_syn, 0,
        "Client: 'Received your SYN; connection ESTABLISHED'")
    print()
    print(f"  ── ESTABLISHED ── client next_seq={c_seq_after_syn:,}  "
          f"server next_seq={s_seq_after_syn:,}")
    print()

    c_next = c_seq_after_syn
    s_next = s_seq_after_syn

    # ── Data exchange ──────────────────────────────────────────────────
    # Client sends data
    row(4, "C → S", "ACK, PSH", c_next, s_next, data_bytes_c_to_s,
        f"Client sends {data_bytes_c_to_s} bytes")
    c_next += data_bytes_c_to_s

    # Server ACKs client's data
    row(5, "S → C", "ACK", s_next, c_next, 0,
        f"Server ACKs all {data_bytes_c_to_s} bytes (cumulative)")

    # Server sends data
    row(6, "S → C", "ACK, PSH", s_next, c_next, data_bytes_s_to_c,
        f"Server sends {data_bytes_s_to_c} bytes")
    s_next += data_bytes_s_to_c

    # Client ACKs server's data
    row(7, "C → S", "ACK", c_next, s_next, 0,
        f"Client ACKs all {data_bytes_s_to_c} bytes (cumulative)")
    print()
    print(f"  ── data exchange complete ── "
          f"client delivered {data_bytes_c_to_s} B,  server delivered {data_bytes_s_to_c} B")
    print()

    # ── Teardown (client initiates) ────────────────────────────────────
    # FIN from client
    row(8, "C → S", "FIN, ACK", c_next, s_next, 0,
        "Client: 'Done sending; half-close client→server'")
    c_next += 1    # FIN consumes one seq number

    # Server ACKs FIN
    row(9, "S → C", "ACK", s_next, c_next, 0,
        "Server ACKs client FIN (client enters FIN_WAIT_2)")

    # Server sends its own FIN (often combined with ACK above in practice)
    row(10, "S → C", "FIN, ACK", s_next, c_next, 0,
        "Server: 'Also done sending; half-close server→client'")
    s_next += 1

    # Client ACKs server FIN — enters TIME_WAIT
    row(11, "C → S", "ACK", c_next, s_next, 0,
        "Client ACKs server FIN → enters TIME_WAIT (2×MSL ≈ 2–4 min)")
    print()
    print("  ── TIME_WAIT ── client waits 2×MSL before releasing port/5-tuple")
    print("     Reason 1: final ACK (step 11) may be lost → server retransmits FIN")
    print("     Reason 2: stale segments from this 5-tuple must expire before reuse")
    print()


tcp_handshake(
    client_isn=1_000_000,
    server_isn=4_000_000,
    data_bytes_c_to_s=500,
    data_bytes_s_to_c=1460,
)

# ISN randomization note
print("  ISN Randomization:")
print("    ISNs are chosen pseudo-randomly (not starting at 0 or 1).")
print("    Linux: ISN = MD5(src IP, dst IP, ports, key, timestamp)")
print("    Reason 1 — stale segment prevention: a new connection on the same")
print("      5-tuple must not accidentally accept a segment from the old connection.")
print("    Reason 2 — security: predictable ISNs enable TCP sequence prediction")
print("      attacks (hijack a connection without seeing its packets).")
print()


# ──────────────────────────────────────────────────────────────────────
# 3. Flow Control: Receive Window (rwnd)
# ──────────────────────────────────────────────────────────────────────
print(SEP)
print("3. Flow Control: Receive Window (rwnd)")
print(SEP)
print()
print("  Constraint: bytes_in_flight ≤ rwnd")
print("  rwnd = receiver's free buffer space, advertised in every ACK.")
print("  If rwnd = 0, sender stops and sends 1-byte zero-window probes.")
print()


def simulate_flow_control(buf_size, seg_size, app_read_bytes_per_round, n_rounds, seed=99):
    """
    Simulate TCP flow control over several rounds.

    Each round:
      1. Sender transmits as many full segments as rwnd allows (up to 3 per round).
      2. Receiver buffers the arriving bytes.
      3. Application reads `app_read_bytes_per_round` bytes from the buffer.
      4. rwnd is updated and advertised in the ACK.

    Parameters
    ----------
    buf_size               : receiver buffer capacity (bytes)
    seg_size               : segment size (bytes)
    app_read_bytes_per_round : bytes app consumes per round
    n_rounds               : number of rounds to simulate
    """
    print(f"  Buffer size:      {buf_size:>6,} bytes")
    print(f"  Segment size:     {seg_size:>6,} bytes")
    print(f"  App read/round:   {app_read_bytes_per_round:>6,} bytes")
    print()
    print(f"  {'Round':>5}  {'Sent (B)':>9}  {'Buffered':>9}  {'App read':>9}  "
          f"{'Free buf':>9}  {'rwnd':>9}  {'Status'}")
    print(f"  {'-----':>5}  {'-'*9}  {'-'*9}  {'-'*9}  {'-'*9}  {'-'*9}  {'------'}")

    buffered = 0
    stalls = 0

    for rnd in range(1, n_rounds + 1):
        rwnd = buf_size - buffered

        # How many segments can sender push this round?
        max_send = (rwnd // seg_size) * seg_size   # floor to segment boundary
        max_send = min(max_send, 3 * seg_size)     # cap at 3 segs/round for demo

        status = ""
        if rwnd == 0:
            max_send = 0
            status = "STALL (zero-window)"
            stalls += 1
        elif max_send == 0 and rwnd > 0:
            max_send = 0
            status = "window < 1 MSS"

        sent = max_send
        buffered = min(buffered + sent, buf_size)

        # App reads
        read = min(app_read_bytes_per_round, buffered)
        buffered -= read

        free = buf_size - buffered
        rwnd_next = free

        print(f"  {rnd:>5}  {sent:>9,}  {buffered:>9,}  {read:>9,}  "
              f"{free:>9,}  {rwnd_next:>9,}  {status}")

    print()
    print(f"  Rounds simulated: {n_rounds}   Zero-window stalls: {stalls}")
    print()


print("  --- Scenario A: App reads faster than data arrives (no stall) ---")
simulate_flow_control(
    buf_size=16_384,
    seg_size=1_460,
    app_read_bytes_per_round=4_380,   # reads 3 segments per round
    n_rounds=8,
)

print("  --- Scenario B: App reads slowly — buffer fills, sender stalls ---")
simulate_flow_control(
    buf_size=16_384,
    seg_size=1_460,
    app_read_bytes_per_round=500,     # app is slow
    n_rounds=12,
)

print()
print("  Key observations:")
print("  • rwnd shrinks as the buffer fills and grows as the app reads.")
print("  • When rwnd < 1 MSS the sender stops sending full segments.")
print("  • Zero window → sender sends 1-byte probes until rwnd opens.")
print("  • Flow control is purely receiver-driven (vs. congestion control,")
print("    which is network-driven — covered in L20).")
