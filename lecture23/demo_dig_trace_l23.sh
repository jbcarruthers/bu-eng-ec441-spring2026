#!/usr/bin/env bash
# EC 441 L23 -- DNS resolution chain with dig
#
# Works on macOS and Linux. No VM required.
#
# Run individual commands or the whole thing:
#     bash demo_dig_trace_l23.sh
set -u

hr() { printf '\n==================================================\n%s\n==================================================\n' "$1"; }

hr "1. Basic A record lookup"
dig www.eng.bu.edu +short
dig www.eng.bu.edu      # full output -- ANSWER section, TTL, flags

hr "2. Specify the recursive resolver"
dig @1.1.1.1 www.eng.bu.edu +short    # Cloudflare
dig @8.8.8.8 www.eng.bu.edu +short    # Google

hr "3. Other record types"
dig bu.edu MX +short                  # mail exchange (with priority)
dig bu.edu NS +short                  # authoritative name servers
dig bu.edu SOA                        # zone metadata
dig google.com TXT +short | head -5   # SPF, DKIM, domain verification

hr "4. The resolution chain -- dig +trace"
# Walks root -> TLD -> authoritative. Ignores caching; queries each level.
dig +trace www.eng.bu.edu

hr "5. IPv6 and CNAME"
dig www.google.com AAAA +short        # IPv6 addresses
dig www.github.com +short             # usually shows a CNAME chain

hr "6. Reverse DNS"
dig -x 8.8.8.8 +short                 # IP -> name (PTR record)

hr "7. DNS over HTTPS (DoH)"
echo "DoH is HTTP, not DNS wire format. Example using curl:"
echo "  curl -s 'https://cloudflare-dns.com/dns-query?name=example.com&type=A' \\"
echo "       -H 'accept: application/dns-json' | jq"
