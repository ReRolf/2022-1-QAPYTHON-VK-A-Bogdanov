#! /bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
LOG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$LOG_DIR"/access.log
mkdir -p "$LOG_DIR"/parsed_log
RESULT="$LOG_DIR"/parsed_log/result_total.txt

echo -n "${bold}Total Requests:${normal}" >> "$RESULT"
awk 'END { print NR }' "$LOG_FILE" >> "$RESULT"
