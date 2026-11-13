import duckdb
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# Independent checks, calculated straight from the raw tables (not from the Power BI tables).
# Compare each result with the matching dashboard value and record both in docs/.
con = duckdb.connect("airbnb.duckdb", read_only=True)

print("1. LISTINGS PER CITY (Page 1 bar chart)")
print(con.execute("""SELECT city, COUNT(*) AS listings
  FROM listings GROUP BY city ORDER BY listings DESC""").fetchdf())

print("\n2. MEDIAN VALID PRICE PER CITY, price > 0, local currency (Page 2 table)")
print(con.execute("""SELECT city, MEDIAN(price) AS median_price_valid,
  AVG(price) AS average_price_valid, COUNT(*) AS valid_price_listings
  FROM listings WHERE price > 0 GROUP BY city ORDER BY city""").fetchdf())

print("\n3. TOTAL REVIEW RECORDS (Page 4 card, expect 5373143)")
print(con.execute("SELECT COUNT(*) FROM reviews").fetchone()[0])

print("\n4. LISTINGS WITH REVIEWS (Page 4 card, expect 193556)")
print(con.execute("SELECT COUNT(DISTINCT listing_id) FROM reviews").fetchone()[0])

print("\n5. RATED LISTINGS and AVERAGE RATING (Page 4 cards, expect 188307 rated)")
print(con.execute("""SELECT COUNT(review_scores_rating) AS rated_listings,
  AVG(review_scores_rating) AS avg_rating FROM listings""").fetchdf())

print("\n6. HOST COVERAGE (Page 3, expect about 0.540 and 0.596)")
print(con.execute("""SELECT COUNT(host_response_rate) * 1.0 / COUNT(*) AS response_coverage,
  COUNT(host_acceptance_rate) * 1.0 / COUNT(*) AS acceptance_coverage,
  AVG(host_response_rate) AS avg_response_rate,
  AVG(host_acceptance_rate) AS avg_acceptance_rate FROM listings""").fetchdf())

print("\n7. SUPERHOST % among listings with a value (Page 3 card)")
print(con.execute("""SELECT AVG(CASE WHEN host_is_superhost THEN 1.0 ELSE 0.0 END)
  FROM listings WHERE host_is_superhost IS NOT NULL""").fetchone()[0])

print("\n8. HOSTS and LISTINGS PER HOST (Page 3 cards)")
print(con.execute("""SELECT COUNT(DISTINCT host_id) AS hosts,
  COUNT(*) * 1.0 / COUNT(DISTINCT host_id) AS listings_per_host FROM listings""").fetchdf())