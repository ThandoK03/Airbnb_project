# Executive Summary: Airbnb Market Performance and Listing Insights

AnalystLab Africa Experience Lab, Week 1, Track A (Data Analytics)
Intern: Thando Kheswa

Scope: 279,712 listings and 5,373,143 review records across 10 cities. Prices are advertised prices in each city's assumed local currency. They are not revenue, occupancy or profit, and the data holds no guest sentiment.

## Findings

1. **Paris is the largest market and Hong Kong the smallest.** Paris has 64,690 listings (23.1% of all listings) and Hong Kong 7,087 (2.5%). Paris, New York and Sydney together hold 135,332 listings (48.4%).
2. **Most listings are entire places.** Entire places are 182,005 listings (65.1%) and private rooms 86,988 (31.1%). Hotel and shared rooms together are about 3.8%.
3. **Apartments dominate supply.** "Entire apartment" alone is 49.7% of listings (138,989). With "Private room in apartment" (16.9%), apartments are about two thirds (66.6%). The top 10 property types cover 88.4% of listings, and the other 134 types together are 11.6%.
4. **About 31% of listings have no review record.** 86,156 listings (30.8%) have no reviews in the supplied extract. Review dates run from November 2008 to 1 March 2021, so 2021 is a partial year and the data predates anything after that.
5. **Host performance data is only partly available.** Host response rate is missing for 46.0% of listings and acceptance rate for 40.4%. Rate averages therefore describe only 54.0% and 59.6% of listings, and the dashboard shows that coverage next to each rate.
6. **Pricing data needs care.** There is no currency field, so prices can only be compared within one city. 113 listings have a price of 0, and several cities have maximum prices far above their 99th percentile (for example Rio de Janeiro 625,216 against 5,693). These were flagged, not deleted.
7. **Review volume is uneven, and Rome stands out.** Paris (about 1.21 million review records) and Rome (about 1.11 million) lead review volume. Rome has far fewer listings (27,647) than Paris (64,690), so it has roughly twice as many reviews per listing (about 40 against about 19). Figures are read from the dashboard's rounded labels.
8. **Review activity peaked in late 2019, then fell sharply in 2020.** Monthly review records rose steadily to roughly 170,000 a month, then dropped in 2020. The data cannot show why, so no cause is claimed.
9. **Listing-level ratings are high everywhere.** Average ratings by city range from 89.7 (Hong Kong, the lowest) to 94.8 (Mexico City) on a 20 to 100 scale. The differences are small, and ratings exist for only 67% of listings.

## Recommendations

**1. Compare prices only within each city, and add a currency field to the source data before any cross-city price work.**
- Evidence: the data has no currency field, and prices for the 10 cities are in different currencies (Finding 6).
- Proposed action: keep every price view within one city or one row, and ask the data owner for a currency column.
- How to evaluate: check that every price visual shows its currency, and that a currency field removes the assumption currently stated in the README.

**2. Treat host response and acceptance rates as partial indicators, and request the missing values.**
- Evidence: 46.0% and 40.4% of listings have no value (Finding 5).
- Proposed action: always show coverage next to each rate, and ask for the missing host data before ranking cities by host performance.
- How to evaluate: track coverage (currently 54.0% response, 59.6% acceptance) after any data refresh. A ranking is reliable only once coverage is high and similar across cities.

**3. Analyse listings with no reviews separately, and request a fuller and more recent Reviews extract.**
- Evidence: 86,156 listings have no review record, 5,250 further listings have reviews but no rating, and review records end in March 2021 (Finding 4).
- Proposed action: report review metrics only for listings that have reviews, label the others "no reviews", and request a newer extract.
- How to evaluate: compare the share of listings with no reviews, and the latest review date, before and after the refresh.

## Limitations

- Advertised prices only: no bookings, occupancy, revenue or profit.
- No review text and no individual review ratings, so no sentiment analysis is possible. Review activity is not guest satisfaction.
- Currencies are assumed from the city.
- Differences between cities partly reflect very different market sizes, and ratings are bunched near the top of the 20 to 100 scale.
