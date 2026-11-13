import duckdb
con = duckdb.connect("airbnb.duckdb")

con.execute("""
COPY (
  WITH ranked AS (
    SELECT property_type, COUNT(*) AS listings,
           ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rnk
    FROM listings_clean GROUP BY property_type)
  SELECT property_type, listings,
         CASE WHEN rnk <= 10 THEN property_type ELSE 'Other' END AS property_type_group
  FROM ranked ORDER BY listings DESC)
TO 'data_clean/powerbi/dim_property_type.csv' (HEADER, DELIMITER ',')""")

for col in ["city", "room_type"]:
    con.execute(f"""COPY (SELECT DISTINCT {col} FROM listings_clean ORDER BY 1)
                    TO 'data_clean/powerbi/dim_{col}.csv' (HEADER, DELIMITER ',')""")

print(con.execute("""
  SELECT property_type, COUNT(*) AS listings,
         ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
  FROM listings_clean GROUP BY property_type
  ORDER BY listings DESC LIMIT 11""").fetchdf())