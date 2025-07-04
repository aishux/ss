import json

# Assuming `result` is your dictionary
print("Final Result ------------------\n")

for rule, items in result.items():
    print(f"{rule}:")
    for idx, item in enumerate(items, 1):
        ques = item.get("ques", "")
        sql_query = item.get("sqlQuery", "")
        print(f"  [{idx}] Ques     : {ques}")
        print(f"      SQLQuery: {sql_query}\n")
