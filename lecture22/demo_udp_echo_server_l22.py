"""Minimal UDP echo server.

Notice what is missing compared to the TCP version: no listen(), no accept(),
no per-connection socket. UDP is stateless at the socket layer -- every
datagram stands alone.

Run (in the ec441 VM):
    python3 demo_udp_echo_server_l22.py
"""
import socket

HOST, PORT = "127.0.0.1", 5002


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srv.bind((HOST, PORT))
    print(f"UDP echo server listening on {HOST}:{PORT}")

    try:
        while True:
            data, addr = srv.recvfrom(1024)
            print(f"{addr}: {data!r}")
            srv.sendto(data, addr)
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
