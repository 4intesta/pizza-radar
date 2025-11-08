import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Generate mock data
names = [f"Pizzeria {i}" for i in range(1, 21)]
latitudes = np.random.uniform(40.745, 40.755, size=20)
longitudes = np.random.uniform(-73.955, -73.945, size=20)
reviews_7d = np.random.randint(0, 50, size=20)
reviews_30d = reviews_7d + np.random.randint(0, 150, size=20)
ratings_7d = np.round(np.random.uniform(1.0, 5.0, size=20), 2)
ratings_30d = np.round((ratings_7d + np.random.uniform(-0.5, 0.5, size=20)).clip(1.0, 5.0), 2)

# Create DataFrame
competition_page_data = pd.DataFrame({
    "Name": names,
    "Latitude": latitudes,
    "Longitude": longitudes,
    "Number of Reviews last 7 days": reviews_7d,
    "Number of Reviews last 30 days": reviews_30d,
    "Average Rating last 7 days": ratings_7d,
    "Average Rating last 30 days": ratings_30d
})

print("Competition_page_data:")
print(competition_page_data.head())