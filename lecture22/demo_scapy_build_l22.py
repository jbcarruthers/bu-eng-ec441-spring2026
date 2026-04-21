"""Scapy: build and inspect a packet without sending it.

Run (in the ec441 VM):
    sudo python3 demo_scapy_build_l22.py
"""
from scapy.all import IP, ICMP


def main():
    pkt = IP(dst="8.8.8.8") / ICMP()

    print("=== Scapy's view ===")
    pkt.show()

    raw = bytes(pkt)
    print(f"\nTotal length on the wire: {len(raw)} bytes")
    print(f"First 20 bytes (IP header): {raw[:20].hex(' ')}")
    print(f"Last 8 bytes  (ICMP Echo ): {raw[-8:].hex(' ')}")

    print("\nKey fields filled in by defaults:")
    print(f"  version = {pkt.version}")
    print(f"  ihl     = {pkt.ihl}   (header length in 32-bit words)")
    print(f"  ttl     = {pkt.ttl}  (Linux default; Windows defaults to 128)")
    print(f"  proto   = {pkt.proto} (1 = ICMP)")


if __name__ == "__main__":
    main()
