#!/bin/sh
hz=$(getconf CLK_TCK)
execution_limit=120
for f in /proc/*; do
  pid=$(basename "$f")
  case $pid in
  '' | '1' | *[!0-9]*)
    ;;
  *)
    echo "checking $pid"
    uptime=$(awk '{print $1}' </proc/uptime)
    starttime=$(awk '{print $22}' <"/proc/$pid/stat")
    seconds=$((${uptime%.*} - $starttime / $hz))
    if [ "$seconds" -gt "$execution_limit" ]; then
      echo "killing $pid"
      kill -9 "$pid"
    fi
    ;;
  esac
done
