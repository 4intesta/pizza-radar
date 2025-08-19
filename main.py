import config  # Must be the very first import
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
from data_mock import (get_all_reviews, get_mock_competitors, get_historical_data, 
                      get_recent_rating, get_recent_reviews, get_aspect_ratings, 
                      get_ai_insights, get_opening_hours)  # Add this import
import plotly.express as px
import numpy as np

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
    
    # AI Insights section
    with st.expander("💡 Analisi AI", expanded=True):
        st.markdown(f"""
        <div class="ai-card">
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
    numeric_columns = ['Prezzo Margherita', 'avgRating', 'avgRatingCibo', 'avgRatingServizio', 
                      'avgRatingAtmosfera', 'Recensioni', 'Menu Items', 
                      'Prezzo Medio Menu', 'Tempo Attesa Max']
    competitors_avg = competitors_df[competitors_df['Nome'] != 'La Mia Pizzeria'][numeric_columns].mean()

    # 1. KPI Section with comparison

    # Calculate percentile ranks
    price_percentile = (competitors_df['Prezzo Margherita'] > my_pizzeria['Prezzo Margherita']).mean() * 100
    rating_percentile = (competitors_df['avgRating'] < my_pizzeria['avgRating']).mean() * 100
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
            "🌼 Prezzo Margherita",
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
        rating_diff = overall_rating - competitors_avg['avgRating']  # Keep original diff calculation
        st.metric(
            "⭐ Valutazione",
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
        time_diff = my_pizzeria['Tempo Attesa Max'] - competitors_avg['Tempo Attesa Max']
        st.metric(
            "⏱️ Tempo Attesa Max",
            f"{int(my_pizzeria['Tempo Attesa Max'])} min",
            f"{int(time_diff):+d} min vs media competitor",
            delta_color="inverse"
        )

    with row2_col3:
        recent_reviews = get_recent_reviews()
        recent_rating = recent_reviews['Rating'].mean()
        recent_rating_diff = recent_rating - competitors_avg['avgRating']  # Keep original diff calculation
        st.metric(
            "✨ Valutazione ultimi 3 mesi",
            f"{recent_rating:.1f}",
            f"{recent_rating_diff:+.1f} vs media competitor",
            delta_color="normal"
        )

    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
    
    # Add Aspect Ratings Chart
        # Add Ratings Trend Chart
    st.markdown("<div class='kpi-section-title'>📈 Trend Valutazioni</div>", unsafe_allow_html=True)
    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

    # Get reviews and calculate moving averages
    reviews = get_all_reviews()
    reviews['Data'] = pd.to_datetime(reviews['Data'])
    
    # Filter for last year only
    one_year_ago = pd.Timestamp.now() - pd.DateOffset(years=1)
    reviews = reviews[reviews['Data'] >= one_year_ago]
    
    # Resample to weekly data points and calculate 1-month moving average
    window = '30D'  # 1 month window
    moving_avgs = pd.DataFrame()
    for col in ['Rating', 'Cibo', 'Servizio', 'Ambiente']:
        # First resample to weekly averages
        weekly_data = reviews.groupby('Data')[col].mean().resample('W').mean()
        # Then calculate 1-month moving average
        moving_avgs[col] = weekly_data.rolling(window, min_periods=1).mean()

    # Calculate minimum value from the data and round down to nearest integer
    min_rating = np.floor(min(moving_avgs['Rating'].min(),
                            moving_avgs['Cibo'].min(),
                            moving_avgs['Servizio'].min(),
                            moving_avgs['Ambiente'].min()))

    # Create line chart options with same configuration but updated data
    options = {
        "tooltip": {
            "trigger": "axis",
            "formatter": "{b}<br/>{a}: {c}"
        },
        "legend": {
            "data": ["Rating Generale", "Cibo", "Servizio", "Ambiente"],
            "orient": "horizontal",
            "left": "center",
            "top": "top",
            "textStyle": {"fontSize": 16}
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "top": "15%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [d.strftime('%m/%Y') for d in moving_avgs.index],  # Changed date format
            "axisLabel": {
                "fontSize": 14,
                "rotate": 45,
                "interval": 4  # Adjusted to show fewer labels for better readability
            }
        },
        "yAxis": {
            "type": "value",
            "name": "valutazione",
            "min": min_rating,
            "max": 5,
            "interval": 0.5,
            "axisLabel": {"fontSize": 14}
        },
        "series": [
            {
                "name": "Rating Generale",
                "type": "line",
                "data": moving_avgs['Rating'].round(2).tolist(),
                "smooth": True,
                "symbol": "circle",  # Show data points
                "symbolSize": 6,     # Size of data points
                "lineStyle": {"width": 2},
                "itemStyle": {"color": "#5470c6"}
            },
            {
                "name": "Cibo",
                "type": "line",
                "data": moving_avgs['Cibo'].round(2).tolist(),
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 6,
                "lineStyle": {"width": 2},
                "itemStyle": {"color": "#91cc75"}
            },
            {
                "name": "Servizio",
                "type": "line",
                "data": moving_avgs['Servizio'].round(2).tolist(),
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 6,
                "lineStyle": {"width": 2},
                "itemStyle": {"color": "#fac858"}
            },
            {
                "name": "Ambiente",
                "type": "line",
                "data": moving_avgs['Ambiente'].round(2).tolist(),
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 6,
                "lineStyle": {"width": 2},
                "itemStyle": {"color": "#ee6666"}
            }
        ]
    }

    # Render the chart
    st_echarts(options=options, height="400px")

    # Add Reviews Section
    st.header("📝 Ultime Recensioni")
    
    # Get recent reviews and sort by date
    reviews = get_recent_reviews()
    positive_reviews = reviews[reviews['Rating'] >= 3].sort_values('Data', ascending=False).head(3)
    negative_reviews = reviews[reviews['Rating'] < 3].sort_values('Data', ascending=False).head(3)
    
    # Create columns for section titles
    rev_col1, rev_col2 = st.columns(2)
    
    with rev_col1:
        st.markdown("<div class='kpi-section-title'>✨ Recensioni Positive</div>", unsafe_allow_html=True)
        
        # Display latest 3 positive reviews
        for _, review in positive_reviews.iterrows():
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
        
        # Display latest 3 negative reviews
        for _, review in negative_reviews.iterrows():
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
    # Get AI insights
    insights = get_ai_insights()
    
    # AI Insights section
    with st.expander("💡 Analisi AI", expanded=True):
        st.markdown(f"""
        <div class="ai-card">
            <div class="suggestion-card">
                <div class="suggestion-priority priority-alta strength">💪 Punto di Forza</div>
                <p>{insights['main_strength']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Competitors Table
    st.header("🏆 Confronto Competitors")
    
    # Create a copy and select only the columns we want to display
    display_columns = ['Nome', 'avgRating', 'avgRatingCibo', 'avgRatingServizio', 'avgRatingAtmosfera', 
                       'Menu Items', 'Prezzo Margherita', 'Prezzo Medio Menu']
    display_df = competitors_df[display_columns].copy()
    
    # Rename columns with numbers
    renamed_df = display_df.copy()
    renamed_df.columns = [str(i+1) for i in range(len(display_df.columns))]
    
    # Function to highlight the best value
    def highlight_best(s, is_inverse=False):
        if is_inverse:
            is_best = s == s.min()
        else:
            is_best = s == s.max()
        return ['background-color: #FBF719; font-weight: bold' if v else '' for v in is_best]

    # Apply styling to the display dataframe
    styled_df = display_df.copy()
    styled_df = styled_df.style\
        .apply(highlight_best, subset=['avgRating', 'avgRatingCibo', 'avgRatingServizio', 'avgRatingAtmosfera', 'Menu Items'])\
        .format({
            'Prezzo Margherita': '€{:.2f}',
            'Prezzo Medio Menu': '€{:.2f}',
            'avgRating': '{:.1f}',
            'avgRatingCibo': '{:.1f}',
            'avgRatingServizio': '{:.1f}',
            'avgRatingAtmosfera': '{:.1f}',
        })

    # Display the styled dataframe
    st.dataframe(
        styled_df,
        height=300,
        column_config={
            "Nome": st.column_config.Column("Nome"),
            "avgRating": st.column_config.NumberColumn("Generale ⭐️", format="%.1f"),
            "avgRatingCibo": st.column_config.NumberColumn("Cibo 🍕", format="%.1f"),
            "avgRatingServizio": st.column_config.NumberColumn("Servizio 👨‍🍳", format="%.1f"),
            "avgRatingAtmosfera": st.column_config.NumberColumn("Ambiente 🏠", format="%.1f"),
            "Menu Items": st.column_config.NumberColumn("Pizze nel Menu"),
            "Prezzo Margherita": st.column_config.NumberColumn("Prezzo Margherita", format="€%.2f"),
            "Prezzo Medio Menu": st.column_config.NumberColumn("Prezzo Medio Pizza", format="€%.2f"),
        },
        use_container_width=True
    )

        # Add map visualization
    st.markdown("<div class='kpi-section-title'>📍 Mappa</div>", unsafe_allow_html=True)
    
    # Create map figure with improved hover and size legend
    fig = px.scatter_mapbox(competitors_df,
                           lat='lat',
                           lon='lon',
                           hover_name='Nome',
                           hover_data={
                               'avgRating': ':.1f',
                               'avgRatingCibo': ':.1f',
                               'avgRatingServizio': ':.1f',
                               'avgRatingAtmosfera': ':.1f',
                               'Prezzo Margherita': ':.2f€',
                               'Recensioni': True,
                               'lat': False,
                               'lon': False
                           },
                           color='avgRating',
                           size='Recensioni',
                           size_max=25,
                           zoom=14,
                           color_continuous_scale='RdYlGn',
                           labels={
                               'avgRating': 'Rating Generale',
                               'avgRatingCibo': 'Rating Cibo',
                               'avgRatingServizio': 'Rating Servizio',
                               'avgRatingAtmosfera': 'Rating Ambiente',
                               'Prezzo Margherita': 'Prezzo Margherita',
                               'Recensioni': 'Numero Recensioni'
                           })

    # Update layout with improved styling
    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox=dict(
            center=dict(
                lat=competitors_df['lat'].mean(),
                lon=competitors_df['lon'].mean()
            )
        ),
        margin=dict(r=0, t=0, l=0, b=0),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Helvetica"
        ),
        coloraxis_colorbar=dict(
            title="Rating",
            tickformat=".1f",
            len=0.5,
            yanchor="top",
            y=1,
            xanchor="left",
            x=0
        )
    )

    # Update traces for better hover template
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "Rating Generale: %{customdata[0]:.1f}⭐<br>" +
                      "Rating Cibo: %{customdata[1]:.1f}🍕<br>" +
                      "Rating Servizio: %{customdata[2]:.1f}👨‍🍳<br>" +
                      "Rating Ambiente: %{customdata[3]:.1f}🏠<br>" +
                      "Prezzo Margherita: %{customdata[4]}<br>" +
                      "Recensioni: %{customdata[5]}<extra></extra>"
    )

    # Display the map
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='kpi-section-title'>⏰ Orari settimanali</div>", unsafe_allow_html=True)
    
    # Get opening hours
    opening_hours = get_opening_hours()
    
    # Add CSS for the calendar
    st.markdown("""
        <style>
        .calendar-grid {
            display: grid;
            grid-template-columns: auto repeat(7, 1fr);
            gap: 1px;
            background-color: #f0f2f6;
            padding: 1px;
            border-radius: 8px;
            margin-top: 1rem;
        }
        .calendar-header, .calendar-cell {
            background: white;
            padding: 8px;
            text-align: center;
            font-size: 14px;
        }
        .calendar-header {
            background: #f8f9fa;
            font-weight: bold;
        }
        .calendar-closed {
            color: #dc3545;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create calendar headers
    days = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
    
    # Build calendar HTML
    calendar_html = '<div class="calendar-grid">'
    calendar_html += '<div class="calendar-header">Pizzeria</div>'
    
    # Add day headers
    for day in days:
        calendar_html += f'<div class="calendar-header">{day}</div>'
    
    # Add rows for each pizzeria
    for pizzeria in opening_hours.keys():
        calendar_html += f'<div class="calendar-cell">{pizzeria}</div>'
        for day in days:
            hours = opening_hours[pizzeria][day]
            cell_class = 'calendar-cell calendar-closed' if hours == 'Chiuso' else 'calendar-cell'
            calendar_html += f'<div class="{cell_class}">{hours}</div>'
    
    calendar_html += '</div>'
    
    # Display the calendar
    st.markdown(calendar_html, unsafe_allow_html=True)
    
    # Add spacing after calendar
    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

    st.header("📈 Analisi Temporale")
    # Prepare data for ratings chart
    dates = ratings_history['Data'].unique()
    pizzerias = competitors_df['Nome'].unique()
    
    # First chart - Ratings
    st.markdown("<div class='kpi-section-title'>📈 Trend Valutazioni</div>", unsafe_allow_html=True)
    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
    
    # Calculate min rating from data
    min_rating = np.floor(ratings_history['Rating'].min())
    
    ratings_options = {
        "tooltip": {
            "trigger": "axis",
            "formatter": "{b}<br/>{a}: {c}"
        },
        "legend": {
            "data": list(pizzerias),
            "type": "scroll",  # Make legend scrollable
            "orient": "horizontal",
            "left": "center",
            "top": "top",
            "textStyle": {"fontSize": 14},
            "pageButtonPosition": "end"
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "top": "15%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [d.strftime('%m/%Y') for d in ratings_history['Data'].unique()],
            "axisLabel": {
                "fontSize": 14,
                "rotate": 45,
                "interval": 0  # Changed to 0 to show all months
            }
        },
        "yAxis": {
            "type": "value",
            "name": "valutazione",
            "min": min_rating,
            "max": 5,
            "interval": 0.5,
            "axisLabel": {"fontSize": 14}
        },
        "series": [
            {
                "name": pizzeria,
                "type": "line",
                "data": ratings_history[ratings_history['Pizzeria'] == pizzeria]['Rating'].tolist(),
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 6,
                "lineStyle": {"width": 2}
            } for pizzeria in pizzerias
        ]
    }
    st_echarts(options=ratings_options, height="400px")

    # Add spacing between charts
    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

    # Second chart - Prices
    st.markdown("<div class='kpi-section-title'>💰 Trend Prezzi</div>", unsafe_allow_html=True)
    st.empty().markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
    
    # Calculate min and max prices from data
    min_price = np.floor(prices_history['Prezzo'].min())
    max_price = np.ceil(prices_history['Prezzo'].max())
    
    prices_options = {
        "tooltip": {
            "trigger": "axis",
            "formatter": "{b}<br/>{a}: €{c}"
        },
        "legend": {
            "data": list(pizzerias),
            "type": "scroll",  # Make legend scrollable
            "orient": "horizontal",
            "left": "center",
            "top": "top",
            "textStyle": {"fontSize": 14},
            "pageButtonPosition": "end"
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "top": "15%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [d.strftime('%m/%Y') for d in dates],
            "axisLabel": {
                "fontSize": 14,
                "rotate": 45,
                "interval": 0  # Changed to 0 to show all months
            }
        },
        "yAxis": {
            "type": "value",
            "name": "€",
            "min": min_price,
            "max": max_price,
            "interval": 0.5,
            "axisLabel": {"fontSize": 14}
        },
        "series": [
            {
                "name": pizzeria,
                "type": "line",
                "data": prices_history[prices_history['Pizzeria'] == pizzeria]['Prezzo'].tolist(),
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 6,
                "lineStyle": {"width": 2}
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

