import os
os.makedirs("data_clean", exist_ok=True)

for name in ["Listings.csv", "Reviews.csv"]:
    bad = 0
    with open(f"data_raw/{name}", "r", encoding="utf-8", errors="replace", newline="") as src, \
         open(f"data_clean/{name}", "w", encoding="utf-8", newline="") as dst:
        for line in src:
            if "\ufffd" in line:
                bad += 1
            dst.write(line)
    print(f"{name}: {bad} lines contained unreadable characters (replaced)")