# CS506Project-Boston-Airbnb-Pricing-Prediction

## Setup and run
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Activate it:
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If you see an XGBoost OpenMP error on macOS, install libomp:
   ```bash
   brew install libomp
   ```

## Proposal
[View the project proposal](Proposal.md)


# Project Report


## 3. Data Processing

### 3.1 Initial Data Inspection
We began by examining the dataset structure, data types, and missing values.
- Dataset size: 4,419 rows × 79 columns
- Mixed data types: numerical, categorical, and text
- Significant missing values observed in multiple columns

| Feature | Missing Value |
|---|---|
| `calendar_updated` | 4419 |
| `neighbourhood_group_cleansed` | 4419 |
| `price` | 913 |
| `beds` | 869 |
| `bathrooms` | 864 |
| `bedrooms` | 305 |
| `host_is_superhost` | 229 |

**Dropping Irrelevant and Redundant Columns**
- Scraping / metadata fields: `scrape_id, last_scraped, calendar_last_scraped, source`
- Identifiers and URLs: `id, listing_url, picture_url`
- Low-value textual features: `name, description, license`
- Fully empty columns:`calendar_updated,neighbourhood_group_cleansed`
- Derived or redundant metrics: `estimated_revenue_l365d, estimated_occupancy_l365d`

### 3.2 Price Cleaning and Transformation
**a. Data Type Conversion**
    Converted to numeric

**b. Check Price Distribution**

![Plot title](./plots/price_distribution_orginal.png)
- Price skewness:     9.30
- log_price skewness: 2.17 

    Log Tranformation `log_price = log(1 + price)`: reduce skewness 

**c. Use IQR method to remove outlier** (data remain 3416 rows)

![Plot title](./plots/price_distribution_after_outlier_removal.png)


Skewness improved significantly:
- Price: 1.31 → still skewed
- Log price: ≈ -0.26 (nearly symmetric)

### 3.3 Host Feature Processing
**a. Data Type Conversion**
  -  numeric type: % -> float
  - t/f -> binary(0/1)

**b. Check with log_price**

![Plot title](./plots/host_related.png)

  Most host-related features showed weak correlation with price
  - Removed all other host-related columns such as:`Profile info, verification, listings count, response metrics`
  - Only maintain: `host_is_superhost`

### 3.4 Minimum/Maximum Nights
**a. Data Exploration**

![Plot title](./plots/min_max_nights.png)

- Weak relationship with price
- High redundancy across features

**b. Feature Engineering: `is_short_stay `**

is_short_stay = (minimum_nights ≤ 2)

![Plot title](./plots/is_short_stay.png)

The minimum and maximum night features showed no clear relationship with price in scatter plots and had near zero correlation, indicating they provide little predictive value. Additionally, the calendar derived night variables were highly redundant and introduced noise without adding new information. Instead, a binary feature is_short_stay (≤2 nights) was retained, as it captures a meaningful behavioral pattern and shows a slightly higher likelihood of high priced listings.


### 3.5 Availability Features
**a. Data Exploration**

![Plot title](./plots/availability.png)

- Highly correlated with each other
- Weak relationship with price

**b. Data Cleaning**
- Dropped all short-term availability variables
- Retained `availability_365`

### 3.6  Review Features
**a. Data Exploration**

![Plot title](./plots/reviews.png)

- Review scores highly concentrated between 4–5
- Limited variance → low predictive power
- Strong redundancy across multiple review metrics

**b. Data Cleaning**

- Dropped:all detailed review score features and time-based review metrics
- Retained: `number_of_reviews` (captures listing popularity)

### 3.7 Property and Room Type 

**Room Type**
| room_type | count |
|---|---|
|Entire home/apt |2443|
|Private room|965|
|Hotel room|5|
|Shared room |3|

![Plot title](./plots/room_type_vs_price.png)

**Property Type**

The property types are highly mixed, with a few dominant categories and many rare ones with very low counts.

| Property Type                         | Count |
|-------------------------------------|------:|
| Entire rental unit                  | 1862  |
| Private room in rental unit         | 463   |
| Private room in home                | 292   |
| Entire condo                        | 227   |
| Entire home                         | 170   |
| Entire serviced apartment           | 64    |
| Entire guest suite                  | 62    |
| Private room in condo               | 53    |
| Room in hotel                       | 44    |
| Private room in townhouse           | 38    |
| Entire townhouse                    | 22    |
| Private room in bed and breakfast   | 22    |
| Room in boutique hotel              | 21    |
| Entire loft                         | 18    |
| Private room in serviced apartment  | 12    |
| Private room in guest suite         | 11    |
| Boat                                | 7     |
| Private room                        | 7     |
| Houseboat                           | 4     |
| Entire guesthouse                   | 4     |
| Private room in villa               | 4     |
| Shared room in rental unit          | 2     |
| Private room in loft                | 1     |
| Entire place                        | 1     |
| Private room in casa particular     | 1     |
| Entire vacation home                | 1     |
| Private room in hostel              | 1     |
| Shared room in condo                | 1     |
| Tiny home                           | 1     |


**Cleaned Property Type Distribution** Mapped property into simplified categories: `apartment, house, condo, townhouse, hotel, loft, guest_space, other`

After grouping similar categories, the property types become less sparse and easier to analyze.

| Property Type (Cleaned) | Count |
|------------------------|------:|
| apartment              | 2403  |
| house                  | 532   |
| condo                  | 281   |
| guest_space            | 73    |
| hotel                  | 65    |
| other                  | 43    |
| loft                   | 19    |

![Plot title](./plots/property_type_vs_price.png)

