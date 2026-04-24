# Project Title: Boston Airbnb Pricing Prediction Model

### Liting Zheng, Zhihui Qian, Siyuan Wang, Lina Yingying Zhang

## 1. Project Description
This project focuses on predicting the nightly price of Airbnb listings in Boston using Airbnb open data(23 September 2025). The model will use listing features such as location, room type, number of bedrooms, amenities, availability, and seasonal factors to estimate a reasonable price per night. By examining how these features influence pricing, the project applies data analysis techniques to capture pricing patterns in the Boston Airbnb market and provide interpretable insights into the factors that drive price differences across listings.

## 2. Project Goals
* **Build a predictive model** that estimates the nightly price of Airbnb listings in Boston using listing features such as location, room type, capacity and amenities.
* **Evaluate the accuracy** of the model using measurable metrics to determine how closely predicted prices match actual listing prices.
* **Identify the most influential factors** affecting price by analyzing feature importance and visualizing key relationships in the data.
* **Support better pricing decisions** for new Airbnb hosts by demonstrating how data-driven price estimates can help avoid underpricing or overpricing listings.


## 3. Timeline
* **March** (First Project Check-in):
  1. Complete data cleaning.(2 weeks)
  2. Conduct exploratory data analysis (EDA) to figure out key features and pricing patterns.(1 week)
  3. Discussing initial modeling ideas and challenges.(half week)
* **April** (Second Project Check-in):
  1. Build and refine predictive models.(2 weeks)
  2. Evaluate model performance.(1 week)
  3. Analyze feature importance and adjust the model based on first check-in.(half week)
* Submit final report and presentation.


## 4. Data Collection Plan
We plan to use data from [Inside Airbnb](http://insideairbnb.com/get-the-data/), an open-source project that collects quarterly information about Airbnb listings across different cities and countries via web scraping and makes it available for the public. Specifically, we will use the listings.csv for Boston Massachusetts, scraped on September 23, 2025 which is the most up-to-date dataset available.
The data will be downloaded in CSV format and loaded using the pandas library. We will then perform data processing, which includes handling missing values and conducting feature engineering, such as extracting temporal features, creating interaction features, one-hot-encoding for categorical variables, etc.

## 5. Modeling Plan
Based on a review of prior research and online resources, our project will adopt a multi-model approach. We list all possible approaches we will consider below.
* **Baseline Model:**
  1. Mean/ Median Price Model: Used as a baseline to evaluate whether more advanced models provide meaningful improvement.
  2. Linear Regression: Linear regression will help us understand linear relationship between listing characteristics (Continuous variables).
  3. WOE and VI: Feature selection.
* **Tree-based Ensemble Models:**
  1. Random Forest Regression (Categorical variables): Capture non-linear interactions between features, robust to outliers and missing values, and provide features important for preliminary interpretation.
  2. XGBoost: Expected to be the primary predictive model. Its models feature interactions, such as the joint effect between variables.
* **Support Vector Regression (SVR)**

## 6. Visualization Plan
Our visualization will support both EDA and result interpretation. 
Tools: matplotlin, seaborn, plotly, folium (for geographic maps)
* **Exploratory Data Analysis:**
  * Price distribution: histogram and box plot to identify outliers
  * Geographic analysis: choropleth map showing average price by neighborhood
  * Correlation heatmap: identify relationships between numerical features
  * Scatter plots: price vs. key features (bedrooms, accommodations, review scores)
* **Model Results:**
  * Feature importance bar charts: top 10-15 features driving price predictions
  * Actual vs. predicted price: scatter plot with regression line
  * Residual plots: identify systematic prediction errors
  * SHAP summary plot (if time permits): explain individual predictions


## 7. Testing Plan
To evaluate the performance, we will use the following strategies:
* **Train test split:** we plan to split the dataset with a 80-20 split, using 80% of the data for training and 20% for testing.
* **Evaluation metrics:**
RMSE to penalize and identify any significant mistakes
R^2 to determine the proportion of variance our model explains
* **Baseline comparison:**
we will compare the different models we’ve trained and understand which is the best approach.
* **Cross-validation:**
we will use 5-fold cross validation to ensure our results are consistent and not biased by a specific split of the data.
* **Error Analysis:**
we will analyze residuals by neighborhood and property type to identify where the model underperforms and potential areas for improvement. 
