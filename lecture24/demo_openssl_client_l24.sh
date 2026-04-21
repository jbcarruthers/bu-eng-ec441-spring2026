#!/usr/bin/env bash
# EC 441 L24 -- inspect a real TLS certificate chain with openssl.
#
# Works on macOS and Linux; no VM required.
# Uses the system openssl.
#
# Run:
#     bash demo_openssl_client_l24.sh

set -u

hr() { printf '\n==================================================\n%s\n==================================================\n' "$1"; }

HOST=${1:-bu.edu}
PORT=${2:-443}

hr "1. Connect and print the cert chain offered by $HOST"
echo | openssl s_client -connect "$HOST:$PORT" -servername "$HOST" \
    -showcerts 2>/dev/null | \
    grep -E '^(subject|issuer|depth|---)|^(Server certificate)' | head -40

hr "2. Just the leaf cert (decoded)"
echo | openssl s_client -connect "$HOST:$PORT" -servername "$HOST" \
    2>/dev/null | \
    openssl x509 -noout -subject -issuer -startdate -enddate -ext subjectAltName 2>/dev/null

hr "3. Cipher and TLS version negotiated"
echo | openssl s_client -connect "$HOST:$PORT" -servername "$HOST" \
    2>/dev/null | \
    grep -E '^(New|Protocol|Cipher|Server Temp Key|Verification)' | head -10

hr "4. Force TLS 1.3 and observe the handshake"
echo | openssl s_client -connect "$HOST:$PORT" -servername "$HOST" \
    -tls1_3 2>/dev/null | \
    grep -E '^(New|Protocol|Cipher|Server Temp Key|Verification)' | head -10

hr "5. Try an expired-cert test site (should fail)"
echo | openssl s_client -connect expired.badssl.com:443 \
    -servername expired.badssl.com 2>&1 | \
    grep -E 'verify (return|error)' | head -5

cat <<EOF

Things to look for in the output above:
  - the chain "depth" counter: depth=0 is the leaf cert, higher numbers
    are intermediate CAs, up to a root in your local trust store
  - the subject/issuer lines: who it is for, who signed it
  - "Server Temp Key": the ephemeral DH share for this session
    (proof of forward secrecy -- new key every connection)
  - the cipher line names the AEAD (e.g., TLS_AES_256_GCM_SHA384) --
    that is AES-GCM + SHA-384-based KDF, both covered in L24
EOF
