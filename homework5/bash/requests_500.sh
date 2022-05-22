#! /bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
LOG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$LOG_DIR"/access.log
mkdir -p "$LOG_DIR"/parsed_log
RESULT="$LOG_DIR"/parsed_log/result_requests_500.txt

echo -e "${bold}Top 5 ip by number of requests with (5XX) error${normal}" > "$RESULT"
awk '{if ($9 ~ /5../) print $1}' "$LOG_FILE" | sort -t "." -rn | uniq -c | sort -rn \
| awk '{printf "\n~ Ip: %s\n~ Requests: %d\n", $2, $1} NR==5{exit}' >> "$RESULT"
