import duckdb
con = duckdb.connect("airbnb.duckdb", read_only=True)
print(con.execute("""
SELECT
  (NOT EXISTS (SELECT 1 FROM reviews r WHERE r.listing_id = l.listing_id)) AS has_no_reviews,
  (l.review_scores_rating IS NULL) AS has_no_rating,
  COUNT(*) AS listings
FROM listings l
GROUP BY 1, 2
ORDER BY 1, 2
""").fetchdf())