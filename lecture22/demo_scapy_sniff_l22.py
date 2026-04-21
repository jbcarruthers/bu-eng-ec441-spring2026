"""Scapy: sniff mode. Capture a few packets and summarize them.

Same underlying libpcap/BPF as pyshark and tcpdump -- different surface.
Use pyshark for large-scale read-only analysis; use Scapy when you want
to both capture AND craft in the same script.

Run (in the ec441 VM):
    sudo python3 demo_scapy_sniff_l22.py
"""
from scapy.all import sniff


def main():
    print("Sniffing 5 ICMP packets on 'any' interface...")
    print("(run `ping -c 5 8.8.8.8` in another shell to generate traffic)")
    pkts = sniff(filter="icmp", count=5, iface="any")
    print("\n=== Summary ===")
    pkts.summary()
    print("\n=== First packet in detail ===")
    pkts[0].show()


if __name__ == "__main__":
    main()
