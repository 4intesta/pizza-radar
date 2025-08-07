import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_mock_competitors():
    """Generate mock data for competitors comparison"""
    data = {
        'Nome': ['La Mia Pizzeria', 'Pizza Express', 'Napoli Corner', 'Pizza Hub', 
                'Bella Napoli', 'Don Giovanni', 'Pizzeria Italia', 'Il Forno', 
                'Il Forno1', 'Il Forno2', 'Il Forno3', 'Il Forno4'],
        'Prezzo Margherita': [8.50, 9.00, 8.00, 7.50, 8.80, 9.50, 7.80, 8.30, 6, 6, 6, 6],
        'avgRating': [0, 4.0, 4.1, 3.9, 4.3, 4.5, 3.8, 4.2, 4.0, 4.1, 4.2, 4.3],
        'avgRatingCibo': [0, 4.2, 4.3, 4.0, 4.5, 4.6, 3.9, 4.3, 4.1, 4.2, 4.3, 4.4],
        'avgRatingServizio': [0, 3.9, 4.0, 3.8, 4.2, 4.4, 3.7, 4.1, 3.9, 4.0, 4.1, 4.2],
        'avgRatingAtmosfera': [0, 4.1, 4.0, 3.9, 4.3, 4.5, 3.8, 4.2, 4.0, 4.1, 4.2, 4.3],
        'Recensioni': [120, 85, 95, 150, 200, 180, 90, 130, 50, 60, 70, 80],
        'Menu Items': [25, 20, 15, 30, 22, 28, 18, 24, 10, 12, 14, 16],
        'Prezzo Medio Menu': [12.50, 13.00, 11.50, 10.50, 13.50, 14.00, 11.00, 12.00, 9.0, 9.5, 10.0, 10.5],
        'Tempo Attesa Max': [45, 60, 35, 50, 55, 65, 40, 45, 30, 35, 40, 45]  # Changed to minutes
    }
    return pd.DataFrame(data)

def get_historical_data():
    """Generate mock historical data for trends"""
    end_date = datetime.now()
    dates = pd.date_range(end=end_date, periods=6, freq='M')
    pizzerias = ['La Mia Pizzeria', 'Pizza Express', 'Napoli Corner', 'Pizza Hub']
    
    # Generate ratings data
    ratings_data = []
    prices_data = []
    
    for pizzeria in pizzerias:
        base_rating = np.random.uniform(3.8, 4.5)
        base_price = np.random.uniform(7.0, 9.0)
        
        for date in dates:
            ratings_data.append({
                'Pizzeria': pizzeria,
                'Data': date,
                'Rating': base_rating + np.random.uniform(-0.2, 0.2)
            })
            prices_data.append({
                'Pizzeria': pizzeria,
                'Data': date,
                'Prezzo': base_price + np.random.uniform(-0.5, 0.5)
            })
    
    return (pd.DataFrame(ratings_data), 
            pd.DataFrame(prices_data))

def get_recent_rating(ratings_df, pizzeria_name, months=3):
    """Calculate average rating for the last n months"""
    recent_data = ratings_df[
        (ratings_df['Pizzeria'] == pizzeria_name) & 
        (ratings_df['Data'] >= datetime.now() - timedelta(days=30*months))
    ]
    return recent_data['Rating'].mean()

def get_all_reviews():
    """Generate 3 years of historical reviews with aspect ratings"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*3)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Base ratings with some randomness
    base_ratings = {
        'Rating': 3,
        'Cibo': 3,
        'Servizio': 3,
        'Ambiente': 3
    }
    
    reviews = []
    for date in dates:
        # Add some seasonality and random variation
        seasonal_factor = 0.2 * np.sin(2 * np.pi * date.dayofyear / 365)
        random_factor = np.random.normal(0, 0.3)
        
        review = {
            'Data': date,
            'Rating': min(5, max(1, base_ratings['Rating'] + seasonal_factor + random_factor)),
            'Cibo': min(5, max(1, base_ratings['Cibo'] + seasonal_factor + np.random.normal(0, 0.2))),
            'Servizio': min(5, max(1, base_ratings['Servizio'] + seasonal_factor + np.random.normal(0, 0.3))),
            'Ambiente': min(5, max(1, base_ratings['Ambiente'] + seasonal_factor + np.random.normal(0, 0.2))),
            'Autore': f"User_{np.random.randint(1000)}",
            'Fonte': np.random.choice(['Google', 'Tripadvisor', 'Deliveroo']),
            'Testo': "Review text"  # Simplified for this example
        }
        reviews.append(review)
    
    return pd.DataFrame(reviews)

def get_recent_reviews():
    """Retrieve only reviews from the last 3 months"""
    all_reviews = get_all_reviews()
    three_months_ago = datetime.now() - timedelta(days=90)
    return all_reviews[all_reviews['Data'] >= three_months_ago]

def get_aspect_ratings(reviews_df):
    """Calculate average ratings for different aspects"""
    current_date = datetime.now()
    three_months_ago = current_date - timedelta(days=90)
    
    # Last 3 months data
    recent_reviews = reviews_df[reviews_df['Data'] >= three_months_ago]
    aspects = ['Cibo', 'Servizio', 'Ambiente']
    
    all_time = {aspect: round(reviews_df[aspect].mean(), 1) for aspect in aspects}
    last_3m = {aspect: round(recent_reviews[aspect].mean(), 1) for aspect in aspects}
    
    return {
        'all_time': all_time,
        'last_3_months': last_3m
    }

def get_ai_insights():
    """Return simplified AI insights with main strength, weakness and summary."""
    return {
        'main_strength': 'Qualità del cibo eccellente, con un rating medio di 4.8/5 per la categoria "Cibo"',
        'main_weakness': 'Tempi di attesa elevati nelle ore di punta (>45 min)',
        'summary': 'Il locale mantiene un ottimo standard qualitativo ma potrebbe migliorare l\'efficienza del servizio per ridurre i tempi di attesa.'
    }