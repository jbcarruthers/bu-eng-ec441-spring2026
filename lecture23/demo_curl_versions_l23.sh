#!/usr/bin/env bash
# EC 441 L23 -- HTTP/1.1 vs HTTP/2 vs HTTP/3 with curl
#
# Requires a curl built with HTTP/2 and HTTP/3 support. Check:
#     curl --version
# The Features line should list "HTTP2" and "HTTP3".
# On macOS: `brew install curl` gives a modern build; the system curl is older.
#
# Run individual commands or the whole thing:
#     bash demo_curl_versions_l23.sh
set -u

HOST=https://www.cloudflare.com

hr() { printf '\n==================================================\n%s\n==================================================\n' "$1"; }

hr "Your curl's capabilities"
curl --version

hr "HTTP/1.1 -- forced"
curl -sv --http1.1 -o /dev/null "$HOST" 2>&1 | grep -E '^[<>*] ' | head -30

hr "HTTP/2 -- forced"
curl -sv --http2 -o /dev/null "$HOST" 2>&1 | grep -E '^[<>*] ' | head -30

hr "HTTP/3 -- forced (QUIC over UDP)"
# --http3-only fails fast if HTTP/3 is unavailable; --http3 falls back.
curl -sv --http3 -o /dev/null "$HOST" 2>&1 | grep -E '^[<>*] ' | head -30

hr "POST with a JSON body (HTTP/2)"
curl -sv --http2 -X POST https://httpbin.org/post \
    -H 'Content-Type: application/json' \
    -d '{"course":"EC441","lecture":23}' 2>&1 | grep -E '^[<>*] ' | head -40

hr "Headers only (HEAD request)"
curl -sI "$HOST" | head -20
