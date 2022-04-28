#! /bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
LOG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$LOG_DIR"/access.log
mkdir -p "$LOG_DIR"/parsed_log
RESULT="$LOG_DIR"/parsed_log/result_requests_top.txt

echo -e "${bold}Top 10 requests:${normal}" > "$RESULT"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | \
head | awk '{print NR,"\b. URL:", $2,"\n   Requests:", $1}'>> "$RESULT"
