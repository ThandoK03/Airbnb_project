import duckdb
con = duckdb.connect("airbnb.duckdb", read_only=True)

rows, distinct_ids = con.execute(
    "SELECT COUNT(*), COUNT(DISTINCT listing_id) FROM listings").fetchone()
print("listings rows:", rows, "| distinct listing_id:", distinct_ids,
      "| primary key valid:", rows == distinct_ids)

n_reviews = con.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]
n_pairs = con.execute("""SELECT COUNT(*) FROM (
  SELECT DISTINCT listing_id, review_id FROM reviews)""").fetchone()[0]
n_ids = con.execute("SELECT COUNT(DISTINCT review_id) FROM reviews").fetchone()[0]
print("reviews rows:", n_reviews)
print("distinct (listing_id, review_id) pairs:", n_pairs,
      "| pair is unique:", n_reviews == n_pairs)
print("distinct review_id:", n_ids, "| rows minus distinct ids (expect 160):", n_reviews - n_ids)