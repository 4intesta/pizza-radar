import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_mock_competitors():
    """Generate mock data for competitors comparison"""
    data = {
        'Nome': ['La Mia Pizzeria', 'Pizza Express', 'Napoli Corner', 'Pizza Hub'],
        'Prezzo Margherita': [8.50, 9.00, 8.00, 7.50],
        'Rating': [0, 4, 4.1, 3.9],
        'Recensioni': [120, 85, 95, 150],
        'Menu Items': [25, 20, 15, 30],
        'Prezzo Medio Menu': [12.50, 13.00, 11.50, 10.50],
        'Tempo Permanenza Max': [1.5, 2.0, 1.25, 1.75]  # Added new field (in hours)
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
    """Generate all historical reviews with aspect ratings"""
    reviews = [
        # Recent reviews (last 3 months)
        {
            'Data': datetime.now() - timedelta(days=5),
            'Rating': 4.5,
            'Testo': "Pizza napoletana autentica, impasto perfetto! Servizio veloce e cordiale.",
            'Autore': "Marco S.",
            'Fonte': "Google",
            'Cibo': 5.0,
            'Servizio': 4.0,
            'Ambiente': 4.5
        },
        {
            'Data': datetime.now() - timedelta(days=12),
            'Rating': 2.0,
            'Testo': "Attesa troppo lunga nel weekend, pizza tiepida all'arrivo.",
            'Autore': "Laura B.",
            'Fonte': "Tripadvisor",
            'Cibo': 2.5,
            'Servizio': 1.5,
            'Ambiente': 3.0
        },
        {
            'Data': datetime.now() - timedelta(days=25),
            'Rating': 5.0,
            'Testo': "La migliore margherita della zona! Personale gentilissimo.",
            'Autore': "Giuseppe R.",
            'Fonte': "Deliveroo",
            'Cibo': 5.0,
            'Servizio': 5.0,
            'Ambiente': 4.5
        },
        {
            'Data': datetime.now() - timedelta(days=45),
            'Rating': 4.0,
            'Testo': "Ottimo rapporto qualità-prezzo, ambiente accogliente.",
            'Autore': "Sofia M.",
            'Fonte': "Google",
            'Cibo': 4.0,
            'Servizio': 4.0,
            'Ambiente': 4.0
        },
        {
            'Data': datetime.now() - timedelta(days=60),
            'Rating': 3.5,
            'Testo': "Pizza buona ma servizio lento nel weekend.",
            'Autore': "Andrea B.",
            'Fonte': "Tripadvisor",
            'Cibo': 4.0,
            'Servizio': 2.5,
            'Ambiente': 3.5
        },
        {
            'Data': datetime.now() - timedelta(days=80),
            'Rating': 4.5,
            'Testo': "Ingredienti di prima qualità, personale professionale.",
            'Autore': "Elena P.",
            'Fonte': "Google",
            'Cibo': 5.0,
            'Servizio': 4.0,
            'Ambiente': 4.0
        },
        # Older reviews (3-6 months ago)
        {
            'Data': datetime.now() - timedelta(days=120),
            'Rating': 3.5,
            'Testo': "Buona pizza ma prezzi un po' alti per la zona.",
            'Autore': "Luca M.",
            'Fonte': "Deliveroo",
            'Cibo': 4.0,
            'Servizio': 3.5,
            'Ambiente': 3.0
        },
        {
            'Data': datetime.now() - timedelta(days=140),
            'Rating': 1.5,
            'Testo': "Esperienza deludente, tempi di attesa assurdi.",
            'Autore': "Paolo F.",
            'Fonte': "Tripadvisor",
            'Cibo': 2.0,
            'Servizio': 1.0,
            'Ambiente': 2.5
        },
        {
            'Data': datetime.now() - timedelta(days=160),
            'Rating': 4.0,
            'Testo': "Locale molto carino, pizza buona e personale attento.",
            'Autore': "Chiara D.",
            'Fonte': "Google",
            'Cibo': 4.0,
            'Servizio': 4.5,
            'Ambiente': 4.5
        },
        {
            'Data': datetime.now() - timedelta(days=180),
            'Rating': 3.0,
            'Testo': "Qualità altalenante, a volte ottima a volte così così.",
            'Autore': "Roberto N.",
            'Fonte': "Tripadvisor",
            'Cibo': 3.0,
            'Servizio': 3.5,
            'Ambiente': 3.0
        }
    ]
    return pd.DataFrame(reviews).sort_values('Data', ascending=False)

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