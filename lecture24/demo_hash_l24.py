"""EC 441 L24 -- hash function properties.

Demonstrates:
  1. Fixed output size regardless of input size.
  2. The avalanche effect: a one-bit input change flips ~half the output bits.
  3. A simple commitment scheme: publish h(secret), reveal secret later.

Uses Python's stdlib hashlib -- no extra libraries required.

Run:
    python3 demo_hash_l24.py
"""
import hashlib
import secrets


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hamming_bits(a: bytes, b: bytes) -> int:
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def demo_fixed_size():
    print("=== 1. Fixed output size ===")
    for msg in [b"", b"a", b"hello", b"x" * 1000, b"x" * 1_000_000]:
        h = sha256_hex(msg)
        print(f"  SHA-256({len(msg):>7d} B) = {h[:16]}... ({len(h)*4} bits)")


def demo_avalanche():
    print("\n=== 2. Avalanche effect ===")
    m1 = b"The quick brown fox jumps over the lazy dog"
    m2 = b"The quick brown fox jumps over the lazy dog."   # added a '.'
    h1 = hashlib.sha256(m1).digest()
    h2 = hashlib.sha256(m2).digest()
    flipped = hamming_bits(h1, h2)
    print(f"  m1: {m1!r}")
    print(f"  m2: {m2!r}")
    print(f"  SHA-256(m1) = {h1.hex()}")
    print(f"  SHA-256(m2) = {h2.hex()}")
    print(f"  Bits flipped: {flipped}/256 "
          f"(~{flipped/256*100:.1f}%, ideal is ~50%)")


def demo_commitment():
    print("\n=== 3. Commitment scheme ===")
    # alpha commits to a bid without revealing it.
    nonce = secrets.token_bytes(16)                 # blinds the commitment
    bid = b"$42"
    commitment = sha256_hex(nonce + bid)
    print(f"  alpha's bid    (hidden) : {bid!r}")
    print(f"  alpha publishes         : commitment = {commitment}")
    print(f"  (later) alpha reveals   : bid={bid!r}, nonce={nonce.hex()}")
    verify = sha256_hex(nonce + bid)
    print(f"  verifier recomputes     : {verify}")
    print(f"  match?                  : {verify == commitment}")
    print("  alpha cannot change the bid after committing -- that would")
    print("  require a hash collision (infeasible).")


def main():
    demo_fixed_size()
    demo_avalanche()
    demo_commitment()


if __name__ == "__main__":
    main()
