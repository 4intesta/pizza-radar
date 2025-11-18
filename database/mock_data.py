import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import random

np.random.seed(42)
random.seed(42)

# =========================================================
# 1. BASIC SETTINGS
# =========================================================

def generate_base_settings(num_pizzerias=20):
    names = [f"Pizzeria {i}" for i in range(1, num_pizzerias + 1)]
    latitudes = np.random.uniform(45.468, 45.478, size=num_pizzerias)
    longitudes = np.random.uniform(9.182, 9.192, size=num_pizzerias)
    mean_prices = ["€", "€€", "€€€"] * (num_pizzerias // 3 + 1)
    mean_prices = mean_prices[:num_pizzerias]

    today = dt.date.today()
    dates_last_year = [today - dt.timedelta(days=i) for i in range(364, -1, -1)]

    return names, latitudes, longitudes, mean_prices, today, dates_last_year

# =========================================================
# 2. BASE VALUES PER PIZZERIA
# =========================================================

def generate_base_values(names):
    base_values = {
        name: {
            "reviews": int(np.random.randint(0, 15)),
            "rating": float(np.round(np.random.uniform(1.0, 5.0), 2))
        }
        for name in names
    }
    for values in base_values.values():
        if values["reviews"] == 0:
            values["rating"] = 0.0
    return base_values

# =========================================================
# 3. DAILY DATA FOR LAST YEAR
# =========================================================

def generate_daily_last_year(names, dates_last_year, base_values):
    daily_data = {}
    for name in names:
        daily_data[name] = {}
        base_reviews = base_values[name]["reviews"]
        base_rating = base_values[name]["rating"]

        for date in dates_last_year:
            reviews = max(0, int(np.random.normal(base_reviews, 2)))
            rating = 0.0 if reviews == 0 else float(np.clip(np.random.normal(base_rating, 0.3), 1.0, 5.0))
            daily_data[name][str(date)] = {"reviews": reviews, "rating": rating}

    return daily_data

# =========================================================
# 4. TAGS + HOT TOPICS
# =========================================================

def generate_tags():
    return [
        "Napoletana","Romana","Gourmet","Classica","In teglia","Al taglio","A pala",
        "Senza glutine","Integrale","Canotto / Cornicione alto","Forno a legna","Forno elettrico",
        "Forno a gas","Cottura su pietra refrattaria","Alta idratazione","Lievitazione lunga (24/48/72h)",
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

def generate_hot_topics(names, tags, today):
    # Monthly topics
    months_last_year = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(11, -1, -1)]
    hot_topics_month = {name: {month: {"rating": random.sample(tags, k=3)} for month in months_last_year} for name in names}

    # Weekly topics (52 weeks)
    weeks_last_year = [(today - dt.timedelta(weeks=i)).strftime("%Y-W%W") for i in range(51, -1, -1)]
    hot_topics_week = {name: {week: {"rating": random.sample(tags, k=random.randint(0,2))} for week in weeks_last_year} for name in names}

    # Last 30d / 7d topics
    hot_topics_last_30d = {name: random.sample(tags, k=3) for name in names}
    hot_topics_last_7d = {name: random.sample(hot_topics_last_30d[name], k=random.randint(0,2)) for name in names}

    return months_last_year, weeks_last_year, hot_topics_month, hot_topics_week, hot_topics_last_30d, hot_topics_last_7d

# =========================================================
# 5. LAST 30 DAYS DATA MATRICES
# =========================================================

def extract_last_30d_matrices(names, today, daily_data):
    last_30_days = [today - dt.timedelta(days=i) for i in range(29, -1, -1)]
    last_30_days_str = [str(d) for d in last_30_days]

    reviews_30d = np.array([[daily_data[name][day]["reviews"] for day in last_30_days_str] for name in names])
    ratings_30d = np.array([[daily_data[name][day]["rating"] for day in last_30_days_str] for name in names])

    return reviews_30d, ratings_30d

# =========================================================
# 6. COMPUTE AGGREGATES
# =========================================================

def compute_aggregates(reviews_30d, ratings_30d):
    reviews_7d = reviews_30d[:, -7:].sum(axis=1)
    reviews_30d_sum = reviews_30d.sum(axis=1)

    weighted_7d = (ratings_30d[:, -7:] * reviews_30d[:, -7:]).sum(axis=1)
    ratings_7d = np.round(np.divide(weighted_7d, reviews_7d, out=np.zeros_like(weighted_7d), where=reviews_7d!=0), 2)

    weighted_30d = (ratings_30d * reviews_30d).sum(axis=1)
    ratings_30d_avg = np.round(np.divide(weighted_30d, reviews_30d_sum, out=np.zeros_like(weighted_30d), where=reviews_30d_sum!=0), 2)

    return reviews_7d, reviews_30d_sum, ratings_7d, ratings_30d_avg

# =========================================================
# 7. MONTHLY HISTORICAL DATA
# =========================================================

def compute_monthly_history(names, today, daily_data):
    monthly_reviews = []
    monthly_ratings = []
    num_months = 12

    for name in names:
        p_data = daily_data[name]
        reviews_per_month = []
        ratings_per_month = []

        for i in range(num_months - 1, -1, -1):
            month_start = (today - relativedelta(months=i)).replace(day=1)
            next_month_start = month_start + relativedelta(months=1)
            days_in_month = [d for d in p_data.keys() if month_start <= dt.date.fromisoformat(d) < next_month_start]

            if days_in_month:
                revs = [p_data[d]["reviews"] for d in days_in_month]
                rats = [p_data[d]["rating"] for d in days_in_month if p_data[d]["reviews"] > 0]
                reviews_per_month.append(int(np.sum(revs)))
                ratings_per_month.append(float(np.round(np.mean(rats), 2)) if rats else np.nan)
            else:
                reviews_per_month.append(0)
                ratings_per_month.append(np.nan)

        monthly_reviews.append(reviews_per_month)
        monthly_ratings.append(ratings_per_month)

    return monthly_reviews, monthly_ratings

# =========================================================
# 7.bis WEEKLY HISTORICAL DATA
# =========================================================

def compute_weekly_history(names, today, daily_data):
    weekly_reviews = []
    weekly_ratings = []
    num_weeks = 52

    for name in names:
        p_data = daily_data[name]
        reviews_per_week = []
        ratings_per_week = []

        for i in range(num_weeks - 1, -1, -1):
            week_start = today - dt.timedelta(weeks=i)
            week_start = week_start - dt.timedelta(days=week_start.weekday())  # Monday
            week_end = week_start + dt.timedelta(days=7)

            days_in_week = [d for d in p_data.keys() if week_start <= dt.date.fromisoformat(d) < week_end]

            if days_in_week:
                revs = [p_data[d]["reviews"] for d in days_in_week]
                rats = [p_data[d]["rating"] for d in days_in_week if p_data[d]["reviews"] > 0]
                reviews_per_week.append(int(np.sum(revs)))
                ratings_per_week.append(float(np.round(np.mean(rats), 2)) if rats else np.nan)
            else:
                reviews_per_week.append(0)
                ratings_per_week.append(np.nan)

        weekly_reviews.append(reviews_per_week)
        weekly_ratings.append(ratings_per_week)

    return weekly_reviews, weekly_ratings

# =========================================================
# 8. BUILD FINAL DATAFRAME
# =========================================================

def build_competition_page_data(
    names, latitudes, longitudes, mean_prices,
    reviews_30d, ratings_30d, reviews_7d, reviews_30d_sum, ratings_7d, ratings_30d_avg,
    months_last_year, hot_topics_month, weeks_last_year, hot_topics_week,
    hot_topics_last_30d, hot_topics_last_7d,
    monthly_reviews, monthly_ratings,
    weekly_reviews, weekly_ratings
):
    df = pd.DataFrame({
        "Name": names,
        "Latitude": latitudes,
        "Longitude": longitudes,
        "Daily Reviews (30d)": reviews_30d.tolist(),
        "Daily Ratings (30d)": ratings_30d.tolist(),
        "Number of Reviews last 7 days": reviews_7d,
        "Number of Reviews last 30 days": reviews_30d_sum,
        "Average Rating last 7 days": ratings_7d,
        "Average Rating last 30 days": ratings_30d_avg,
        "Mean Price": mean_prices,
        "Last Year Monthly Reviews": monthly_reviews,
        "Last Year Monthly Ratings": monthly_ratings,
        "Last Year Weekly Reviews": weekly_reviews,
        "Last Year Weekly Ratings": weekly_ratings
    })

    # Monthly tags
    for month in months_last_year:
        df[f"Tags {month}"] = [hot_topics_month[name][month]["rating"] for name in names]

    # Weekly topics
    df["hot_topics_week"] = df["Name"].map(hot_topics_week)

    # Last 30d / 7d topics
    df["hot_topics_last_30d"] = df["Name"].map(hot_topics_last_30d)
    df["hot_topics_last_7d"] = df["Name"].map(hot_topics_last_7d)

    return df

# =========================================================
# 9. EXECUTE EVERYTHING
# =========================================================

names, latitudes, longitudes, mean_prices, today, dates_last_year = generate_base_settings()
base_values = generate_base_values(names)
daily_data_last_year = generate_daily_last_year(names, dates_last_year, base_values)

tags = generate_tags()
months_last_year, weeks_last_year, hot_topics_month, hot_topics_week, hot_topics_last_30d, hot_topics_last_7d = generate_hot_topics(names, tags, today)

reviews_30d, ratings_30d = extract_last_30d_matrices(names, today, daily_data_last_year)
reviews_7d, reviews_30d_sum, ratings_7d, ratings_30d_avg = compute_aggregates(reviews_30d, ratings_30d)

monthly_reviews, monthly_ratings = compute_monthly_history(names, today, daily_data_last_year)
weekly_reviews, weekly_ratings = compute_weekly_history(names, today, daily_data_last_year)

competition_page_data = build_competition_page_data(
    names, latitudes, longitudes, mean_prices,
    reviews_30d, ratings_30d, reviews_7d, reviews_30d_sum, ratings_7d, ratings_30d_avg,
    months_last_year, hot_topics_month, weeks_last_year, hot_topics_week,
    hot_topics_last_30d, hot_topics_last_7d,
    monthly_reviews, monthly_ratings,
    weekly_reviews, weekly_ratings
)

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