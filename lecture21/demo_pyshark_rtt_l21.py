"""
EC 441 — Lecture 21: See the Network
demo_pyshark_rtt_l21.py

Slide: "pyshark --- Plot TCP RTT"

How did RTT evolve during a TCP connection?  Wireshark annotates each
ACK with the measured RTT (tcp.analysis.ack_rtt); this script collects
those values and plots them over time.

This is the raw RTT signal that TCP's EWMA smooths into srtt, and whose
variance (RTTVAR) sets the retransmission timeout (RTO).

Usage:
    python -u demo_pyshark_rtt_l21.py capture.pcap   # saves rtt_plot.png
"""

import sys
import pyshark
import matplotlib.pyplot as plt

pcap_file = sys.argv[1] if len(sys.argv) > 1 else "capture.pcap"

cap = pyshark.FileCapture(pcap_file, display_filter="tcp.analysis.ack_rtt")
times, rtts = [], []
for pkt in cap:
    try:
        times.append(float(pkt.sniff_timestamp))
        rtts.append(float(pkt.tcp.analysis_ack_rtt) * 1000)
    except AttributeError:
        pass

plt.plot(times, rtts, ".", markersize=3)
plt.xlabel("Time (s)")
plt.ylabel("RTT (ms)")
plt.title("TCP ACK RTT over time")
plt.tight_layout()
plt.savefig("rtt_plot.png")
print(f"Saved rtt_plot.png  ({len(times)} RTT samples)")
