import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import random

np.random.seed(42)

# =========================
# 1. BASIC SETTINGS
# =========================
names = [f"Pizzeria {i}" for i in range(1, 21)]
latitudes = np.random.uniform(45.468, 45.478, size=20)
longitudes = np.random.uniform(9.182, 9.192, size=20)
mean_prices = [
    "€", "€€", "€€€", "€", "€€",
    "€€€", "€", "€€", "€€€", "€",
    "€€", "€€€", "€", "€€", "€€€",
    "€", "€€", "€€€", "€", "€€"
]

today = dt.date.today()
dates_last_year = [today - dt.timedelta(days=i) for i in range(364, -1, -1)]

# =========================
# 2. BASE DATA PER PIZZERIA
# =========================
base_values = {
    name: {
        "reviews": int(np.random.randint(0, 15)),
        "rating": float(np.round(np.random.uniform(1.0, 5.0), 2))
    }
    for name in names
}

# Rating = 0 if reviews = 0
for name, values in base_values.items():
    if values["reviews"] == 0:
        values["rating"] = 0.0

# =========================
# 3. DAILY FLUCTUATING DATA FOR 1 YEAR
# =========================
daily_data_last_year = {}

for name in names:
    daily_data_last_year[name] = {}
    base_reviews = base_values[name]["reviews"]
    base_rating = base_values[name]["rating"]
    
    for date in dates_last_year:

        # Daily reviews fluctuate around base
        daily_reviews = max(0, int(np.random.normal(base_reviews, 2)))

        # Ratings fluctuate, but 0 if no reviews
        if daily_reviews == 0:
            daily_rating = 0.0
        else:
            daily_rating = float(np.clip(np.random.normal(base_rating, 0.3), 1.0, 5.0))

        daily_data_last_year[name][str(date)] = {
            "reviews": daily_reviews,
            "rating": daily_rating
        }

# =========================
# 4. TAGS
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
# 5. TAGS - MONTHLY, 30D, 7D
# =========================
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

hot_topics_last_30d = {}
hot_topics_last_7d = {}

for name in names:
    last_30d_tags = random.sample(tags, k=3)
    hot_topics_last_30d[name] = last_30d_tags
    
    n_tags_7d = random.randint(0, 2)
    last_7d_tags = random.sample(last_30d_tags, k=n_tags_7d)
    hot_topics_last_7d[name] = last_7d_tags

# =========================
# 6. EXTRACT LAST 30 DAYS DATA
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

# =========================
# 7. REVIEW COUNTS
# =========================
reviews_7d_matrix = daily_reviews_30d[:, -7:]
reviews_30d_matrix = daily_reviews_30d

reviews_7d = reviews_7d_matrix.sum(axis=1)
reviews_30d = reviews_30d_matrix.sum(axis=1)

# =========================
# 8. WEIGHTED AVERAGE RATINGS
# =========================

# Weighted average for last 7 days
weighted_sum_7d = (ratings_30d_matrix[:, -7:] * reviews_7d_matrix).sum(axis=1)
ratings_7d = np.round(
    np.divide(weighted_sum_7d, reviews_7d, out=np.zeros_like(weighted_sum_7d), where=reviews_7d!=0),
    2
)

# Weighted average for last 30 days
weighted_sum_30d = (ratings_30d_matrix * reviews_30d_matrix).sum(axis=1)
ratings_30d = np.round(
    np.divide(weighted_sum_30d, reviews_30d, out=np.zeros_like(weighted_sum_30d), where=reviews_30d!=0),
    2
)

# =========================
# 9. FINAL DATAFRAME
# =========================
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





######################################
reviews = [
    {
        "author": "Luca B.",
        "date": "2024-02-10",
        "platform": "Google",
        "rating": 5,
        "text": "Pizza eccellente, servizio veloce e personale gentilissimo.",
        "subratings": {
            "cibo": 5,
            "qualità-prezzo": 4,
            "servizio": 5,
            "ambiente": 4
        },
        "tags": ["pizza", "servizio impeccabile", "familiare"],
        "ownerResponse": True
    },
    {
        "author": "Sara M.",
        "date": "2024-02-08",
        "platform": "TripAdvisor",
        "rating": 4,
        "text": "Buona pizza, locale accogliente ma tempi di attesa un po' lunghi.",
        "subratings": {
            "cibo": 4,
            "qualità-prezzo": 4,
            "servizio": 3,
            "ambiente": 5
        },
        "tags": ["accogliente", "attesa lunga"],
        "ownerResponse": True
    },
    {
        "author": "Marco R.",
        "date": "2024-02-02",
        "platform": "TheFork",
        "rating": 3,
        "text": "Qualità discreta ma rapporto qualità-prezzo migliorabile.",
        "subratings": {
            "cibo": 3,
            "qualità-prezzo": 2,
            "servizio": 4,
            "ambiente": 3
        },
        "tags": ["qualità-prezzo", "moderato"],
        "ownerResponse": True
    },
    {
        "author": "Giulia P.",
        "date": "2024-01-28",
        "platform": "Google",
        "rating": 5,
        "subratings": {
            "cibo": 5,
            "qualità-prezzo": 5,
            "servizio": 5,
            "ambiente": 4
        },
        "tags": ["top", "consigliato", "pizza eccellente"],
        "ownerResponse": False
    },
    {
        "author": "Andrea V.",
        "date": "2024-01-20",
        "platform": "TripAdvisor",
        "rating": 2,
        "ownerResponse": False
    }
]