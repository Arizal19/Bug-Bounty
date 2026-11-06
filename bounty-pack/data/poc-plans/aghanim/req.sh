#!/bin/bash
# usage: req.sh METHOD URL [data] [extra curl args...]
M=$1; U=$2; D=$3; shift 3 2>/dev/null
H=(-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" -H "X-Bug-Bounty: RESEARCHER_EMAIL" -H "Origin: https://pay.aghanim.com" -H "Referer: https://pay.aghanim.com/")
if [ -n "$D" ]; then H+=(-H "Content-Type: application/json" --data "$D"); fi
printf "%-8s %s\n" "$M" "$U"
curl -sS -X "$M" "${H[@]}" "$@" -w "\n[http %{http_code} ct=%{content_type} sz=%{size_download}]\n" "$U" --max-time 20 | head -c 1200
echo
