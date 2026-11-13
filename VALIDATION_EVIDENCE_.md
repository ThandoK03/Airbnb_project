# Validation Evidence

AnalystLab Africa Experience Lab, Week 1, Track A (Data Analytics)
Intern: Thando Kheswa
Method: dashboard values (Power BI) compared with independent calculations in DuckDB/SQL on the raw tables (`load_data.py`, `quality_checks_3.py`, `quality_checks_4.py`, `quality_checks_5.py`, `build_clean_tables.py`, `validation_checks.py`).

## A. Data pipeline reconciliation (passed, output saved in `docs/`)

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| Listings rows loaded | 279,712 | 279,712 | Pass |
| Sum of the 10 city counts | 279,712 | 279,712 | Pass |
| listings_clean rows | 279,712 | 279,712 | Pass |
| Sum of review_count (listings_clean) | 5,373,143 | 5,373,143 | Pass |
| Sum of monthly review_records | 5,373,143 | 5,373,143 | Pass |
| Zero-price listings | 113 | 113 | Pass |
| Reviews with no matching listing | 0 | 0 | Pass |
| Has reviews / has rating groups add up | 279,712 | 188,306 + 5,250 + 1 + 86,155 = 279,712 | Pass |

## B. Dashboard versus independent SQL

### Page 1: Market Overview

| Dashboard value | Dashboard | SQL | Result |
|-----------------|-----------|-----|--------|
| Total Listings card | 279,712 | 279,712 | Pass |
| Cities Represented card | 10 | 10 | Pass |
| Listings by city (Paris to Hong Kong) | 64,690 / 37,012 / 33,630 / 27,647 / 26,615 / 24,519 / 20,065 / 19,361 / 19,086 / 7,087 | Same values | Pass |
| Property type counts (top 10 and Other) | 138,989 / 47,322 / 32,555 / 13,292 / 13,273 / 11,250 / 5,771 / 4,587 / 4,462 / 4,238 / 3,973 | Same values | Pass |
| Room type: Entire place, Private room | 182,005 / 86,988 | 65.07% and 31.1% of 279,712 | Pass |

### Page 2: Pricing (median valid advertised price, local currency, price > 0)

| City | Dashboard median | SQL median (earlier city table, includes zero prices) | Result |
|------|------------------|-------------------------------------------------------|--------|
| Paris (EUR) | 80 | 80 | Pass |
| New York (USD) | 99 | 99 | Pass |
| Cape Town (ZAR) | 1,069 | 1,069 | Pass |
| Hong Kong (HKD) | 386 | 386 | Pass |
| Istanbul (TRY) | 252 | 252 | Pass |
| Bangkok (THB) | 1,100 | 1,100 | Pass |
| Mexico City (MXN) | 664 | 661 | Explained: the SQL figure includes 7 zero-price listings, which the dashboard excludes |

Also checked on Page 2: per-city Total Listings in the table match the city counts above, the zero-price column totals 113, and with Bangkok selected the zero-price card reads 1 (matches the Bangkok table row).

### Page 3: Host performance

| Dashboard value | Dashboard | SQL / check | Result |
|-----------------|-----------|-------------|--------|
| Response Coverage (total) | 54% | 1 - 128,782 / 279,712 = 53.96% | Pass |
| Acceptance Coverage (total) | 60% | 1 - 113,087 / 279,712 = 59.57% | Pass |
| Listings per Host | 1.54 | 279,712 / 182,024 = 1.537 | Pass (arithmetic). Hosts = 182,024 to be confirmed against `validation_checks.py` output 8 |
| Total Listings in host table | 279,712 | 279,712 | Pass |

### Page 4: Review activity

| Dashboard value | Dashboard | SQL | Result |
|-----------------|-----------|-----|--------|
| Total Review Records | 5,373,143 | 5,373,143 (rows in Reviews) | Pass |
| Listings With Reviews | 193,556 | 193,556 (188,306 + 5,250 from `quality_checks_4.py`) | Pass |
| Rated Listings | 188,307 | 188,307 (188,306 + 1 from `quality_checks_4.py`) | Pass |
| Review records by city (labels, rounded) | Sum about 5.35M | 5,373,143 | Consistent with rounding |
| Top 10 listings by review count | Highest 891 | to confirm with a `GROUP BY listing_id ORDER BY COUNT(*) DESC LIMIT 10` query | To confirm |

## C. Filter tests (checked on screen)

| Test | Expected | Observed | Result |
|------|----------|----------|--------|
| City slicer = Paris, Total Listings (Page 1) | 64,690 | 64,690 | Pass |
| City slicer = Paris, Cities Represented | 1 | 1 | Pass |
| City slicer = Paris, charts | Only Paris data | Only Paris data | Pass |
| Clear the slicer | 279,712 | 279,712 | Pass |
| City slicer = Bangkok, Price Context (Page 2) | Prices in THB | Prices in THB | Pass |
| City slicer = Bangkok, Zero-price Listings (Page 2) | 1 | 1 | Pass |

## D. Discrepancies found between source records and dashboard, and how they were resolved

| # | Where | What differed | Cause | Fix and result |
|---|-------|---------------|-------|----------------|
| 1 | Page 2 table and zero-price card | The table total was about 3,300 listings below 279,712 (Bangkok median showed 1,088, not 1,100), and the zero-price card read 113 with Bangkok selected | A filter on `accommodates` (meant for one chart) was applied to the whole page, and the city slicer's interaction with the card was switched off | Moved the filter to the capacity chart and restored the slicer interaction. Table total now 279,712, Bangkok median 1,100, card 1 |
| 2 | Page 4, Total Review Records | 5,373,142 against 5,373,143 (1 record short) | A date filter (before 1 March 2021) meant for the line chart was applied to the whole page, removing the one review dated 1 March 2021 | Moved the filter to the line chart. Card now 5,373,143 |
| 3 | Page 4, Rated Listings | 188,306 against 188,307 (1 short) | Hiding the "No reviews" band on one chart was applied to the whole page, removing the single listing that has a rating but no reviews | Moved the filter to that chart. Card now 188,307 |

Lesson recorded: a filter set in "Filters on this page" affects every visual on the page. Visual-specific filters belong under "Filters on this visual".

## E. Limitations that affect interpretation

- Prices are advertised prices in assumed local currencies, not revenue.
- Host rates and review scores are missing for 33% to 46% of listings, so averages describe reporting listings only.
- 160 review IDs appear on two listings each. They were kept, and the effect on totals is 0.003%.
- Review data ends on 1 March 2021.
- Dashboard labels on the review-by-city chart are rounded to 0.01M.
