import duckdb
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

con = duckdb.connect("airbnb.duckdb", read_only=True)

print("1. REVIEWS WITH NO MATCHING LISTING (expect 0)")
print(con.execute("""SELECT COUNT(*) FROM reviews r
  WHERE NOT EXISTS (SELECT 1 FROM listings l WHERE l.listing_id = r.listing_id)""").fetchone()[0])

print("\n2. LISTINGS WITH NO REVIEWS (expect above 0)")
print(con.execute("""SELECT COUNT(*) FROM listings l
  WHERE NOT EXISTS (SELECT 1 FROM reviews r WHERE r.listing_id = l.listing_id)""").fetchone()[0])

print("\n3. REVIEW DATE RANGE")
print(con.execute("""SELECT MIN("date") AS first_review, MAX("date") AS last_review
  FROM reviews""").fetchdf())

print("\n4. REPEATED REVIEW_IDs: SUMMARY")
print(con.execute("""SELECT COUNT(*) AS repeated_ids,
  SUM(n) AS rows_involved,
  SUM(CASE WHEN listings > 1 THEN 1 ELSE 0 END) AS ids_across_different_listings,
  SUM(CASE WHEN reviewers > 1 THEN 1 ELSE 0 END) AS ids_with_different_reviewers
  FROM (SELECT review_id, COUNT(*) AS n,
          COUNT(DISTINCT listing_id) AS listings,
          COUNT(DISTINCT reviewer_id) AS reviewers
        FROM reviews GROUP BY review_id HAVING COUNT(*) > 1)""").fetchdf())

print("\n5. REPEATED REVIEW_IDs: FIRST 10 EXAMPLES")
print(con.execute("""SELECT r.review_id, r.listing_id, r."date"
  FROM reviews r
  WHERE r.review_id IN (SELECT review_id FROM reviews
                        GROUP BY review_id HAVING COUNT(*) > 1)
  ORDER BY r.review_id LIMIT 10""").fetchdf())