import duckdb
con = duckdb.connect("airbnb.duckdb")

print("LISTINGS COLUMNS")
print(con.execute("DESCRIBE listings").fetchdf().iloc[:, :2].to_string())

print("\nREVIEWS WITH NO MATCHING LISTING (expect 0)")
print(con.execute("""SELECT COUNT(*) FROM reviews r
  LEFT JOIN listings l ON r.listing_id = l.listing_id
  WHERE l.listing_id IS NULL""").fetchone())

print("\nLISTINGS WITH NO REVIEWS")
print(con.execute("""SELECT COUNT(*) FROM listings l
  WHERE l.listing_id NOT IN (SELECT DISTINCT listing_id FROM reviews)""").fetchone())

print("\nREPEATED REVIEW_IDs: are the rows identical or different?")
print(con.execute("""SELECT review_id, COUNT(*) n, COUNT(DISTINCT listing_id) listings,
  COUNT(DISTINCT reviewer_id) reviewers
  FROM reviews GROUP BY review_id HAVING COUNT(*) > 1
  ORDER BY n DESC LIMIT 10""").fetchdf())