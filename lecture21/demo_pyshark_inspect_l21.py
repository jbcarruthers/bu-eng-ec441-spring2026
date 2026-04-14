"""
EC 441 — Lecture 21: See the Network
demo_pyshark_inspect_l21.py

Slide: "pyshark --- Inspect a Packet"

Load a pcap and print layer, IP fields, and transport protocol for the
first packet.  Field names match Wireshark exactly — if you can see it
in the GUI, you can read it here.

Usage:
    python -u demo_pyshark_inspect_l21.py capture.pcap
"""

import sys
import pyshark

pcap_file = sys.argv[1] if len(sys.argv) > 1 else "capture.pcap"

cap = pyshark.FileCapture(pcap_file)
pkt = next(iter(cap))
print(pkt.layers)            # all layers present
print(pkt.ip.src)            # source IP
print(pkt.ip.ttl)            # TTL from L17
print(pkt.transport_layer)   # TCP or UDP
