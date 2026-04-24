import pandas as pd
import numpy as np
import pytest


# Fixtures

@pytest.fixture
def raw_price_series():
    return pd.Series(["$150.00", "0", None, "$500.00", "$1,200.00"])

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "price": ["$150.00", "$80.00", "$500.00", "$20.00"],
        "accommodates": [2, 1, 4, 1],
        "bathrooms_text": ["1 bath", "1 shared bath", "2 baths", "1 shared bath"],
        "minimum_nights": [1, 3, 5, 2],
        "amenities": ['["Wifi", "Kitchen", "Air conditioning"]', '["Parking", "Pets allowed"]', '["Wifi", "Self check-in"]', '["Kitchen"]',],
        "neighbourhood_cleansed": ["South Boston Waterfront", "Back Bay", "Leather District", "Fenway"],
        "number_of_reviews": [10, 0, 5, 20],
        "log_price": [5.01, 4.39, 6.21, 3.00],
    })


# Data cleaning tests

def test_price_parsing_strips_symbols(raw_price_series): 
    """Replicates Section 1.2: strip "$" and ",", cast to float, drop null and zero price rows. """
    cleaned = (raw_price_series.astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False))
    parsed = pd.to_numeric(cleaned, errors="coerce")
    parsed = parsed.dropna()
    parsed = parsed[parsed > 0]
    assert (parsed > 0).all()
    assert len(parsed) == 3 # null and $0 are dropped
    assert 1200.0 in parsed.values # comma in "$1,200.00" is correctly removed

def test_log_price_reduces_skew():
    """log(1+price) should always produce lower skewness than raw price. """
    prices = pd.Series([50, 75, 100, 200, 500, 1200])
    log_prices = np.log1p(prices)
    assert log_prices.skew() < prices.skew()

def test_iqr_outlier_removal():
    """
    IQR cap: Q3 + 3 * IQR

    The extreme value 5000 should be removed. 
    """
    prices = pd.Series([50, 80, 100, 120, 150, 5000])
    Q1 = prices.quantile(0.25)
    Q3 = prices.quantile(0.75)
    upper = Q3 + 3 * (Q3 - Q1)
    filtered = prices[prices <= upper]
    assert 5000 not in filtered.values
    assert len(filtered) == 5


# Feature engineering

def test_is_shared_bath(sample_df):
    """
    Replicates Section: 1.8: flag rows where bathrooms_text contains "shared". 

    Expected: [0, 1, 0, 1] (rows 1 and 3 have shared bathrooms)
    """
    bath_text = sample_df["bathrooms_text"].astype(str).str.lower()
    flag = bath_text.str.contains("shared", na=False).astype(int)
    assert list(flag) == [0, 1, 0, 1]

def test_is_short_stay(sample_df):
    """
    Replicates Section: 1.4: flag listings with minimum_nights <= 2. 

    Expected: [1, 0, 0, 1] (rows 0 (1 night) and 3 (2 nights) qualify)
    """
    flag = (sample_df["minimum_nights"] <= 2).astype(int)
    assert list(flag) == [1, 0, 0, 1]

def test_amenity_wifi_flag(sample_df):
    """
    Replicates Section: 2.1: detect wifi in amenities string (case insensitive). 

    Expected: [1, 0, 1, 0] (rows 0 and 2 contain "Wifi")
    """
    flag = sample_df["amenities"].str.contains(r"wifi|wi-fi|wireless", case=False).astype(int)
    assert list(flag) == [1, 0, 1, 0]

def test_amenity_pet_flag(sample_df):
    """
    Replicates Section: 2.1: detect pet friendly listings. 

    Expected: [0, 1, 0, 0] (rows 1 has "Pets allowed")
    """
    flag = sample_df["amenities"].str.contains(r"pets allowed|pet allowed", case=False).astype(int)
    assert list(flag) == [0, 1, 0, 0]

def test_neighbourhood_consolidation(sample_df):
    """
    Replicates Section 1.9: merge small neighbourhoods into larger ones. 

    Examples:
    "South Boston Waterfront" -> "South Boston"
    "Leather District" -> "Downtown"
    """
    neigh_map ={
        "South Boston Waterfront": "South Boston", 
        "Leather District": "Downtown", 
        "Longwood Medical Area": "Fenway",
    }
    cleaned = sample_df["neighbourhood_cleansed"].replace(neigh_map)
    assert "South Boston Waterfront" not in cleaned.values
    assert "South Boston" in cleaned.values
    assert "Leather District" not in cleaned.values
    assert "Downtown" in cleaned.values


# No data leakage

def test_no_data_leakage_in_imputer():
    from sklearn.impute import SimpleImputer
    from sklearn.model_selection import train_test_split

    X = pd.DataFrame({"a": [1.0, 2.0, np.nan, 4.0, 5.0]})
    y = pd.Series([1, 2, 3, 4, 5])
    X_train, X_test, _, _ = train_test_split(X, y, test_size=0.4, random_state=0)

    imp = SimpleImputer(strategy="mean")
    imp.fit(X_train) # fit on train only, not on X (full dataset)

    train_mean = X_train["a"].dropna().mean()
    assert abs(imp.statistics_[0] - train_mean) < 1e-9, \
    "Imputer must be fit on training data only"