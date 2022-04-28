#! /bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
LOG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$LOG_DIR"/access.log
mkdir -p "$LOG_DIR"/parsed_log
RESULT="$LOG_DIR"/parsed_log/FULL_RESULT.txt

printf '%.s─' $(seq 1 $(tput cols)) > "$RESULT"
echo -n "${bold}Total Requests:${normal}" >> "$RESULT"
awk 'END { print NR }' "$LOG_FILE" >> "$RESULT"
printf '%.s─' $(seq 1 $(tput cols)) >> "$RESULT"

echo -e "\n${bold}Request amount by type:${normal}" >> "$RESULT"
awk '{print $6}' "$LOG_FILE" | tr -dc '[:alnum:]\n\r' | sort | uniq -c | sort -nr | awk \
'length($2)<=10{print NR,$2, "\t\t: ", $1} length($2)>10{print "\nUNDEFINED REQUEST TYPE:\n",NR, $2, "\b: ", $1}'>> "$RESULT"
printf '%.s─' $(seq 1 $(tput cols)) >> "$RESULT"

echo -e "\n${bold}Top 10 requests:${normal}" >> "$RESULT"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | \
head | awk '{print NR,"\b. URL:", $2,"\n   Requests:", $1}'>> "$RESULT"
printf '%.s─' $(seq 1 $(tput cols)) >> "$RESULT"

echo -e "\n${bold}10 largest requests with (4XX) Error:${normal}" >> "$RESULT"
awk '{if ($9 ~ /4../) print $7, $9, $10, $1, "\n"}' "$LOG_FILE" | sort -rnk3 | head -n 5| awk \
'{printf "\n\n~ URL: %s\n~ Response: %d\n~ Size: %d\n~ Ip: %s\n", $1, $2, $3, $4}'>> "$RESULT"
printf '%.s─' $(seq 1 $(tput cols)) >> "$RESULT"

echo -e "\n${bold}Top 5 ip by number of requests with (5XX) error${normal}" >> "$RESULT"
awk '{if ($9 ~ /5../) print $1}' "$LOG_FILE" | sort -t "." -rn | uniq -c | sort -rn \
| awk '{printf "\n~ Ip: %s\n~ Requests: %d\n", $2, $1} NR==5{exit}' >> "$RESULT"
printf '%.s─' $(seq 1 $(tput cols)) >> "$RESULT"
