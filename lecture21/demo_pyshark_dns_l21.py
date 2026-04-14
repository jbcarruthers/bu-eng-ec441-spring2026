"""
EC 441 — Lecture 21: See the Network
demo_pyshark_dns_l21.py

Slide: "pyshark --- Extract DNS Queries"

What domains did this machine look up?  Filter to DNS packets and
collect every query name, then print the unique set in sorted order.

Usage:
    python -u demo_pyshark_dns_l21.py capture.pcap
"""

import sys
import pyshark

pcap_file = sys.argv[1] if len(sys.argv) > 1 else "capture.pcap"

cap = pyshark.FileCapture(pcap_file, display_filter="dns")
queries = []
for pkt in cap:
    try:
        if hasattr(pkt.dns, "qry_name"):
            queries.append(pkt.dns.qry_name)
    except AttributeError:
        pass

for q in sorted(set(queries)):
    print(q)
