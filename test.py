import json

# ANSI color codes
BOLD = '\033[1m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RESET = '\033[0m'
YELLOW = '\033[93m'

print(f"{BOLD}Final Result ------------------{RESET}\n")

for rule, items in result.items():
    print(f"{YELLOW}{rule}:{RESET}")
    for idx, item in enumerate(items, 1):
        ques = item.get("ques", "")
        sql_query = item.get("sqlQuery", "")
        print(f"  [{idx}] {BLUE}Ques     :{RESET} {ques}")
        print(f"       {GREEN}SQLQuery :{RESET} {sql_query}\n")
