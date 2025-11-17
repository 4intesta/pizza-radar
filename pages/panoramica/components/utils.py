import pydeck as pdk
import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from datetime import datetime
from database.mock_data import reviews

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
        number_of_reviews_help = "Numero di recensioni degli ultimi 30 giorni"
        rank_change_colum_name = "rank_change_monthly"
        rank_change_colum_help = "Variazione classifica gradimento rispetto al mese scorso"
        hot_topics_name = "hot_topics_last_30d"
        hot_topics_help = "Temi ricorrenti nelle recensioni degli ultimi 30 giorni"

    else: #show weekly-related data
        gradimento_clienti_help = "Ordine basato sul numero e valutazione di recensioni ricevute negli ultimi 7 giorni"
        average_rating_column_name = "Average Rating last 7 days"
        average_rating_column_help = "Valutazione generale degli ultimi 7 giorni"
        number_of_reviews_name = "Number of Reviews last 7 days"
        number_of_reviews_help = "Numero di recensioni degli ultimi 7 giorni"
        rank_change_colum_name = "rank_change_weekly"
        rank_change_colum_help = "Variazione classifica gradimento rispetto alla settimana scorsa"
        hot_topics_name = "hot_topics_last_7d"
        hot_topics_help = "Temi ricorrenti nelle recensioni degli ultimi 7 giorni"

    columns_to_show = [
        "Name", 
        "Mean Price", 
        hot_topics_name,
        average_rating_column_name, 
        number_of_reviews_name,
        #"Custom Score of Last Month - weekly-view", 
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
        hot_topics_name: st.column_config.MultiselectColumn(
            "Temi ricorrenti",
            color="primary",
            width="wide",
            help=hot_topics_help
        ),
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
        "Mean Price": st.column_config.TextColumn(
            "Fascia di prezzo",
            width="small"
        ),
        rank_change_colum_name: st.column_config.TextColumn(
            "Variazione",
            #width="small",
            help=rank_change_colum_help
        )
    }
    return competition_page_for_table, columns_to_show, column_config

# -----------------------------
# Fixed pizzerias & colors
# -----------------------------
ALL_PIZZERIAS = [
    "Pizzeria 1", "Pizzeria 2", "Pizzeria 3", "Pizzeria 4", "Pizzeria 5",
    "Pizzeria 6", "Pizzeria 7", "Pizzeria 8", "Pizzeria 9", "Pizzeria 10",
    "Pizzeria 11", "Pizzeria 12", "Pizzeria 13", "Pizzeria 14", "Pizzeria 15",
    "Pizzeria 16", "Pizzeria 17", "Pizzeria 18", "Pizzeria 19", "Pizzeria 20"
]

FIXED_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
]

COLOR_SCALE = alt.Scale(domain=ALL_PIZZERIAS, range=FIXED_COLORS)

def get_best_and_worst_last_30d_for_linechart(competition_page_data: pd.DataFrame, name_of_my_pizzeria: str):
    competition_page_data = competition_page_data.copy()
    competition_page_data["score"] = (
        competition_page_data["Number of Reviews last 30 days"] *
        (competition_page_data["Average Rating last 30 days"] - 3)
    )

    # Sort descending for best
    sorted_desc = competition_page_data.sort_values("score", ascending=False)
    if sorted_desc.iloc[0]["Name"] == name_of_my_pizzeria and len(sorted_desc) > 1:
        best = sorted_desc.iloc[1]["Name"]
    else:
        best = sorted_desc.iloc[0]["Name"]

    # Sort ascending for worst
    sorted_asc = competition_page_data.sort_values("score", ascending=True)
    if sorted_asc.iloc[0]["Name"] == name_of_my_pizzeria and len(sorted_asc) > 1:
        worst = sorted_asc.iloc[1]["Name"]
    else:
        worst = sorted_asc.iloc[0]["Name"]

    return best, worst

# -----------------------------
# Prepare data function
# -----------------------------
def prepare_data_for_linechart(competition_page_data: pd.DataFrame, name_of_my_pizzeria: str, best: str, worst: str):
    # Base ratings matrix
    competition_page_for_linechart = pd.DataFrame(
        competition_page_data["Last Year Monthly Custom Rating"].to_list(),
        index=competition_page_data["Name"]
    ).T.fillna(0)

    months = competition_page_for_linechart.index.tolist()
    pizzeria_names = competition_page_for_linechart.columns.tolist()

    # Streamlit multiselect
    selected_pizzerias = st.multiselect(
        "Select Pizzerias:",
        label_visibility="collapsed",
        placeholder="Seleziona pizzerie da confrontare",
        help="Lista di pizzerie da visualizzare nel grafico a linee",
        options=pizzeria_names,
        max_selections=10,
        default=[name_of_my_pizzeria, best, worst]
    )

    filtered_df = competition_page_for_linechart[selected_pizzerias].copy().fillna(0)

    # Month names
    month_names_abbr = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    month_names_full = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                        "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

    # Shift months by current month
    current_month = datetime.now().month - 1
    month_names_abbr_shifted = month_names_abbr[current_month+1:] + month_names_abbr[:current_month+1]
    month_names_full_shifted = month_names_full[current_month+1:] + month_names_full[:current_month+1]

    filtered_df['Month_Num'] = months
    filtered_df['Month_Abbr'] = filtered_df['Month_Num'].map(dict(enumerate(month_names_abbr_shifted)))
    filtered_df['Month_Full'] = filtered_df['Month_Num'].map(dict(enumerate(month_names_full_shifted)))

    # -----------------------------
    # Extract tags
    # -----------------------------
    tag_columns = sorted([col for col in competition_page_data.columns if col.startswith("Tags ")])
    tags_matrix = {
        p: competition_page_data.loc[competition_page_data["Name"] == p, tag_columns].values[0].tolist()
        for p in selected_pizzerias
    }

    chart_data = filtered_df[selected_pizzerias + ['Month_Num', 'Month_Abbr', 'Month_Full']].melt(
        id_vars=['Month_Num', 'Month_Abbr', 'Month_Full'],
        var_name='Pizzeria',
        value_name='Value'
    )

    tags_list = []
    for _, row in chart_data.iterrows():
        p = row["Pizzeria"]
        m = int(row["Month_Num"])
        tags_list.append(tags_matrix[p][m])  # 3 tags per month

    chart_data["Tags"] = tags_list

    return chart_data, month_names_abbr_shifted

# -----------------------------
# Line chart generator
# -----------------------------
def linechart_generator(competition_page_data: pd.DataFrame, name_of_my_pizzeria: str, toggle_on: bool = False):
    best, worst = get_best_and_worst_last_30d_for_linechart(competition_page_data, name_of_my_pizzeria)

    chart_data, month_names_abbr_shifted = prepare_data_for_linechart(competition_page_data, name_of_my_pizzeria, best, worst)

    chart_height = 450

    # Y-axis bounds
    if not chart_data.empty:
        y_min = chart_data['Value'].min()
        y_max = chart_data['Value'].max()
        if y_max < 0: y_max = 10
        if y_min > 0: y_min = -10
    else:
        y_min, y_max = -10, 10

    hover = alt.selection_single(nearest=True, on='mouseover', empty='none', clear='mouseout')

    chart_data["Tags_Str"] = chart_data["Tags"].apply(lambda x: " - ".join(x))

    # Suppose selected_pizzerias comes from your multiselect
    selected_pizzerias = chart_data['Pizzeria'].unique().tolist()

    # Main line chart
    line_chart = alt.Chart(chart_data).mark_line(interpolate='monotone', opacity=0.8).encode(
        x=alt.X(
            'Month_Num:Q',
            axis=alt.Axis(
                grid=False,
                domain=True,
                title=None,
                labelFontSize=16,
                values=list(range(12)),
                labelExpr=f'datum.value >= 0 ? {month_names_abbr_shifted} [datum.value] : datum.value'
            )
        ),
        y=alt.Y(
            'Value:Q',
            scale=alt.Scale(domain=[y_min, y_max]),
            axis=alt.Axis(grid=True, labels=False, domain=True, title="Gradimento percepito ", titleFontSize=16, values=[0])
        ),
        color=alt.Color(
            'Pizzeria:N',
            scale=COLOR_SCALE,
            legend=alt.Legend(values=selected_pizzerias)
        ),
        tooltip=[
            alt.Tooltip('Pizzeria:N', title='Pizzeria'),
            alt.Tooltip('Month_Full:N', title='Mese'),
            alt.Tooltip('Value:Q', title='Valore'),
            alt.Tooltip('Tags_Str:N', title='Tags del mese')
        ]
    ).properties(height=chart_height)


    # Hover points
    points = alt.Chart(chart_data).mark_point(size=100, filled=True).encode(
        x='Month_Num:Q',
        y='Value:Q',
        color=alt.Color(
            'Pizzeria:N',
            scale=COLOR_SCALE,
            legend=alt.Legend(values=selected_pizzerias)
        ),
        opacity=alt.condition(hover, alt.value(1), alt.value(0)),
        tooltip=[
            alt.Tooltip('Pizzeria:N', title='Pizzeria'),
            alt.Tooltip('Month_Full:N', title='Mese'),
            alt.Tooltip('Tags_Str:N', title='Aspetti ricorrenti')
        ]
    ).add_selection(hover).properties(height=chart_height)

    return line_chart + points

# -----------------------------
# Tab generator
# -----------------------------
def render_review_tab(pizzeria, avg_eviews_rating_last_7_days, avg_reviews_number_7_days):
    rating_generale_value = round(pizzeria["Average Rating last 7 days"].iloc[0],2)
    rating_generale_diff = round(rating_generale_value - avg_eviews_rating_last_7_days, 1)

    reviews_number_value = round(pizzeria["Number of Reviews last 7 days"].iloc[0],2)
    reviews_number_diff = round(reviews_number_value - avg_reviews_number_7_days, 0)

    #st.write(pizzeria)
    st.subheader(pizzeria["Name"].iloc[0])

    col1, col2 = st.columns([1.35, 4.1])
    with col1:
        st.metric(
            "Rating Generale", 
            rating_generale_value, 
            f"{rating_generale_diff} rispetto a pizzerie in zona",
            help="Valutazione generale delle recesioni degli ultimi 7 giorni.", 
            border=True
        )
    
        st.metric(
            "Numero Recensioni Ricevute", 
            reviews_number_value,
            f"{reviews_number_diff:.0f} rispetto a pizzerie in zona",
            chart_data=pizzeria['Daily Reviews (30d)'].iloc[0][-7:], 
            chart_type="area",
            delta_color="off",
            help="Numero di recesioni degli ultimi 7 giorni.  \n Il grafico mostra come sono distribuite", 
            border=True
        )
    
    with col2:
        st.write("Recensioni recenti:")
        with st.container(height=322, border=False):
            for comment in reviews:
                label=comment["author"]+" ("+str(comment["date"])+") "+(comment["rating"]*":material/star:")+" - "+comment["platform"]
                with st.expander(label=label):
                    
                    #TESTO
                    text = comment.get("text") 
                    if text:
                        st.markdown(comment["text"])
                    
                    #TAGS
                    missing_comment_warning = ""
                    if comment["ownerResponse"] is False:
                        missing_comment_warning = ":yellow-badge[:material/warning: Recensione senza tua risposta]"

                    #SUBRATING
                    subratings_string = ""
                    subratings = comment.get("subratings", {})
                    for label, value in subratings.items():
                        if label=="cibo":
                            subratings_string = subratings_string +" "+f":grey-badge[:material/local_pizza: {label.capitalize()}"+f": {value}]"
                        elif label=="qualità-prezzo":
                            subratings_string = subratings_string +" "+f":grey-badge[:material/money_bag: {label.capitalize()}"+f": {value}]"
                        elif label=="servizio":
                            subratings_string = subratings_string +" "+f":grey-badge[:material/hand_meal: {label.capitalize()}"+f": {value}]"
                        elif label=="ambiente":
                            subratings_string = subratings_string +" "+f":grey-badge[:material/candle: {label.capitalize()}"+f": {value}]"
                    
                    #TAGS
                    tags_string = ""
                    tags = comment.get("tags", [])
                    for label in tags:
                        tags_string = tags_string +" "+f":grey-badge[{label.capitalize()}]"

                    if text is None and subratings_string == "" and tags_string == "":
                        st.markdown("Questo commento è privo di contenuto")
                        if missing_comment_warning != "":
                            st.markdown(missing_comment_warning)

                    else:
                        st.markdown((missing_comment_warning+" "+subratings_string+" "+tags_string).strip())
                    
def get_best_last_7d(competition_page_data: pd.DataFrame):
    competition_page_data["score"] = (
        competition_page_data["Number of Reviews last 7 days"] * 
        (competition_page_data["Average Rating last 7 days"] - 3)
    )
    best_row = competition_page_data.loc[competition_page_data["score"].idxmax()]
    return best_row["Name"]

def get_worst_last_7d(competition_page_data: pd.DataFrame):
    competition_page_data["score"] = (
        competition_page_data["Number of Reviews last 7 days"] * 
        (competition_page_data["Average Rating last 7 days"] - 3)
    )
    worst_row = competition_page_data.loc[competition_page_data["score"].idxmin()]
    return worst_row["Name"]