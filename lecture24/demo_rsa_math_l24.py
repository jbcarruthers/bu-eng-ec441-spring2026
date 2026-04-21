"""EC 441 L24 -- RSA with small primes, end to end.

The point is to show the math, not real cryptography. Do NOT use this
code to protect anything.

Run:
    python3 demo_rsa_math_l24.py

The worked example from the lecture: p=11, q=13, e=7.
"""
from math import gcd


def egcd(a, b):
    """Extended Euclidean: returns (g, x, y) with g = gcd(a,b) = a*x + b*y."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def modinv(a, n):
    """Modular inverse of a mod n, or raise if gcd(a,n) != 1."""
    g, x, _ = egcd(a % n, n)
    if g != 1:
        raise ValueError(f"no inverse: gcd({a},{n}) = {g}")
    return x % n


def keygen(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError(f"e={e} not coprime to phi={phi}")
    d = modinv(e, phi)
    return (n, e), (n, d), phi


def encrypt(m, pub):
    n, e = pub
    return pow(m, e, n)


def decrypt(c, priv):
    n, d = priv
    return pow(c, d, n)


def sign(m, priv):
    # Textbook signing -- sign the integer directly. Real systems hash first
    # and use padding (RSA-PSS). Do not do this in production.
    return decrypt(m, priv)


def verify(sig, m, pub):
    return encrypt(sig, pub) == m


def main():
    # --- The lecture example -----------------------------------------------
    p, q, e = 11, 13, 7
    pub, priv, phi = keygen(p, q, e)
    n, _ = pub
    _, d = priv

    print("=== Key generation ===")
    print(f"  p = {p}, q = {q}")
    print(f"  n = p*q              = {n}")
    print(f"  phi = (p-1)*(q-1)    = {phi}")
    print(f"  e  (public exponent) = {e}")
    print(f"  d  (private exponent)= {d}     "
          f"(check: e*d mod phi = {(e * d) % phi})")

    m = 9
    print(f"\n=== Encrypt m = {m} ===")
    c = encrypt(m, pub)
    print(f"  c = m^e mod n = {m}^{e} mod {n} = {c}")

    print(f"\n=== Decrypt c = {c} ===")
    m2 = decrypt(c, priv)
    print(f"  m = c^d mod n = {c}^{d} mod {n} = {m2}")
    assert m2 == m

    print("\n=== Sign and verify ===")
    s = sign(m, priv)
    ok = verify(s, m, pub)
    print(f"  sig = m^d mod n            = {s}")
    print(f"  verify: sig^e mod n == m?  -> {ok}")
    assert ok

    # --- An adversary trying to forge a signature --------------------------
    print("\n=== A wrong signature fails verification ===")
    bad = (s + 1) % n
    print(f"  tampered signature {bad}: verify -> {verify(bad, m, pub)}")

    # --- A slightly bigger example ----------------------------------------
    print("\n=== A slightly bigger example ===")
    p2, q2, e2 = 101, 103, 11
    pub2, priv2, phi2 = keygen(p2, q2, e2)
    print(f"  p={p2}, q={q2}, n={pub2[0]}, phi={phi2}, "
          f"e={e2}, d={priv2[1]}")
    for mm in (42, 1234, 5555):
        cc = encrypt(mm, pub2)
        mm2 = decrypt(cc, priv2)
        print(f"  m={mm:5d} -> c={cc:5d} -> decrypt -> {mm2}")
        assert mm2 == mm


if __name__ == "__main__":
    main()
