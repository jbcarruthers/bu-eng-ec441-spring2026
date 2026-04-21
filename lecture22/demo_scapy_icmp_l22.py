"""Scapy: craft and send an ICMP Echo Request, inspect the Echo Reply.

Run (in the ec441 VM):
    sudo python3 demo_scapy_icmp_l22.py
"""
from scapy.all import IP, ICMP, sr1


def main(target: str = "8.8.8.8"):
    req = IP(dst=target) / ICMP()
    reply = sr1(req, timeout=2, verbose=0)

    if reply is None:
        print(f"No reply from {target} within 2 s")
        return

    print("=== Reply ===")
    reply.show()

    print(f"\nRequest TTL sent:   {req.ttl}")
    print(f"Reply    TTL got:   {reply.ttl}")
    print(f"ICMP type (0=Echo Reply): {reply[ICMP].type}")


if __name__ == "__main__":
    main()
