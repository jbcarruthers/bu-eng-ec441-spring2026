"""Minimal UDP echo client. Pairs with demo_udp_echo_server_l22.py."""
import socket

HOST, PORT = "127.0.0.1", 5002


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b"hello udp from ec441\n", (HOST, PORT))
    data, addr = s.recvfrom(1024)
    print("server echoed:", data, "from", addr)
    s.close()


if __name__ == "__main__":
    main()
