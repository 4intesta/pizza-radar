import pydeck as pdk
import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from datetime import datetime


def value_to_color(n):
    if n <= 3:
        # Red to Yellow
        t = (n - 1) / (3 - 1)
        r = 255
        g = int(0 + (255 - 0) * t)
        b = 0
    else:
        # Yellow to Green
        t = (n - 3) / (5 - 3)
        r = int(255 - (255 - 0) * t)
        g = 255
        b = 0
    return (r, g, b)

def value_to_size(value, min_val, max_val, min_size=25, max_size=80):
    """Linearly map review counts to circle sizes for visualization."""
    if max_val == min_val:
        return (min_size + max_size) / 2  # avoid division by zero
    return min_size + (value - min_val) / (max_val - min_val) * (max_size - min_size)

def map_generator(my_pizzeria: str, competition_page_data: pd.DataFrame, toggle_on: bool = False) -> pdk.Deck:
    if toggle_on:
        print("Mappa: ultimi 30 giorni")
        ratings = competition_page_data['Average Rating last 30 days']
        reviews = competition_page_data['Number of Reviews last 30 days']

        min_reviews, max_reviews = reviews.min(), reviews.max()

        competition_page_data['color'] = ratings.apply(value_to_color)
        competition_page_data['scaled_size'] = reviews.apply(lambda x: value_to_size(x, min_reviews, max_reviews))

    else:
        print("Mappa: ultimi 7 giorni")
        ratings = competition_page_data['Average Rating last 7 days']
        reviews = competition_page_data['Number of Reviews last 7 days']

        min_reviews, max_reviews = reviews.min(), reviews.max()

        competition_page_data['color'] = ratings.apply(value_to_color)
        competition_page_data['scaled_size'] = reviews.apply(lambda x: value_to_size(x, min_reviews, max_reviews))



    la_mia_pizzeria = competition_page_data[competition_page_data["Name"] == my_pizzeria]
    altre_pizzerie = competition_page_data[competition_page_data["Name"] != my_pizzeria]

    center_latitude = la_mia_pizzeria["Latitude"].iloc[0]
    center_longitude = la_mia_pizzeria["Longitude"].iloc[0]
    
    # Layer for my pizzeria
    my_pizzeria_layer = pdk.Layer(
    "ScatterplotLayer",
    data=la_mia_pizzeria,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius='scaled_size',
    pickable=True,
    auto_highlight=True,
    ) 
    # Layer for my pizzeria
    my_pizzeria_marker = pdk.Layer(
    "ScatterplotLayer",
    data=la_mia_pizzeria,
    get_position='[Longitude, Latitude]',
    get_fill_color='black',
    opacity=0.8,
    get_radius= 20,
    ) 

    # Layer for competitors
    competitors_layer = pdk.Layer(
    "ScatterplotLayer",
    data=altre_pizzerie,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius='scaled_size',
    opacity=0.6,
    pickable=True,
    auto_highlight=True,
    )

    # --- Define the view ---
    view_state = pdk.ViewState(
        latitude=center_latitude,
        longitude=center_longitude,
        zoom=14,
        pitch=0,
    )

    # --- Tooltip ---
    if toggle_on:
        tooltip = {"html": "<b>{Name}</b><br>Recensioni: {Number of Reviews last 30 days}</br>Valutazione media: {Average Rating last 30 days}"}
    else:
        tooltip = {"html": "<b>{Name}</b><br>Recensioni: {Number of Reviews last 7 days}</br>Valutazione media: {Average Rating last 7 days}"}

    map = pdk.Deck(
        layers=[competitors_layer, my_pizzeria_layer, my_pizzeria_marker],
        initial_view_state=view_state,
        map_style=None,
        tooltip=tooltip
    )

    return map

def order_pizzeria_for_table(competition_page_data: pd.DataFrame, toggle_on: bool) -> pd.DataFrame:
    """
    Orders pizzerias by a custom performance score:
        Custom Rating = (Number of Reviews) * (Average Rating - 3)
    """

    if toggle_on:
        print("Tabella: ultimi 30 giorni (monthly view)")
        reviews_col = "Number of Reviews last 30 days"
        ratings_col = "Average Rating last 30 days"
    else:
        print("Tabella: ultimi 7 giorni (weekly view)")
        reviews_col = "Number of Reviews last 7 days"
        ratings_col = "Average Rating last 7 days"

    # Compute custom rating
    competition_page_data = competition_page_data.copy()
    competition_page_data["Custom Rating"] = (
        competition_page_data[reviews_col] * (competition_page_data[ratings_col] - 3)
    )

    # Sort by custom rating (descending) and reset index
    competition_page_data = competition_page_data.sort_values(by="Custom Rating", ascending=False).reset_index(drop=True)

    # Doing this to show 1°, 2°, 3° instead of 0°, 1°, 2°
    competition_page_data.index = competition_page_data.index + 1
    return competition_page_data

def add_rank_change_columns(competition_page_data: pd.DataFrame) -> pd.DataFrame:
    """
    Adds 'rank_change_weekly' and 'rank_change_monthly' columns as arrows with numeric change.
    
    - Negative value → improved → '↑ n'
    - Positive value → dropped → '↓ n'
    - Zero → ''
    """
    df = competition_page_data.copy()
    
    # Ensure 1-based current rank
    current_rank = np.arange(1, len(df)+1)

    # Initialize columns
    df["rank_change_weekly"] = ""
    df["rank_change_monthly"] = ""

    # Iterate by row position
    for pos in range(len(df)):
        row = df.iloc[pos]

        # Monthly change
        diff_monthly = current_rank[pos] - row["Last Year Monthly Rank"][-1]
        if diff_monthly < 0:
            df.at[df.index[pos], "rank_change_monthly"] = f"↑ {abs(diff_monthly)}"
        elif diff_monthly > 0:
            df.at[df.index[pos], "rank_change_monthly"] = f"↓ {diff_monthly}"
        else:
            df.at[df.index[pos], "rank_change_monthly"] = ""

    return df

def computation_of_historical_rankings(competition_page_data: pd.DataFrame):    
    # ----------------------------------------------------
    # Compute monthly custom rating
    # ----------------------------------------------------
    num_months = 12
    competition_page_data["Last Year Monthly Custom Rating"] = [
        [reviews[i] * (ratings[i] - 3) for i in range(num_months)]
        for reviews, ratings in zip(competition_page_data["Last Year Monthly Reviews"], competition_page_data["Last Year Monthly Ratings"])
    ]
    
    # Compute monthly rankings
    monthly_custom_matrix = np.array(competition_page_data["Last Year Monthly Custom Rating"].to_list())  # shape: (num_pizzerias, 12)
    monthly_ranks = np.zeros_like(monthly_custom_matrix, dtype=int)
    
    for month_idx in range(num_months):
        month_scores = monthly_custom_matrix[:, month_idx]
        sorted_indices = np.argsort(-month_scores)
        ranks = np.empty_like(sorted_indices)
        ranks[sorted_indices] = np.arange(1, len(month_scores)+1)
        monthly_ranks[:, month_idx] = ranks

    competition_page_data["Last Year Monthly Rank"] = monthly_ranks.tolist()
    
    return competition_page_data
    
def compute_area_chart_colum(competition_page_data: pd.DataFrame) -> pd.DataFrame:
    """
    For each pizzeria, take the last 28 days of Daily Reviews and Daily Ratings,
    group them into 4 weeks (7 days each), and compute adjusted weekly scores:
    Adjusted Score = Number of Reviews * (Average Rating - 3)

    Adds a new column 'Weekly Adjusted Scores' to the DataFrame as a list of 4 values.
    """
    adjusted_scores_list = []

    for idx, row in competition_page_data.iterrows():
        reviews = np.array(row["Daily Reviews (30d)"][-28:])
        ratings = np.array(row["Daily Ratings (30d)"][-28:])

        # Split into 4 weeks
        reviews_weeks = reviews.reshape(4, 7).sum(axis=1)
        ratings_weeks = ratings.reshape(4, 7).mean(axis=1)

        # Compute adjusted scores
        adjusted_scores = reviews_weeks * (ratings_weeks - 3)

        # Append as a list of 4 elements
        adjusted_scores_list.append(list(np.round(adjusted_scores, 2)))

    # Add as new column to the original DataFrame
    competition_page_data["Custom Score of Last Month - weekly-view"] = adjusted_scores_list
    return competition_page_data

def table_generator(competition_page_data: pd.DataFrame, toggle_on: bool = False):
    competition_page_for_table = order_pizzeria_for_table(competition_page_data, toggle_on)
    competition_page_for_table = add_rank_change_columns(competition_page_for_table)
    competition_page_for_table = compute_area_chart_colum(competition_page_for_table)
    
    if(toggle_on): #show monthly-related data
        gradimento_clienti_help = "Ordine basato sul numero e valutazione di recensioni ricevute negli ultimi 30 giorni"
        average_rating_column_name = "Average Rating last 30 days"
        average_rating_column_help = "Valutazione generale degli ultimi 30 giorni"
        number_of_reviews_name = "Number of Reviews last 30 days"
        number_of_reviews_help = "Numero di recensioni ultimi 30 giorni"
        rank_change_colum_name = "rank_change_monthly"
        rank_change_colum_help = "Variazione classifica gradimento rispetto al mese scorso"

    else: #show weekly-related data
        gradimento_clienti_help = "Ordine basato sul numero e valutazione di recensioni ricevute negli ultimi 7 giorni"
        average_rating_column_name = "Average Rating last 7 days"
        average_rating_column_help = "Valutazione generale degli ultimi 7 giorni"
        number_of_reviews_name = "Number of Reviews last 7 days"
        number_of_reviews_help = "Numero di recensioni ultimi 7 giorni"
        rank_change_colum_name = "rank_change_weekly"
        rank_change_colum_help = "Variazione classifica gradimento rispetto alla settimana scorsa"


    #TODO: prova a mettere None al posto di valutazione recensione = 0 

    columns_to_show = [
        "Name", 
        "Mean Price", 
        average_rating_column_name, 
        number_of_reviews_name,
        "Custom Score of Last Month - weekly-view", 
        #TODO: per adesso nascondo le frecce variazione
        #rank_change_colum_name
    ]

    column_config={
        "_index": st.column_config.NumberColumn(
            "Gradimento",
            #width=100,
            help=gradimento_clienti_help,
        ),
        "Name": st.column_config.TextColumn(
            "Pizzeria",
            width="medium",
            help="Nome della pizzeria"
        ),
        #TODO: risolvi il fatto che la media tenga in considerazione gli zeri
        average_rating_column_name: st.column_config.ProgressColumn(
            "Valutazione ⭐️",
            format="%.1f",
            width="medium",
            min_value=1,
            max_value=5,
            help=average_rating_column_help
        ),
        number_of_reviews_name: st.column_config.NumberColumn(
            "Recensioni",
            width="small",
            help=number_of_reviews_help
        ),
        "Mean Price": st.column_config.NumberColumn(
            "Prezzo medio",
            format="euro",
            width="small",
            help="Prezzo medio delle pizze"
        ),
        "Distance_m_rounded": st.column_config.NumberColumn(
            "Distanza da te",
            #width=100,
            format="%d m",
            help="Distanza stimata dalla tua pizzeria"
        ),
        rank_change_colum_name: st.column_config.TextColumn(
            "Variazione",
            #width="small",
            help=rank_change_colum_help
        ),
        "Custom Score of Last Month - weekly-view": st.column_config.AreaChartColumn(
            "Andamento Percezione",
            color="auto",
            width="medium",
            help="Andamento percezione nell'ultimo mese basato sul numero e valutazione di recensioni ricevute"
        ),
        rank_change_colum_name: st.column_config.TextColumn(
            "Variazione",
            #width="small",
            help=rank_change_colum_help
        ),
    }
    return competition_page_for_table, columns_to_show, column_config

def prepare_data_for_linechart(competition_page_data: pd.DataFrame, name_of_my_pizzeria: str):
    competition_page_for_linechart = pd.DataFrame(
        competition_page_data["Last Year Monthly Custom Rating"].to_list(),
        index=competition_page_data["Name"]
    ).T

    # Replace null values with zeros
    competition_page_for_linechart = competition_page_for_linechart.fillna(0)
    
    months = competition_page_for_linechart.index.tolist()
    pizzeria_names = competition_page_for_linechart.columns.tolist()

    # Multiselect for pizzerias
    selected_pizzerias = st.multiselect(
        "Select Pizzerias:",
        label_visibility="collapsed",
        placeholder="Seleziona pizzerie da confrontare",
        help="Lista di pizzerie da visualizzare nel grafico a linee",
        options=pizzeria_names,
        default=name_of_my_pizzeria
    )
    month_names_abbr = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    month_names_full = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                        "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

    # Shift months so current month is last
    current_month = datetime.now().month - 1
    month_names_abbr_shifted = month_names_abbr[current_month+1:] + month_names_abbr[:current_month+1]
    month_names_full_shifted = month_names_full[current_month+1:] + month_names_full[:current_month+1]

    filtered_df = competition_page_for_linechart[selected_pizzerias].copy()
    filtered_df = filtered_df.fillna(0)
    filtered_df['Month_Num'] = months
    filtered_df['Month_Abbr'] = filtered_df['Month_Num'].map(dict(enumerate(month_names_abbr_shifted)))
    filtered_df['Month_Full'] = filtered_df['Month_Num'].map(dict(enumerate(month_names_full_shifted)))

    chart_data = filtered_df[selected_pizzerias + ['Month_Num', 'Month_Abbr', 'Month_Full']].melt(
        id_vars=['Month_Num', 'Month_Abbr', 'Month_Full'],
        var_name='Pizzeria',
        value_name='Value'
    )

    return chart_data, month_names_abbr_shifted


def linechart_generator(competition_page_data: pd.DataFrame, name_of_my_pizzeria: str):
    chart_data, month_names_abbr_shifted = prepare_data_for_linechart(competition_page_data, name_of_my_pizzeria)

    # Check if chart_data is not empty before resizing
    if not chart_data.empty:
        y_min = chart_data['Value'].min()
        y_max = chart_data['Value'].max()

        if y_max < 0:
            y_max = 10
        if y_min > 0:
            y_min = -10
    else:
        # Default y-axis if no data
        y_min, y_max = -10, 10

    # Define a hover selection
    hover = alt.selection_single(
        nearest=True,
        on='mouseover',
        empty='none',
        clear='mouseout'
    )

    # Base line chart
    line_chart = alt.Chart(chart_data).mark_line(
        interpolate='monotone',
        opacity=0.8
    ).encode(
        x=alt.X(
            'Month_Num:Q',
            axis=alt.Axis(
                grid=False,
                domain=True,
                title="Mesi",
                values=list(range(12)),
                labelExpr=f'datum.value >= 0 ? {month_names_abbr_shifted} [datum.value] : datum.value'
            )
        ),
        y=alt.Y(
            'Value:Q',
            scale=alt.Scale(domain=[y_min, y_max]),  # Set dynamic y-axis range
            axis=alt.Axis(
                grid=True,
                labels=False,
                domain=True,
                title="Percezione pizzeria",
                values=[0]
            )
        ),
        color='Pizzeria',
        tooltip=[
            alt.Tooltip('Pizzeria:N', title='Pizzeria'),
            alt.Tooltip('Month_Full:N', title='Mese'),
            alt.Tooltip('Value:Q', title='Valore')
        ]
    ).properties(height=500)

    # Points visible on hover
    points = alt.Chart(chart_data).mark_point(size=100, filled=True).encode(
        x='Month_Num:Q',
        y='Value:Q',
        color='Pizzeria:N',
        tooltip=[
            alt.Tooltip('Pizzeria:N', title='Pizzeria'),
            alt.Tooltip('Month_Full:N', title='Mese')
        ],
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    ).add_selection(
        hover
    )

    final_chart = line_chart + points

    return final_chart