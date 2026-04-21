"""Scapy: minimal traceroute in ~10 lines.

Sends ICMP Echo Requests with increasing TTL. Each router that decrements
TTL to 0 replies with ICMP Time Exceeded (type 11). The destination, when
finally reached, replies with ICMP Echo Reply (type 0).

Run (in the ec441 VM):
    sudo python3 demo_scapy_traceroute_l22.py [dst]
"""
import sys
from scapy.all import IP, ICMP, sr1


def traceroute(dst: str, max_ttl: int = 20):
    print(f"traceroute to {dst}, max {max_ttl} hops")
    for ttl in range(1, max_ttl + 1):
        reply = sr1(IP(dst=dst, ttl=ttl) / ICMP(), timeout=2, verbose=0)
        if reply is None:
            print(f"  {ttl:2d}  *")
        elif reply[ICMP].type == 0:
            print(f"  {ttl:2d}  {reply.src}  (reached destination)")
            return
        else:
            print(f"  {ttl:2d}  {reply.src}")


if __name__ == "__main__":
    dst = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
    traceroute(dst)
