"""Mininet: two hosts across a bottleneck link, iperf3 between them.

Topology:

    h1 ---- s1 ---- h2
       fast     bottleneck
     (100 Mb/s,  (10 Mb/s,
        1 ms)   20 ms, 1% loss)

The h1-s1 link is deliberately generous so that the h2-side link is the sole
constraint. The 20 ms one-way delay gives a 40 ms RTT: BDP is 10 Mb/s x 40 ms
= 50 KB ~= 35 MSS -- big enough for cwnd to grow, unlike the L21 loopback demo.

Run (in the ec441 VM):
    sudo python3 demo_mininet_bottleneck_l22.py
"""
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.log import setLogLevel


def main():
    setLogLevel("info")

    net = Mininet(controller=OVSController, link=TCLink)
    net.addController("c0")

    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    s1 = net.addSwitch("s1")

    net.addLink(h1, s1, bw=100, delay="1ms")
    net.addLink(s1, h2, bw=10, delay="20ms", loss=1)

    net.start()

    print("\n=== Sanity: h1 -> h2 ping ===")
    print(h1.cmd("ping -c 3 %s" % h2.IP()))

    print("\n=== iperf3 across the bottleneck (20 s) ===")
    h2.cmd("iperf3 -s -D")
    print(h1.cmd("iperf3 -c %s -t 20" % h2.IP()))

    print("\n=== ss -tipm on h1 immediately after ===")
    print(h1.cmd("ss -tipm"))

    net.stop()


if __name__ == "__main__":
    main()
