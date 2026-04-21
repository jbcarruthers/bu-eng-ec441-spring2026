"""Scapy: TCP SYN probe against a closed port and an open port.

scanme.nmap.org is maintained by the nmap project as a legal target for
learners. Do NOT point this script at hosts you do not own or have written
permission to scan.

Run (in the ec441 VM):
    sudo python3 demo_scapy_syn_l22.py
"""
from scapy.all import IP, TCP, sr1, RandShort


def probe(host: str, port: int):
    pkt = IP(dst=host) / TCP(dport=port, flags="S", sport=RandShort())
    reply = sr1(pkt, timeout=2, verbose=0)

    if reply is None:
        print(f"  {host}:{port:<5}  no reply (filtered?)")
        return

    flags = reply.sprintf("%TCP.flags%")
    if flags == "SA":
        print(f"  {host}:{port:<5}  SYN-ACK  -> open")
    elif "R" in flags:
        print(f"  {host}:{port:<5}  RST      -> closed")
    else:
        print(f"  {host}:{port:<5}  flags={flags}")


def main():
    host = "scanme.nmap.org"
    print(f"TCP SYN probes against {host}:")
    probe(host, 80)    # expected: open
    probe(host, 22)    # expected: open (ssh)
    probe(host, 81)    # expected: closed


if __name__ == "__main__":
    main()
