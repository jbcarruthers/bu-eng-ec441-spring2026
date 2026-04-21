"""EC 441 L24 -- AES-GCM authenticated encryption.

AEAD = Authenticated Encryption with Associated Data.
Provides confidentiality AND integrity in one primitive -- this is what
TLS 1.3 uses.

Requires the `cryptography` package:
    pip install cryptography

Run:
    python3 demo_aes_gcm_l24.py
"""
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def main():
    # 256-bit key, shared between alpha and beta.
    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)

    msg = b"Meet at the cafe at 3pm. -- alpha"
    aad = b"ec441 demo header"     # "associated data" -- authenticated but not encrypted
    nonce = os.urandom(12)         # 96-bit nonce; MUST be unique per message with this key

    print("=== Encrypt ===")
    print(f"  key   = {key.hex()}")
    print(f"  nonce = {nonce.hex()}")
    print(f"  aad   = {aad!r}")
    print(f"  msg   = {msg!r}")

    ct = aes.encrypt(nonce, msg, aad)
    print(f"  ct    = {ct.hex()}  ({len(ct)} bytes)")
    print("         ^ last 16 bytes are the GCM authentication tag")

    print("\n=== Decrypt ===")
    pt = aes.decrypt(nonce, ct, aad)
    print(f"  plaintext = {pt!r}")
    assert pt == msg

    print("\n=== Integrity: tampered ciphertext fails ===")
    tampered = bytearray(ct)
    tampered[0] ^= 0x01             # flip one bit
    try:
        aes.decrypt(nonce, bytes(tampered), aad)
    except Exception as exc:
        print(f"  decrypt raised: {type(exc).__name__}: {exc}")

    print("\n=== Integrity: tampered AAD fails ===")
    try:
        aes.decrypt(nonce, ct, b"different header")
    except Exception as exc:
        print(f"  decrypt raised: {type(exc).__name__}: {exc}")

    print("\n=== Never reuse a (key, nonce) pair ===")
    print("  With GCM, reusing a nonce under the same key leaks plaintext")
    print("  XOR and can let an attacker forge tags. Derive fresh nonces per")
    print("  message -- TLS uses a counter embedded in the record layer.")


if __name__ == "__main__":
    main()
