import duckdb, os
os.makedirs("data_clean/powerbi", exist_ok=True)
con = duckdb.connect("airbnb.duckdb")

# 1. Review summary per listing
con.execute("""
CREATE OR REPLACE TABLE review_summary_by_listing AS
SELECT listing_id,
       COUNT(*) AS review_count,
       MIN("date") AS first_review_date,
       MAX("date") AS last_review_date
FROM reviews
GROUP BY listing_id
""")

# 2. Clean listings (no names or host location text)
con.execute("""
CREATE OR REPLACE TABLE listings_clean AS
WITH p AS (
  SELECT city,
         quantile_cont(CASE WHEN price > 0 THEN price END, 0.99) AS p99
  FROM listings GROUP BY city
)
SELECT l.listing_id, l.host_id, l.city, l.neighbourhood, l.district,
       l.property_type, l.room_type, l.accommodates, l.bedrooms,
       l.price,
       CASE WHEN l.price > 0 THEN l.price END AS price_valid,
       (l.price <= 0) AS is_zero_price,
       (l.price > p.p99) AS is_price_outlier,
       l.minimum_nights, l.maximum_nights, l.instant_bookable,
       l.host_since, l.host_response_time, l.host_response_rate,
       l.host_acceptance_rate, l.host_is_superhost,
       l.host_total_listings_count, l.host_identity_verified,
       l.latitude, l.longitude,
       l.review_scores_rating, l.review_scores_accuracy,
       l.review_scores_cleanliness, l.review_scores_checkin,
       l.review_scores_communication, l.review_scores_location,
       l.review_scores_value,
       COALESCE(rs.review_count, 0) AS review_count,
       rs.first_review_date, rs.last_review_date,
       COUNT(*) OVER (PARTITION BY l.host_id) AS host_listings_in_data
FROM listings l
JOIN p ON l.city = p.city
LEFT JOIN review_summary_by_listing rs ON l.listing_id = rs.listing_id
""")

# 3. Monthly review activity by city, room type and property type
con.execute("""
CREATE OR REPLACE TABLE review_activity_monthly AS
SELECT l.city, l.room_type, l.property_type,
       CAST(date_trunc('month', r."date") AS DATE) AS review_month,
       COUNT(*) AS review_records
FROM reviews r
JOIN listings l ON r.listing_id = l.listing_id
GROUP BY 1, 2, 3, 4
""")

# 4. Export for Power BI
for t in ["listings_clean", "review_summary_by_listing", "review_activity_monthly"]:
    con.execute(f"COPY {t} TO 'data_clean/powerbi/{t}.csv' (HEADER, DELIMITER ',')")

# 5. Reconciliation checks
print("listings_clean rows (expect 279712):",
      con.execute("SELECT COUNT(*) FROM listings_clean").fetchone()[0])
print("sum of review_count (expect 5373143):",
      con.execute("SELECT SUM(review_count) FROM listings_clean").fetchone()[0])
print("sum of monthly review_records (expect 5373143):",
      con.execute("SELECT SUM(review_records) FROM review_activity_monthly").fetchone()[0])
print("zero-price listings (expect 113):",
      con.execute("SELECT COUNT(*) FROM listings_clean WHERE is_zero_price").fetchone()[0])
print("monthly table rows:",
      con.execute("SELECT COUNT(*) FROM review_activity_monthly").fetchone()[0])