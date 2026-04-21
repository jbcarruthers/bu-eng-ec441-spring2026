"""Minimal TCP echo server.

Run (in the ec441 VM):
    python3 demo_tcp_echo_server_l22.py

In another shell:
    python3 demo_tcp_echo_client_l22.py
"""
import socket

HOST, PORT = "127.0.0.1", 5001


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print(f"TCP echo server listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = srv.accept()
            with conn:
                print(f"connected: {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
                print(f"closed:    {addr}")
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
