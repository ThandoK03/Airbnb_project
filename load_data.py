import duckdb
con = duckdb.connect("airbnb.duckdb")

con.execute("""CREATE OR REPLACE TABLE listings AS
  SELECT * FROM read_csv('data_clean/Listings.csv', header=true, sample_size=-1)""")
con.execute("""CREATE OR REPLACE TABLE reviews AS
  SELECT * FROM read_csv('data_clean/Reviews.csv', header=true, sample_size=-1)""")

print(con.execute("SELECT COUNT(*) FROM listings").fetchone())
print(con.execute("SELECT COUNT(*) FROM reviews").fetchone())
print(con.execute("SELECT COUNT(*), COUNT(DISTINCT listing_id) FROM listings").fetchone())
print(con.execute("""SELECT COUNT(*) FROM (
  SELECT review_id FROM reviews GROUP BY review_id HAVING COUNT(*) > 1)""").fetchone())