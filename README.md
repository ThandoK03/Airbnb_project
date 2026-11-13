[Uploading README_.md…]()
# Airbnb Market Intelligence: Track A (Data Analytics)

AnalystLab Africa Experience Lab, Week 1, Track A. Data preparation, validation, the four-page Power BI dashboard and the supporting documents are complete.

## Purpose

Prepare and validate the Airbnb Listings and Reviews data (10 cities, 279,712 listings, 5,373,143 review records) so a Power BI dashboard can report listing distribution, advertised pricing, host indicators and review activity. All findings reflect advertised prices and historical review records only. They do not show bookings, occupancy, revenue, profit or guest sentiment.

## Tools

Python 3, DuckDB, pandas, VS Code, Git, Power BI Desktop (dashboard stage). Microsoft Excel is not used, as the assignment requires.

## Setup

1. `pip install duckdb pandas`
2. Create a `data_raw/` folder and place the four supplied files in it (the data files are **not** in this repository, because Reviews.csv exceeds GitHub's file limit and contains reviewer IDs):
   - `Listings.csv`
   - `Reviews.csv`
   - the two data dictionary files
3. Run the scripts from the project folder, in the order below.

## Run order

| # | Script | What it does |
|---|--------|--------------|
| 1 | `clean_encoding.py` | Writes UTF-8 copies of the raw files to `data_clean/`. Originals are untouched. Replaces unreadable characters (981 lines in Listings.csv, 0 in Reviews.csv). |
| 2 | `load_data.py` | Loads the clean CSVs into `airbnb.duckdb` and prints row counts. |
| 3 | `quality_checks_2.py` | Missing values per column, listings per city, price checks per city, value ranges. |
| 4 | `quality_checks_3.py` | Review-to-listing link, listings with no reviews, review date range, repeated review IDs. |
| 5 | `quality_checks_4.py` | Compares listings with no reviews against listings with no rating. |
| 6 | `build_clean_tables.py` | Builds `listings_clean`, `review_summary_by_listing` and `review_activity_monthly`, exports them to `data_clean/powerbi/`, and prints reconciliation checks. |
| 7 | `build_dimensions.py` | Exports the city, room type and property type lookup lists (property types grouped into the top 10 plus "Other"). |

The full step-by-step record, with results and decisions, is in `docs/PROJECT_LOG.md`.

## Key data-quality results

- Listings: 279,712 rows, and `listing_id` is unique. Reviews: 5,373,143 rows. Every review matches a listing.
- 86,156 listings have no review records.
- 160 review IDs appear twice, each across two different listings. No rows were deleted, and `review_id` alone is not used as a key.
- 113 listings have a price of 0. They are kept in counts and excluded from price statistics.
- Missing values: district 86.8%, host response 46.0%, host acceptance 40.4%, review scores about 32.8%, bedrooms 10.5%.
- Reconciliation after transformation: 279,712 listings, 5,373,143 review records and 113 zero-price listings all match the source.

## Assumptions and limitations

- Prices are in local currency and the data has no currency field. The currency of each city is inferred from the city, and prices are analysed within each city only.
- The Reviews file has no review text or individual ratings, so no sentiment analysis is possible.
- There is no booking or occupancy data, so prices are advertised prices, not revenue.
- Review dates run from 2008-11-16 to 2021-03-01. 2021 is a partial year.

## Tools and AI assistance

Claude (Anthropic) was used for help with DuckDB setup, SQL and Python drafting, debugging and documentation. All outputs were run and checked by me.

## Business problem

Stakeholders in the accommodation market need to understand how Airbnb listings are distributed across 10 cities, how advertised prices vary within each local currency, how host indicators differ, and how historical review activity changes. Intended user: a market analyst or property-market stakeholder. Decisions supported: which markets and property types to study further, how reliable the available host and review indicators are, and what data to request next. Limitations: advertised prices only, no occupancy or revenue, no review text.

## Success criteria

1. Dashboard totals reconcile with independent SQL checks (279,712 listings, 5,373,143 review records).
2. Totals respond correctly to filters (for example Paris alone shows 64,690 listings).
3. Every price view is within a single city or a single table row, because currencies differ.
4. Every cleaning and transformation decision is documented (see `docs/DATA_QUALITY_ASSESSMENT.md` and `docs/PROJECT_LOG.md`).

## Deliverables

| Deliverable | File |
|-------------|------|
| Power BI file | `Airbnb_Dashboard.pbix` and `powerbi/airbnb_theme.json` |
| SQL and Python scripts | the `.py` files in this folder |
| Data-quality assessment | `docs/DATA_QUALITY_ASSESSMENT.md` |
| KPI definition sheet | `docs/KPI_DEFINITIONS.md` |
| Dashboard screenshots | `screenshots/` |
| Validation evidence | `docs/VALIDATION_EVIDENCE.md` |
| Executive summary | `docs/EXECUTIVE_SUMMARY.md` |
| Step-by-step record | `docs/PROJECT_LOG.md` |
