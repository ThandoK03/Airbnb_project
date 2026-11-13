# Data-Quality Assessment: Airbnb Listings and Reviews

AnalystLab Africa Experience Lab, Week 1, Track A (Data Analytics)
Intern: Thando Kheswa
Status: draft. Every figure below comes from the scripts listed in the README, and the full step-by-step record is in `PROJECT_LOG.md`. Items marked **to confirm** are listed in Section 12.

## 1. Scope

Four files were supplied: `Listings.csv`, `Reviews.csv` and two data dictionaries. The original files in `data_raw/` were never edited. All cleaning produced separate copies (`data_clean/`) and tables (`airbnb.duckdb`).

## 2. Record counts and keys

| Item | Result |
|------|--------|
| Listings rows | 279,712 (matches the brief; also equals the sum of the 10 city counts) |
| Listings columns | 33 |
| Reviews rows | 5,373,143 (matches the brief; confirmed by reconciliation, Section 10) |
| Candidate primary key, Listings | `listing_id`. Uniqueness: **to confirm** (Section 12) |
| Foreign key, Reviews | `listing_id` links to `listings.listing_id` |
| Reviews with no matching listing | **0** |
| Listings with no reviews | **86,156** (about 31% of listings) |
| Repeated `review_id` values | **160** (Section 5) |

## 3. File encoding

`Listings.csv` is not valid UTF-8 throughout, and the load failed at line 11,877. Latin-1 also failed, so the file mixes encodings. A UTF-8 copy was created with unreadable characters replaced by the replacement symbol (`clean_encoding.py`).

- Listings.csv: **981 lines** contained unreadable characters. Reviews.csv: **0 lines**.
- No rows were dropped. Only text fields are affected, so counts, prices and city analysis are not. Host and listing name text is excluded from the dashboard tables.

## 4. Missing values (Listings, 279,712 rows)

| Column | Missing | Share | Treatment |
|--------|---------|-------|-----------|
| district | 242,700 | 86.8% | Not used. `neighbourhood` (0% missing) is used for location. |
| host_response_time | 128,782 | 46.0% | Left blank. Shown as "(Blank)" meaning no data, with coverage reported. |
| host_response_rate | 128,782 | 46.0% | Not imputed. Averages use reporting listings only, shown with coverage. |
| host_acceptance_rate | 113,087 | 40.4% | Same as response rate. |
| review_scores_rating | 91,405 | 32.7% | Never shown as 0. Averages use rated listings only. |
| Other six review_scores_* fields | about 91,700 each | 32.8% | Same as the overall rating. |
| bedrooms | 29,435 | 10.5% | Left blank ("Unknown"). Excluded from bedroom-based price views. |
| host_since, host_is_superhost, host_total_listings_count, host_has_profile_pic, host_identity_verified | 165 each | 0.1% | Negligible. Left blank. |
| host_location | 832 | 0.3% | Negligible. Excluded from the dashboard tables. |
| name | 171 | 0.1% | Not needed. Excluded from the dashboard tables. |

No missing values: listing_id, host_id, neighbourhood, city, latitude, longitude, property_type, room_type, accommodates, amenities, price, minimum_nights, maximum_nights, instant_bookable.

Not yet proven (observations only): the 165 missing host fields share one count, which suggests the same listings. Response time and response rate share one count (128,782), which suggests the same listings.

## 5. Repeated review identifiers

- 160 `review_id` values appear more than once, each exactly twice (320 rows).
- All 160 are attached to **two different listings**. None involve different reviewers, and the examples show matching dates.
- The same listing pairs recur (for example listings 2997346 and 22219088). One possible explanation is a property listed twice. **This is a hypothesis and has not been verified.**

**Treatment:** no rows were deleted. Each row is a review record for its own listing, and removing one would take a review from a listing with no basis for choosing which. `review_id` alone is not used as a key; tables are linked by `listing_id`. Effect on totals: 160 of 5,373,143 rows (0.003%).

## 6. Prices and currency

- `price` is stored as a whole number (no symbols to strip). There is **no currency field**, so every price analysis is within one city. Currencies are **assumed from the city** (for example Paris EUR, Cape Town ZAR). This is an assumption, not a fact in the data.
- No missing prices and no negative prices. **113 listings have a price of 0.**

| City | Listings | Zero price | Min | Median | 99th pct | Max |
|------|----------|-----------|-----|--------|----------|-----|
| Paris | 64,690 | 62 | 0 | 80 | 600 | 12,000 |
| New York | 37,012 | 28 | 0 | 99 | 850 | 10,000 |
| Sydney | 33,630 | 0 | 5 | 120 | 1,721 | 28,613 |
| Rome | 27,647 | 6 | 0 | 65 | 600 | 10,571 |
| Rio de Janeiro | 26,615 | 7 | 0 | 280 | 5,693 | 625,216 |
| Istanbul | 24,519 | 2 | 0 | 252 | 3,806 | 179,532 |
| Mexico City | 20,065 | 7 | 0 | 661 | 7,294 | 499,000 |
| Bangkok | 19,361 | 1 | 0 | 1,100 | 15,553 | 300,177 |
| Cape Town | 19,086 | 0 | 122 | 1,069 | 22,019 | 180,000 |
| Hong Kong | 7,087 | 0 | 1 | 386 | 8,799 | 83,665 |

(Figures in each city's own currency. The medians in this table include the 113 zero prices.)

**Treatment:**
- Zero-price listings stay in listing counts and are excluded from price statistics (`price_valid` is blank when price is 0).
- Extreme prices are **flagged, not deleted** (`is_price_outlier`: above that city's 99th percentile of positive prices). Several maximums are far above the 99th percentile (for example Rio 625,216 against 5,693). They are probably entry errors or placeholders, but that is not proven.
- Medians are the main price measure because they resist extreme values.

## 7. Listings-to-reviews relationship (one to many)

| Has reviews | Has overall rating | Listings |
|-------------|--------------------|----------|
| Yes | Yes | 188,306 |
| Yes | No | 5,250 |
| No | Yes | 1 |
| No | No | 86,155 |
| **Total** | | **279,712** |

Review presence and rating line up almost exactly. The cause of the 5,250 listings with reviews but no rating is **not established** by the data. Review activity versus rating uses the 188,306 listings that have both.

## 8. Data types and scales

Types come from the loaded Listings table. IDs are whole numbers. `host_since` is a date. The three host flags and `instant_bookable` are true/false. `host_response_rate` and `host_acceptance_rate` are decimals from **0.0 to 1.0** (shown as percentages). `review_scores_rating` is a whole number from **20 to 100**. There is no bathrooms column. Review dates run from **2008-11-16 to 2021-03-01**, so 2021 is a partial year.

## 9. Privacy

Reviewer IDs, listing names, host names, host location text and amenity lists are not exported to the Power BI tables. `host_id` is kept only to count listings per host and is not displayed. Raw data files and the database are excluded from Git (`.gitignore`).

## 10. Transformation and reconciliation

`build_clean_tables.py` builds `listings_clean`, `review_summary_by_listing` and `review_activity_monthly`.

| Check | Expected | Actual |
|-------|----------|--------|
| listings_clean rows | 279,712 | 279,712 |
| Sum of review_count | 5,373,143 | 5,373,143 |
| Sum of monthly review_records | 5,373,143 | 5,373,143 |
| Zero-price listings | 113 | 113 |

No listings or review records were lost or double-counted.

## 11. Limitations

- Prices are advertised prices in assumed local currencies. They are not revenue, occupancy or profit.
- The Reviews file has dates and identifiers only. There is no review text and no individual ratings, so no sentiment analysis is possible. Review activity is not guest satisfaction.
- Host rates and review scores are missing for large shares of listings, so averages describe only the reporting listings.
- City sizes differ greatly (Paris 64,690 listings, Hong Kong 7,087), so counts must be compared as shares or per-city medians.
- District is 86.8% missing, so district-level concentration is not analysed.

## 12. Verification items still open

1. **Primary key:** confirm `listings` has 279,712 distinct `listing_id` values (the check printed during loading was not saved). Run `quality_checks_5.py`.
2. **Reviews key pair:** confirm `(listing_id, review_id)` is unique, as the brief states. Run `quality_checks_5.py`.
3. **Data dictionaries:** read `Listings_data_dictionary` and `Reviews_data_dictionary`, and add anything that conflicts with the above, such as the stated meaning of the host fields.
