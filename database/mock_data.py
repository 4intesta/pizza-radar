import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Generate mock data
names = [f"Pizzeria {i}" for i in range(1, 21)]
latitudes = np.random.uniform(40.745, 40.755, size=20)
longitudes = np.random.uniform(-73.955, -73.945, size=20)

# Generate number of reviews and ratings per day for the last 30 days for each pizzeria
daily_reviews_30d = np.random.randint(0, 10, size=(20, 30))  # shape (20 pizzerias, 30 days)
ratings_30d_matrix = np.round(np.random.uniform(1.0, 5.0, size=(20, 30)), 2)
reviews_7d = daily_reviews_30d[:, -7:].sum(axis=1)   # sum of last 7 days
reviews_30d = daily_reviews_30d.sum(axis=1)          # sum of last 30 days

# The last 7 days for each pizzeria
ratings_7d_matrix = ratings_30d_matrix[:, -7:]
ratings_30d = np.round(ratings_30d_matrix.mean(axis=1), 2)
ratings_7d = np.round(ratings_7d_matrix.mean(axis=1), 2)

# Generate average pizza prices (e.g., between €5 and €20)
mean_prices = np.round(np.random.uniform(5, 20, size=20), 2)

# Create DataFrame
competition_page_data = pd.DataFrame({
    "Name": names,
    "Latitude": latitudes,
    "Longitude": longitudes,
    "Daily Reviews (30d)": daily_reviews_30d.tolist(), #this is a list of values
    "Daily Ratings (30d)": ratings_30d_matrix.tolist(), #this is a list of values
    "Number of Reviews last 7 days": reviews_7d, #this is a single value
    "Number of Reviews last 30 days": reviews_30d, #this is a single value
    "Average Rating last 7 days": ratings_7d, #this is a single value
    "Average Rating last 30 days": ratings_30d, #this is a single value
    "Mean Price": mean_prices
})

print("Competition_page_data:")
print(competition_page_data.head())

# ----------------------------------------------------
# 2. Add WEEKLY historical data (52 weeks). 
# [0] = 1 year ago, [51] = last week
# ----------------------------------------------------
num_weeks = 52
competition_page_data["Last Year Weekly Reviews"] = [
    np.random.randint(0, 80, size=num_weeks).tolist()
    for _ in range(len(competition_page_data))
]
competition_page_data["Last Year Weekly Ratings"] = [
    np.round(np.random.uniform(1.0, 5.0, size=num_weeks), 2).tolist()
    for _ in range(len(competition_page_data))
]

# ----------------------------------------------------
# 3. Add MONTHLY historical data (12 months). 
# [0] = 1 year ago, [11] = last month
# ----------------------------------------------------
num_months = 12
competition_page_data["Last Year Monthly Reviews"] = [
    np.random.randint(0, 300, size=num_months).tolist()
    for _ in range(len(competition_page_data))
]
competition_page_data["Last Year Monthly Ratings"] = [
    np.round(np.random.uniform(1.0, 5.0, size=num_months), 2).tolist()
    for _ in range(len(competition_page_data))
]