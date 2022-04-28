#! /bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
LOG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$LOG_DIR"/access.log
mkdir -p "$LOG_DIR"/parsed_log
RESULT="$LOG_DIR"/parsed_log/result_requests_400.txt

echo -e "${bold}10 largest requests with (4XX) Error:${normal}" > "$RESULT"
awk '{if ($9 ~ /4../) print $7, $9, $10, $1, "\n"}' "$LOG_FILE" | sort -rnk3 | head -n 5| awk \
'{printf "\n\n~ URL: %s\n~ Response: %d\n~ Size: %d\n~ Ip: %s\n", $1, $2, $3, $4}'>> "$RESULT"
