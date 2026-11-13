# KPI Definition Sheet: Airbnb Market Performance Dashboard

AnalystLab Africa Experience Lab, Week 1, Track A (Data Analytics)
Intern: Thando Kheswa
Status: draft. Measures are defined in Power BI (DAX) on the tables built by `build_clean_tables.py`. Independent SQL checks for these KPIs are in `validation_checks.py`.

## 1. Shared definitions

| Term | Definition used in this project |
|------|---------------------------------|
| Listing count | Number of rows in Listings (one row per `listing_id`). |
| Advertised price | The `price` field for a listing, in the local currency of its city (currency assumed from the city; the data has no currency field). It is not revenue, occupancy or profit. |
| Valid advertised price | `price` greater than 0. Zero prices (113 listings) are kept in counts and excluded from price statistics (`price_valid`). |
| Room type | The `room_type` field (4 values). |
| Property type | The `property_type` field (144 values). Charts and slicers use `property_type_group`: the 10 most common types plus "Other" (the top 10 cover 88.4% of listings). |
| Host performance indicators | `host_response_rate`, `host_acceptance_rate`, `host_response_time` and `host_is_superhost`, as supplied. They are reported in the data and not independently verified. |
| Review count | Number of rows in Reviews for a listing (`review_count`). Each (listing, review) row counts once. Total review records is 5,373,143, of which 160 rows share a review ID with another listing (kept). |
| Review activity | Number of review records by calendar month of the review date (`review_month`). Not a measure of guest satisfaction or of bookings. |
| Listing-level review rating | `review_scores_rating` in Listings, scale 20 to 100. Missing for 32.7% of listings; missing means "no rating", never 0. |

## 2. Business questions covered (7 of the 10 listed for Track A)

Q1 listings by city, Q2 room types, Q3 property types, Q4 advertised prices within each local currency, Q7 reviews per listing, Q8 review activity over time, Q9 host response and acceptance indicators.

## 3. KPI definitions

| ID | KPI | Question | Definition | Calculation (DAX) | Business interpretation | Caveats |
|----|-----|----------|------------|-------------------|-------------------------|---------|
| K1 | Total Listings | Q1 | Number of listings in the current filter | `COUNTROWS(listings_clean)` | Market size and supply by city. Shows which markets are largest and smallest. | Counts listings, not available nights or bookings. Markets differ greatly in size, so compare shares, not raw counts, across cities. |
| K2 | Cities Represented | Q1 | Distinct cities in the filter | `DISTINCTCOUNT(listings_clean[city])` | Confirms coverage (10 cities). | None. |
| K3 | Room type share | Q2 | Share of listings by room type | `Total Listings` by `room_type`, shown as a percentage of the total | Shows the balance between entire places and private or shared rooms. | Based on the host's room-type label. |
| K4 | Property type share | Q3 | Share of listings by property type group | `Total Listings` by `property_type_group`, shown as a percentage of the total | Shows which accommodation types dominate supply (apartments are about two thirds of listings). | "Other" combines 134 smaller types. |
| K5 | Median Price (valid) | Q4 | Median advertised price among listings with price > 0 | `MEDIAN(listings_clean[price_valid])` | Typical advertised price within one city and currency. The median resists extreme prices. | **Compare only within one city.** Different currencies. Advertised price, not revenue. The dashboard shows it for a single city (`Median Price (single city)`) or one city per table row. |
| K6 | Average Price (valid) | Q4 | Mean advertised price, price > 0 | `AVERAGE(listings_clean[price_valid])` | Shown alongside the median to reveal the pull of extreme prices. | Strongly affected by extreme prices (for example Rio maximum 625,216). |
| K7 | Price band share | Q4 | Share of listings by price relative to the city's own median | `Price Band` column (under 0.5x, 0.5x to 1x, 1x to 1.5x, 1.5x to 2x, 2x to 3x, over 3x the city median) with `Total Listings` | Shows how spread out prices are within each city without comparing currencies. | The city median is calculated on valid prices. |
| K8 | Price Outliers and Zero-price Listings | Q4 | Listings above the city's 99th percentile of positive prices; listings with price 0 | `CALCULATE(COUNTROWS(listings_clean), listings_clean[is_price_outlier] = TRUE())`; same pattern for `is_zero_price` | Data-quality indicators for pricing. | Outliers are flagged, not removed, and not proven to be errors. |
| K9 | Review count per listing | Q7 | Number of review records for each listing | `review_count` column (sum per listing); top 10 listings by Top N filter | Shows which listings receive the most review activity. | 31% of listings have no reviews (86,156). Review count is not occupancy. |
| K10 | Listings With Reviews | Q7 | Listings with at least one review record | `CALCULATE(COUNTROWS(listings_clean), listings_clean[review_count] > 0)` | Share of the market with any review history. | Depends on the supplied Reviews extract. |
| K11 | Avg Reviews per Reviewed Listing | Q7 | Review records divided by listings with reviews | `DIVIDE(SUM(listings_clean[review_count]), [Listings With Reviews])` | Typical review depth among listings that have reviews. | Skewed by a few listings with very many reviews; older listings accumulate more. |
| K12 | Total Review Records | Q8 | Number of review records in the filter | `SUM(review_activity_monthly[review_records])` | Overall review volume. | Responds to city, room type and property type filters only. |
| K13 | Review activity by month | Q8 | Review records per calendar month | `Total Review Records` by `review_month`, March 2021 excluded as incomplete (data ends 1 March 2021) | Shows how review activity changes over time. | Describes recorded reviews, not bookings. Dips (such as 2020) cannot be attributed to a cause from this data. |
| K14 | Avg Response Rate and Avg Acceptance Rate | Q9 | Mean host response rate and acceptance rate among listings that report them | `AVERAGE(listings_clean[host_response_rate])`; same for acceptance | Compares host responsiveness across cities (unit-free, so cross-city comparison is valid). | Missing for 46.0% and 40.4% of listings; averages describe reporting listings only. |
| K15 | Response Coverage and Acceptance Coverage | Q9 | Share of listings that report the rate | `DIVIDE(COUNT(listings_clean[host_response_rate]), [Total Listings])` | Shows how much of the market each rate average represents. | Always read with K14. |
| K16 | Hosts and Listings per Host | Q9 | Distinct hosts; listings divided by hosts, inside this dataset | `DISTINCTCOUNT(listings_clean[host_id])`; `DIVIDE([Total Listings], [Hosts])` | Shows host concentration and professional multi-listing hosts. | Uses host_id within the dataset, not the platform's `host_total_listings_count`. |
| K17 | Multi-listing Host Share | Q9 | Share of listings whose host has more than one listing in the data | `DIVIDE(CALCULATE(COUNTROWS(listings_clean), listings_clean[host_listings_in_data] > 1), [Total Listings])` | Indicates how much of supply comes from multi-listing hosts. | Within this dataset only. |
| K18 | Superhost % | Q9 | Share of listings with a superhost host, among listings with a value | `DIVIDE(CALCULATE(COUNTROWS(listings_clean), listings_clean[host_is_superhost] = TRUE()), COUNTA(listings_clean[host_is_superhost]))` | Indicator of the platform's superhost status across markets. | 165 listings (0.1%) have no value and are excluded from the denominator. |
| K19 | Rated Listings and Avg Rating (rated listings) | Q7 | Listings with a rating; their mean `review_scores_rating` | `COUNT(listings_clean[review_scores_rating])`; `AVERAGE(listings_clean[review_scores_rating])` | Compares listing-level ratings across cities and property types. | Rating is on a 0 to 100 scale and bunched near the top; small differences matter little. Not guest sentiment. Association with review count is not causal. |

## 4. Independent checks (run `validation_checks.py`)

| KPI | Dashboard value | Independent SQL (DuckDB) | Result |
|-----|-----------------|--------------------------|--------|
| K1 listings per city | Page 1 | `SELECT city, COUNT(*) FROM listings GROUP BY city` | to record |
| K5 median valid price per city | Page 2 table | `SELECT city, MEDIAN(price) FROM listings WHERE price > 0 GROUP BY city` | to record |
| K12 total review records | Page 4 card | `SELECT COUNT(*) FROM reviews` (expect 5,373,143) | to record |
| K10 listings with reviews | Page 4 card | `SELECT COUNT(DISTINCT listing_id) FROM reviews` (expect 193,556) | to record |
| K19 rated listings | Page 4 card | `SELECT COUNT(review_scores_rating) FROM listings` (expect 188,307) | to record |
| K15 coverage | Page 3 | `SELECT COUNT(host_response_rate)*1.0/COUNT(*) FROM listings` (about 0.540) | to record |

Also check that totals respond correctly to slicers (for example Paris alone shows 64,690 listings), and record each dashboard-versus-SQL comparison in `validation_evidence`.
