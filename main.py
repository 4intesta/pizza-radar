import config  # Must be the very first import
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
from data_mock import get_all_reviews, get_mock_competitors, get_historical_data, get_recent_rating, get_recent_reviews, get_aspect_ratings, get_ai_insights

# Add custom CSS for better tab styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }

    .review-card {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
    }

    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
        color: #666;
        font-size: 0.9rem;
    }

    .review-source {
        background-color: #f8f9fa;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        color: #1E3D59;
    }

    .review-rating {
        color: #ffd700;
        font-size: 0.9rem;
    }

    .aspect-ratings {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid #eee;
    }

    .aspect-ratings span {
        margin-right: 1rem;
    }

    /* Style for negative reviews */
    .review-card.negative {
        background-color: #fff5f5;
    }

    .ai-card {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 0.5rem 1.5rem 1.5rem 1.5rem; /* top right bottom left */
        margin-bottom: 2rem;
    }

    .ai-header {
        color: #1E3D59;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .suggestion-card {
        background: white;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border: 1px solid #e6e9ef;
    }
    .suggestion-priority {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .priority-alta {
        background-color: #ffe4e4;
        color: #cf0000;
    }
    .priority-media {
        background-color: #fff4e4;
        color: #b25000;
    }
    .priority-alta.strength {
        background-color: #e4ffe4;
        color: #008000;
    }
    
    .priority-alta.summary {
        background-color: #e4f1ff;
        color: #0066cc;
    }

    .analysis-text {
        background: white;
        padding: 1.2rem;
        border-radius: 6px;
        margin-top: 1rem;
        border: 1px solid #e6e9ef;
        line-height: 1.6;
        white-space: pre-line;
    }
    
    </style>
""", unsafe_allow_html=True)

st.title("La Mia Pizzeria")

# Load mock data
competitors_df = get_mock_competitors()
ratings_history, prices_history = get_historical_data()

# Create tabs
tab1, tab2 = st.tabs(["📊 La mia performance", "📈 Analisi Competitiva"])

with tab1:
    # Get AI insights
    insights = get_ai_insights()
    
    # Display simplified AI insights card
    st.markdown(f"""
    <div class="ai-card">
        <h2>💡 Analisi AI</h2>
        <div class="suggestion-card">
            <div class="suggestion-priority priority-alta strength">💪 Punto di Forza</div>
            <p>{insights['main_strength']}</p>
        </div>
        <div class="suggestion-card">
            <div class="suggestion-priority priority-media">⚠️ Punto Debole</div>
            <p>{insights['main_weakness']}</p>
        </div>
        <div class="suggestion-card">
            <div class="suggestion-priority priority-alta summary">📑 Sommario</div>
            <p>{insights['summary']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.header("📊 Indicatori principali")
    
    # Get data for "La Mia Pizzeria"
    my_pizzeria = competitors_df[competitors_df['Nome'] == 'La Mia Pizzeria'].iloc[0]
    numeric_columns = ['Prezzo Margherita', 'Rating', 'Recensioni', 'Menu Items', 
                      'Prezzo Medio Menu', 'Tempo Permanenza Max']
    competitors_avg = competitors_df[competitors_df['Nome'] != 'La Mia Pizzeria'][numeric_columns].mean()

    # 1. KPI Section with comparison

    # Calculate percentile ranks
    price_percentile = (competitors_df['Prezzo Margherita'] > my_pizzeria['Prezzo Margherita']).mean() * 100
    rating_percentile = (competitors_df['Rating'] < my_pizzeria['Rating']).mean() * 100
    menu_percentile = (competitors_df['Menu Items'] < my_pizzeria['Menu Items']).mean() * 100

    # Add section titles with custom styling
    st.markdown("""
        <style>
        .kpi-section-title {
            color: #1E3D59;
            font-size: 1.1rem;
            padding: 0.5rem 0;
            margin-bottom: 0.5rem;
            border-bottom: 2px solid #e6e6e6;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create columns for section titles
    price_section, exp_section = st.columns([1, 2])

    with price_section:
        st.markdown("<div class='kpi-section-title'>💰 Prezzi</div>", unsafe_allow_html=True)
    with exp_section:
        st.markdown("<div class='kpi-section-title'>👥 Esperienza Cliente</div>", unsafe_allow_html=True)

    # Create two rows of metrics
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    # First row - Absolute values and comparisons
    with row1_col1:
        price_diff = my_pizzeria['Prezzo Margherita'] - competitors_avg['Prezzo Margherita']
        st.metric(
            "💰 Prezzo Margherita",
            f"€{my_pizzeria['Prezzo Margherita']:.2f}",
            f"{price_diff:+.2f}€ vs media competitor",
            delta_color="inverse"
        )

    with row1_col2:
        menu_diff = my_pizzeria['Menu Items'] - competitors_avg['Menu Items']
        st.metric(
            "🍕 Varietà Menu",
            f"{int(my_pizzeria['Menu Items'])} pizze",
            f"{int(menu_diff):+d} vs media competitor"
        )

    with row1_col3:
        all_reviews = get_all_reviews()
        overall_rating = all_reviews['Rating'].mean()
        rating_diff = overall_rating - competitors_avg['Rating']  # Keep original diff calculation
        st.metric(
            "⭐ Rating",
            f"{overall_rating:.1f}",
            f"{rating_diff:+.1f} vs media competitor"
        )

    # Second row - Market position metrics
    with row2_col1:
        menu_price_diff = my_pizzeria['Prezzo Medio Menu'] - competitors_avg['Prezzo Medio Menu']
        st.metric(
            "💶 Prezzo Medio Menu",
            f"€{my_pizzeria['Prezzo Medio Menu']:.2f}",
            f"{menu_price_diff:+.2f}€ vs media competitor",
            delta_color="inverse"
        )

    with row2_col2:
        time_diff = my_pizzeria['Tempo Permanenza Max'] - competitors_avg['Tempo Permanenza Max']
        st.metric(
            "⏱️ Permanenza Max",
            f"{int(my_pizzeria['Tempo Permanenza Max'])}h",
            f"{int(time_diff):+d}h vs media competitor",
            delta_color="inverse"
        )

    with row2_col3:
        recent_reviews = get_recent_reviews()
        recent_rating = recent_reviews['Rating'].mean()
        recent_rating_diff = recent_rating - competitors_avg['Rating']  # Keep original diff calculation
        st.metric(
            "✨ Rating ultimi 3 mesi",
            f"{recent_rating:.1f}",
            f"{recent_rating_diff:+.1f} vs media competitor",
            delta_color="normal"
        )

    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
    
    # Add Aspect Ratings Chart
    st.markdown("<div class='kpi-section-title'>📊 Valutazione per Categoria</div>", unsafe_allow_html=True)
    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
    reviews = get_all_reviews()
    aspect_ratings = get_aspect_ratings(reviews)
    
    # Create ECharts bar chart options with improved formatting
    options = {
        "tooltip": {"trigger": "axis"},
        "legend": {
            "data": ["Media Storica", "Ultimi 3 mesi"],
            "orient": "horizontal",  # Change to horizontal orientation
            "left": "center",       # Center the legend
            "top": "top",          # Place at the top
            "textStyle": {
                "fontSize": 16
            },
            "padding": [0, 0, 10, 0]  # Add padding below legend
        },
        "grid": {
            "left": "10%",
            "right": "10%",
            "top": "15%",          # Increase top margin to accommodate legend
            "bottom": "3%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": ["Cibo", "Servizio", "Ambiente"],
            "axisLabel": {
                "interval": 0,
                "fontSize": 16  # Match website font size
            },
            "axisTick": {
                "alignWithLabel": True
            }
        },
        "yAxis": {
            "type": "value",
            "min": 0,
            "max": 5,
            "interval": 1,
            "name": "Rating",
            "nameLocation": "middle",
            "nameGap": 30,
            "nameTextStyle": {
                "fontSize": 16  # Match website font size
            },
            "axisLabel": {
                "fontSize": 16  # Match website font size
            }
        },
        "series": [
            {
                "name": "Media Storica",
                "type": "bar",
                "data": [
                    round(aspect_ratings['all_time']['Cibo'], 1),
                    round(aspect_ratings['all_time']['Servizio'], 1),
                    round(aspect_ratings['all_time']['Ambiente'], 1)
                ],
                "label": {
                    "show": True,
                    "position": "top",
                    "formatter": "{c}",
                    "fontSize": 16  # Match website font size
                },
                "itemStyle": {
                    "color": "#5470c6"
                }
            },
            {
                "name": "Ultimi 3 mesi",
                "type": "bar",
                "data": [
                    round(aspect_ratings['last_3_months']['Cibo'], 1),
                    round(aspect_ratings['last_3_months']['Servizio'], 1),
                    round(aspect_ratings['last_3_months']['Ambiente'], 1)
                ],
                "label": {
                    "show": True,
                    "position": "top",
                    "formatter": "{c}",
                    "fontSize": 16  # Match website font size
                },
                "itemStyle": {
                    "color": "rgba(84, 112, 198, 0.6)"
                },
                "barGap": "10%"  # Decrease spacing between bars in a pair
            }
        ]
    }
    
    # Render the chart
    st_echarts(options=options, height="300px")

    # Add Reviews Section with pagination
    st.header("📝 Ultime Recensioni")
    
    reviews = get_recent_reviews()
    positive_reviews = reviews[reviews['Rating'] >= 3]
    negative_reviews = reviews[reviews['Rating'] < 3]
    items_per_page = 3
    
    # Create columns for section titles
    rev_col1, rev_col2 = st.columns(2)
    
    with rev_col1:
        st.markdown("<div class='kpi-section-title'>✨ Recensioni Positive</div>", unsafe_allow_html=True)
        
        # Calculate pagination for positive reviews
        num_pages_pos = max(1, len(positive_reviews) // items_per_page + (1 if len(positive_reviews) % items_per_page > 0 else 0))
        page_pos = st.number_input('Pagina', min_value=1, max_value=num_pages_pos, value=1, key='pos_page')
        
        start_idx_pos = (page_pos - 1) * items_per_page
        end_idx_pos = min(start_idx_pos + items_per_page, len(positive_reviews))
        
        # Display positive reviews
        for _, review in positive_reviews.iloc[start_idx_pos:end_idx_pos].iterrows():
            st.markdown(f"""
                <div class="review-card">
                    <div class="review-header">
                        <span>{review['Autore']} • {review['Data'].strftime('%d/%m/%Y')} • 
                        <span class="review-source">{review['Fonte']}</span></span>
                        <span class="review-rating">{'⭐' * int(review['Rating'])}</span>
                    </div>
                    <p>{review['Testo']}</p>
                    <div class="aspect-ratings">
                        <span>🍕 Cibo: {review['Cibo']:.1f}</span> •
                        <span>👨‍🍳 Servizio: {review['Servizio']:.1f}</span> •
                        <span>🏠 Ambiente: {review['Ambiente']:.1f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
    with rev_col2:
        st.markdown("<div class='kpi-section-title'>⚠️ Recensioni Negative</div>", unsafe_allow_html=True)
        
        # Calculate pagination for negative reviews
        num_pages_neg = max(1, len(negative_reviews) // items_per_page + (1 if len(negative_reviews) % items_per_page > 0 else 0))
        page_neg = st.number_input('Pagina', min_value=1, max_value=num_pages_neg, value=1, key='neg_page')
        
        start_idx_neg = (page_neg - 1) * items_per_page
        end_idx_neg = min(start_idx_neg + items_per_page, len(negative_reviews))
        
        # Display negative reviews
        for _, review in negative_reviews.iloc[start_idx_neg:end_idx_neg].iterrows():
            st.markdown(f"""
                <div class="review-card negative">
                    <div class="review-header">
                        <span>{review['Autore']} • {review['Data'].strftime('%d/%m/%Y')} • 
                        <span class="review-source">{review['Fonte']}</span></span>
                        <span class="review-rating">{'⭐' * int(review['Rating'])}</span>
                    </div>
                    <p>{review['Testo']}</p>
                    <div class="aspect-ratings">
                        <span>🍕 Cibo: {review['Cibo']:.1f}</span> •
                        <span>👨‍🍳 Servizio: {review['Servizio']:.1f}</span> •
                        <span>🏠 Ambiente: {review['Ambiente']:.1f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
with tab2:
    # Competitors Table
    st.header("🏆 Confronto Competitors")
    styled_df = competitors_df.style.format({
        'Prezzo Margherita': '€{:.2f}',
        'Rating': '{:.1f}'
    })
    st.dataframe(styled_df, use_container_width=True)
    
    # Trend Charts
    st.header("📈 Analisi Temporale")
    col1, col2 = st.columns(2)
    
    with col1:
        # Prepare data for ratings chart
        dates = ratings_history['Data'].unique()
        pizzerias = ratings_history['Pizzeria'].unique()
        
        ratings_options = {
            "title": {"text": "Andamento Rating (ultimi 6 mesi)"},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": list(pizzerias)},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "boundaryGap": False,
                "data": [d.strftime('%Y-%m-%d') for d in dates]
            },
            "yAxis": {
                "type": "value",
                "min": 3.5,
                "max": 5,
                "interval": 0.5
            },
            "series": [
                {
                    "name": pizzeria,
                    "type": "line",
                    "data": ratings_history[ratings_history['Pizzeria'] == pizzeria]['Rating'].tolist()
                } for pizzeria in pizzerias
            ]
        }
        st_echarts(options=ratings_options, height="400px")

    with col2:
        # Prepare data for prices chart
        prices_options = {
            "title": {"text": "Variazione Prezzo Margherita (ultimi 6 mesi)"},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": list(pizzerias)},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "boundaryGap": False,
                "data": [d.strftime('%Y-%m-%d') for d in dates]
            },
            "yAxis": {
                "type": "value",
                "name": "€",
                "min": 7,
                "max": 10,
                "interval": 0.5
            },
            "series": [
                {
                    "name": pizzeria,
                    "type": "line",
                    "data": prices_history[prices_history['Pizzeria'] == pizzeria]['Prezzo'].tolist()
                } for pizzeria in pizzerias
            ]
        }
        st_echarts(options=prices_options, height="400px")


# Footer
st.markdown("""
    <hr style="margin-top: 2rem; margin-bottom: 1rem;">
    <div style="text-align: center; font-size: 0.9rem; color: #999;">
        © 2025 Pizza Radar • Dashboard realizzata con ❤️ da Carpi (Modena)
    </div>
""", unsafe_allow_html=True)

