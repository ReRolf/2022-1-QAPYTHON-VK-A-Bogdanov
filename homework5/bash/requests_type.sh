#! /bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
LOG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$LOG_DIR"/access.log
mkdir -p "$LOG_DIR"/parsed_log
RESULT="$LOG_DIR"/parsed_log/result_request_type.txt

echo -e "${bold}Request amount by type:${normal}" > "$RESULT"
awk '{print $6}' "$LOG_FILE" | tr -dc '[:alnum:]\n\r' | sort | uniq -c | sort -nr | awk \
'length($2)<=10{print NR,$2, "\t\t: ", $1} length($2)>10{print "\nUNDEFINED REQUEST TYPE:\n",NR, $2, "\b: ", $1}'>> "$RESULT"
