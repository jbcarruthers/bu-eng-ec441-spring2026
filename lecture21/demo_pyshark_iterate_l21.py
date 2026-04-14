"""
EC 441 — Lecture 21: See the Network
demo_pyshark_iterate_l21.py

Slide: "pyshark --- Load and Iterate"

Load a pcap file and print the highest-layer protocol and frame length
for every packet.

Usage (inside the ec441 VM or any host with pyshark installed):
    python -u demo_pyshark_iterate_l21.py capture.pcap
"""

import sys
import pyshark

pcap_file = sys.argv[1] if len(sys.argv) > 1 else "capture.pcap"

cap = pyshark.FileCapture(pcap_file)
for pkt in cap:
    print(pkt.highest_layer, pkt.length)
