import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

np.random.seed(42)

# =========================
# MOCK RAW DATA FROM DB
# =========================
names = [f"Pizzeria {i}" for i in range(1, 21)]
latitudes = np.random.uniform(40.745, 40.755, size=20)
longitudes = np.random.uniform(-73.955, -73.945, size=20)
mean_prices = [
    "€", "€€", "€€€", "€", "€€",
    "€€€", "€", "€€", "€€€", "€",
    "€€", "€€€", "€", "€€", "€€€",
    "€", "€€", "€€€", "€", "€€"
]

today = dt.date.today()
dates_last_year = [today - dt.timedelta(days=i) for i in range(364, -1, -1)]

# --- Base values for each pizzeria ---
base_values = {
    name: {
        "reviews": int(np.random.randint(0, 15)),
        "rating": float(np.round(np.random.uniform(1.0, 5.0), 2))
    }
    for name in names
}

# Set rating to 0 if reviews is 0
for name, values in base_values.items():
    if values["reviews"] == 0:
        values["rating"] = 0.0

# --- Daily fluctuating data ---
daily_data_last_year = {}

for name in names:
    daily_data_last_year[name] = {}
    base_reviews = base_values[name]["reviews"]
    base_rating = base_values[name]["rating"]
    
    for date in dates_last_year:
        # Reviews fluctuate ±3 (but never below 0)
        daily_reviews = max(0, int(np.random.normal(base_reviews, 2)))
        
        # Rating fluctuates ±0.5 around base (clipped 1.0 to 5.0)
        if daily_reviews == 0:
            daily_rating = 0.0
        else:
            daily_rating = float(np.clip(np.random.normal(base_rating, 0.3), 1.0, 5.0))
        
        daily_data_last_year[name][str(date)] = {
            "reviews": daily_reviews,
            "rating": daily_rating
        }

import random

# =========================
# ARRAY DI TAG
# =========================
tags = [
  "Napoletana","Romana","Gourmet","Classica","In teglia","Al taglio","A pala",
  "Senza glutine","Integrale","Canotto / Cornicione alto",
  "Forno a legna","Forno elettrico","Forno a gas","Cottura su pietra refrattaria",
  "Alta idratazione","Lievitazione lunga (24/48/72h)",
  "Ingredienti DOP/IGP","Mozzarella di bufala","Pomodoro San Marzano","Farine bio",
  "Impasto multicereali","Prodotti a km 0","Ingredienti stagionali","Impasto digeribile",
  "Tradizionale","Moderna","Street food","Family friendly","Rustica","Gourmet / di design",
  "Casual","Panoramica / vista mare","Vegetariana","Vegana","Senza lattosio",
  "Senza glutine certificato","Halal","Asporto","Consegna a domicilio","Prenotazione online",
  "Tavoli all’aperto","Menù degustazione","Carta dei vini","Birre artigianali",
  "Pagamenti digitali","Parcheggio","Dog-friendly","Economica","Media","Premium",
  "Gourmet / alta fascia","Pizza fritta","Calzone","Panuozzo","Pizza dolce",
  "Pizza creativa del mese"
]

# =========================
# CREATE STRUCTURE FOR TAG STORAGE YEARLY
# =========================
today = dt.date.today()
months_last_year = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(11, -1, -1)]

hot_topics_for_the_month = {
    name: {
        month: {
            "rating": random.sample(tags, k=3)
        }
        for month in months_last_year
    }
    for name in names
}

# =========================
# CREA HOT TOPICS PER ULTIMI 30 E 7 GIORNI
# =========================
hot_topics_last_30d = {}
hot_topics_last_7d = {}

for name in names:
    # 3 tag casuali dai tag generali
    last_30d_tags = random.sample(tags, k=3)
    hot_topics_last_30d[name] = last_30d_tags
    
    # 0, 1 o 2 tag presi dai 3 di hot_topics_last_30d
    n_tags_7d = random.randint(0, 2)
    last_7d_tags = random.sample(last_30d_tags, k=n_tags_7d)
    hot_topics_last_7d[name] = last_7d_tags

# =========================
# DATA MANIPULATION
# =========================
last_30_days = [today - dt.timedelta(days=i) for i in range(29, -1, -1)]
last_30_days_str = [str(d) for d in last_30_days]

daily_reviews_30d = np.array([
    [daily_data_last_year[name][day]["reviews"] for day in last_30_days_str]
    for name in names
])
ratings_30d_matrix = np.array([
    [daily_data_last_year[name][day]["rating"] for day in last_30_days_str]
    for name in names
])
ratings_7d_matrix = ratings_30d_matrix[:, -7:]

reviews_7d = daily_reviews_30d[:, -7:].sum(axis=1)
reviews_30d = daily_reviews_30d.sum(axis=1)

masked_30d = np.ma.masked_where(ratings_30d_matrix == 0, ratings_30d_matrix)
ratings_30d = np.round(masked_30d.mean(axis=1), 2)

masked_7d = np.ma.masked_where(ratings_7d_matrix == 0, ratings_7d_matrix)
ratings_7d = np.round(masked_7d.mean(axis=1), 2)

competition_page_data = pd.DataFrame({
    "Name": names,
    "Latitude": latitudes,
    "Longitude": longitudes,
    "Daily Reviews (30d)": daily_reviews_30d.tolist(),
    "Daily Ratings (30d)": ratings_30d_matrix.tolist(),
    "Number of Reviews last 7 days": reviews_7d,
    "Number of Reviews last 30 days": reviews_30d,
    "Average Rating last 7 days": ratings_7d,
    "Average Rating last 30 days": ratings_30d,
    "Mean Price": mean_prices
})

#adding labels
for month in months_last_year:
    competition_page_data[f"Tags {month}"] = None

for idx, name in enumerate(names):
    for month in months_last_year:
        competition_page_data.at[idx, f"Tags {month}"] = hot_topics_for_the_month[name][month]["rating"]

competition_page_data["hot_topics_last_30d"] = competition_page_data["Name"].map(hot_topics_last_30d)
competition_page_data["hot_topics_last_7d"] = competition_page_data["Name"].map(hot_topics_last_7d)

# ----------------------------------------------------
# Compute MONTHLY historical data from daily_data_last_year
# ----------------------------------------------------
num_months = 12
monthly_reviews = []
monthly_ratings = []

for name in names:
    pizzeria_data = daily_data_last_year[name]
    
    monthly_review_counts = []
    monthly_rating_means = []
    
    # Go month by month from 12 months ago to this month
    for i in range(num_months - 1, -1, -1):
        # define month start and end
        month_start = (today - relativedelta(months=i)).replace(day=1)
        next_month_start = (month_start + relativedelta(months=1))
        
        # collect all days in that month that exist in our data
        days_in_month = [
            day for day in pizzeria_data.keys()
            if month_start <= dt.date.fromisoformat(day) < next_month_start
        ]
        
        # extract reviews and ratings for those days
        if days_in_month:
            month_reviews = [pizzeria_data[day]["reviews"] for day in days_in_month]
            month_ratings = [pizzeria_data[day]["rating"] for day in days_in_month if pizzeria_data[day]["reviews"] > 0]
            
            monthly_review_counts.append(int(np.sum(month_reviews)))
            monthly_rating_means.append(
                float(np.round(np.mean(month_ratings), 2)) if month_ratings else np.nan
            )
        else:
            # if no data for that month
            monthly_review_counts.append(0)
            monthly_rating_means.append(np.nan)
    
    monthly_reviews.append(monthly_review_counts)
    monthly_ratings.append(monthly_rating_means)

competition_page_data["Last Year Monthly Reviews"] = monthly_reviews
competition_page_data["Last Year Monthly Ratings"] = monthly_ratings

print("\nCompetition_page_data (with monthly data):")
print(competition_page_data[["Name", "Last Year Monthly Reviews", "Last Year Monthly Ratings"]].head())