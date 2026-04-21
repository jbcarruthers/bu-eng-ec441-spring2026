"""Minimal TCP echo client. Pairs with demo_tcp_echo_server_l22.py."""
import socket

HOST, PORT = "127.0.0.1", 5001


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"hello from ec441\n")
        reply = s.recv(1024)
        print("server echoed:", reply)


if __name__ == "__main__":
    main()
