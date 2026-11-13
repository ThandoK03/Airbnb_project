import duckdb
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

con = duckdb.connect("airbnb.duckdb", read_only=True)

total = con.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
cols = [r[0] for r in con.execute("DESCRIBE listings").fetchall()]

print("MISSING VALUES PER COLUMN (listings)")
for c in cols:
    n = con.execute(f'SELECT COUNT(*) FROM listings WHERE "{c}" IS NULL').fetchone()[0]
    print(f"{c:30} {n:>8} {n/total:7.1%}")

print("\nLISTINGS PER CITY")
print(con.execute("""SELECT city, COUNT(*) AS listings
  FROM listings GROUP BY city ORDER BY listings DESC""").fetchdf())

print("\nPRICE CHECKS PER CITY (each city in its own local currency)")
print(con.execute("""SELECT city,
  COUNT(*) AS n,
  SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS missing,
  SUM(CASE WHEN price <= 0 THEN 1 ELSE 0 END) AS zero_or_negative,
  MIN(price) AS min_price,
  MEDIAN(price) AS median_price,
  quantile_cont(price, 0.99) AS p99_price,
  MAX(price) AS max_price
  FROM listings GROUP BY city ORDER BY n DESC""").fetchdf())

print("\nVALUE RANGES (to confirm scales)")
print(con.execute("""SELECT
  MIN(host_response_rate) AS resp_min, MAX(host_response_rate) AS resp_max,
  MIN(host_acceptance_rate) AS acc_min, MAX(host_acceptance_rate) AS acc_max,
  MIN(review_scores_rating) AS rating_min, MAX(review_scores_rating) AS rating_max
  FROM listings""").fetchdf())