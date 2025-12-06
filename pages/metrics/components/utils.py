import streamlit as st
import altair as alt
import pandas as pd
import numpy as np


def pizza_price_selector(my_data, competitor_data):
    with st.container(border=True):

        chart_type = st.selectbox(
            "Seleziona tipologia Comparison",
            ["Prezzo Margherita", "Prezzo Diavola", "Prezzo Quattro Stagioni", "Prezzo Pizza in media"],
            label_visibility="collapsed",
            accept_new_options=False
        )

        if chart_type == "Prezzo Margherita":
            price_diff = competitor_data['Prices']['margherita'] - my_data['Prices']['margherita']
            st.metric(
                "Prezzo Margherita",f"{competitor_data['Prices']['margherita']:.1f} €", f"{price_diff:.2f} € rispetto a te", delta_color="off", border=False)
        elif chart_type == "Prezzo Diavola":
            price_diff = competitor_data['Prices']['diavola'] - my_data['Prices']['diavola']
            st.metric(
                chart_type,f"{competitor_data['Prices']['margherita']:.1f} €", f"{price_diff:.2f} € rispetto a te", delta_color="off", border=False)
        if chart_type == "Prezzo Quattro Stagioni":
            price_diff = competitor_data['Prices']['quattro stagioni'] - my_data['Prices']['quattro stagioni']
            st.metric(
                chart_type,f"{competitor_data['Prices']['margherita']:.1f} €", f"{price_diff:.2f} € rispetto a te", delta_color="off", border=False)
        elif chart_type == "Prezzo Pizza in media":
            price_diff = competitor_data['Prices']['AVG_PRICE'] - my_data['Prices']['AVG_PRICE']
            st.metric(
                chart_type, f"{competitor_data['Prices']['AVG_PRICE']:.1f} €", f"{price_diff:.2f} € rispetto a te", delta_color="off", border=False)
            
def menu_items(my_data, competitor_data):
    menu_diff = competitor_data['Number of Menu Items'] - my_data['Number of Menu Items']
    st.metric(f"Nel Menu", f"{competitor_data['Number of Menu Items']} pizze", f"{menu_diff} rispetto a te", delta_color="off", border=True)

def computation_of_historical_gradimento(competition_page_data: pd.DataFrame):
    competition_page_data["Last Year Monthly Custom Rating"] = competition_page_data.apply(
        lambda row: [
            r * (rating - 3)
            for r, rating in zip(row["Last Year Monthly Reviews"], row["Last Year Monthly Ratings"])
        ],
        axis=1
    )
    return competition_page_data

def gradimento_linechart(my_data, competitor_data):
    height=190 

    # Italian month abbreviations
    months_it = ['Dic', 'Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov']

    # Ratings
    my_ratings = my_data['Last Year Monthly Custom Rating']
    comp_ratings = competitor_data['Last Year Monthly Custom Rating']

    # Create dataframes
    df_my = pd.DataFrame({
        'Month': months_it,
        'Rating': my_ratings,
        'Pizzeria': my_data['Name']
    })

    df_comp = pd.DataFrame({
        'Month': months_it,
        'Rating': comp_ratings,
        'Pizzeria': competitor_data['Name']
    })

    # Combine both dataframes
    df_all = pd.concat([df_my, df_comp], ignore_index=True)
    
    # Add a numeric month column to preserve order
    df_all['Month_Num'] = df_all['Month'].apply(lambda m: months_it.index(m))

    # Hover selection
    hover = alt.selection_single(nearest=True, on='mouseover', empty='none', clear='mouseout')

    # Main line chart
    line_chart = alt.Chart(df_all).mark_line(interpolate='monotone', opacity=0.8).encode(
        x=alt.X('Month_Num:Q',
                axis=alt.Axis(
                    title=None,
                    labels=True,
                    grid=False,
                    tickSize=0,
                    values=list(range(12)),
                    labelExpr=f'{months_it}[datum.value]'
                )
        ),
        y=alt.Y('Rating:Q',
                title='Gradimento Percepito',
                axis=alt.Axis(labels=False, grid=False)
        ),
        color='Pizzeria:N',
        tooltip=[
            alt.Tooltip('Pizzeria:N', title='Pizzeria'),
            alt.Tooltip('Month:N', title='Mese')
        ]
    ).properties(
        height=height
    )

    # Points on hover
    points = alt.Chart(df_all).mark_point(size=100, filled=True).encode(
        x='Month_Num:Q',
        y='Rating:Q',
        color='Pizzeria:N',
        tooltip=[
            alt.Tooltip('Pizzeria:N', title='Pizzeria'),
            alt.Tooltip('Month:N', title='Mese')
        ],
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    ).add_selection(hover).properties(
        height=height
    )

    st.altair_chart(line_chart + points, use_container_width=True)

def gradimento(my_data, competitor_data):

    # ---- TOP METRICS ----
    with st.container(border=True):
        col_rating, col_review = st.columns(2)

        with col_rating:
            st.metric(
                "Valutazione Generale",
                f"{competitor_data['Rating']['GENERALE']:.2f}",
                f"{competitor_data['Rating']['GENERALE'] - my_data['Rating']['GENERALE']:.1f} rispetto a te",
                delta_color="inverse"
            )

        with col_review:
            total_reviews_competitor = sum(competitor_data['Last Year Monthly Reviews'])
            total_reviews_my_data = sum(my_data['Last Year Monthly Reviews'])
            st.metric(
                "Recensioni ultimi 30 giorni",
                total_reviews_competitor,
                f"{total_reviews_competitor - total_reviews_my_data} rispetto a te",
                delta_color="off"
            )
        
        gradimento_linechart(my_data, competitor_data)

def create_comparison_chart(competitor_data, my_data, category):
    height=193

    # Extract series
    comp_series = competitor_data['Monthly Category Ratings'][category.upper()]
    my_series   = my_data['Monthly Category Ratings'][category.upper()]

    df_comp = pd.DataFrame({
        "date": pd.to_datetime(list(comp_series.keys())),
        "value": list(comp_series.values()),
        "source": competitor_data["Name"]
    })

    df_my = pd.DataFrame({
        "date": pd.to_datetime(list(my_series.keys())),
        "value": list(my_series.values()),
        "source": my_data["Name"]
    })

    # Combine
    df = pd.concat([df_comp, df_my], ignore_index=True)

    # Add month label
    months_it = {1: "Gen", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mag", 6: "Giu",
                 7: "Lug", 8: "Ago", 9: "Set", 10: "Ott", 11: "Nov", 12: "Dic"}
    df['month_label'] = df['date'].dt.month.map(months_it)

    # Add numeric month for hover selection order
    df['month_num'] = df['date'].dt.month

    # Hover selection
    hover = alt.selection_single(
        nearest=True, on='mouseover', empty='none', clear='mouseout'
    )

    # Main line chart
    line_chart = (
        alt.Chart(df)
        .mark_line(interpolate='monotone', opacity=0.8)
        .encode(
            x=alt.X(
                "month_label:N",
                title=None,
                sort=None,
                axis=alt.Axis(labelAngle=0)  # horizontal labels
            ),
            y=alt.Y(
                "value:Q",
                title=f"{category.capitalize()}",
                scale=alt.Scale(domain=[1, 5]),  
                axis=alt.Axis(
                    grid=True,
                    tickMinStep=1 
                )
            ),
            color=alt.Color("source:N", title="Source"),
            tooltip=[
                alt.Tooltip("source:N", title="Pizza"),
                alt.Tooltip("value:Q", title="Valore"),
                alt.Tooltip("month_label:N", title="Mese")
            ]
        ).properties(
            height=height
        )
    )

    # Points on hover
    points = (
        alt.Chart(df)
        .mark_point(size=100, filled=True)
        .encode(
            x=alt.X("month_label:N", title="Month", sort=None),
            y="value:Q",
            color="source:N",
            tooltip=[
                alt.Tooltip("source:N", title="Pizza"),
                alt.Tooltip("value:Q", title="Valore"),
                alt.Tooltip("month_label:N", title="Mese")
            ],
            opacity=alt.condition(hover, alt.value(1), alt.value(0))
        )
        .add_selection(hover).properties(
            height=height
        )
    )

    st.altair_chart(line_chart + points, use_container_width=True)

def render_comparison_tab(name_of_my_pizzeria, competition_page_data, selected_pizzeria, label):

    """Helper function to render comparison tab layout"""
    col1, col2 = st.columns([1.35, 4.1])

    # Get data for both pizzerias
    competitor_data = competition_page_data.loc[competition_page_data['Name'] == selected_pizzeria].iloc[0]
    my_data = competition_page_data.loc[competition_page_data['Name']==name_of_my_pizzeria].iloc[0]
    
    # Calculate rating differences
    competitor_rating = competitor_data["Rating"][label.upper()]
    rating_diff = competitor_rating - my_data["Rating"][label.upper()]

    with col1:    
        with st.container(border=True):
            st.metric(f"Valutazione {label}", f"{competitor_rating}", f"{rating_diff:.2f} rispetto a te", delta_color="inverse")

            # Align indices (months)
            df_compare = pd.DataFrame({
                "Competitor": competitor_data["Monthly Category Ratings"][label.upper()],
                "Me": my_data["Monthly Category Ratings"][label.upper()]
            })

            # Count months where "Me" > "Competitor"
            better_count = (df_compare["Me"] > df_compare["Competitor"]).sum()
            total_months = len(df_compare)
            percentage_better = (better_count / total_months) * 100

            st.metric("Nell'anno per quanto hai performato meglio", f"{percentage_better:.0f}%")

    with col2:
        with st.container(border=True):
            create_comparison_chart(competitor_data, my_data, label)
            
def render_platform(my_data, competitor_data):
    with st.container(height=339, border=True): 

        st.metric("Presenza su piattaforme","")
        competitor_platforms = competitor_data['Platforms']

        if "Google Maps" in competitor_platforms:
            st.markdown(":material/check: Google Maps")
        else:
            st.markdown(":material/close: Google Maps")
        
        if "Tripadvisor" in competitor_platforms:
            st.markdown(":material/check: Tripadvisor")
        else:
            st.markdown(":material/close: Tripadvisor")

        if "The Fork" in competitor_platforms:
            st.markdown(":material/check: The Fork")
        else:
            st.markdown(":material/close: The Fork")

        if "Deliveroo" in competitor_platforms:
            st.markdown(":material/check: Deliveroo")
        else:
            st.markdown(":material/close: Deliveroo")
        
        if "Glovo" in competitor_platforms:
            st.markdown(":material/check: Glovo")
        else:
            st.markdown(":material/close: Glovo")
        
        if "Just Eat" in competitor_platforms:
            st.markdown(":material/check: Just Eat")
        else:
            st.markdown(":material/close: Just East")
        
def render_price_diagram(label, my_row, avg_prices, prices_expanded):
    my_prices = my_row["Prices"].iloc[0]
    my_price = my_prices[label]

    label_metric = label if label != "AVG_PRICE" else "Medio"

    st.metric(
        f"**Prezzo {label_metric}**",
        f"{my_price} €",
        f"{my_price - avg_prices[label]:.2f} € vs competitor",
        delta_color="off",
        border=False
    )

    # --- refactor from here ---
    # Round competitor prices for histogram
    competitor_prices = prices_expanded[label].dropna()
    prezzo_rounded = (competitor_prices * 2).apply(np.floor) / 2

    # Compute frequency
    price_freq = prezzo_rounded.value_counts().reset_index()
    price_freq.columns = ['prezzo_rounded', 'frequency']
    price_freq = price_freq.sort_values('prezzo_rounded')
    price_freq['prezzo_rounded'] += 0.0001  # small offset to avoid exact match issues

    # Highlight your pizzeria price
    highlight_value = (my_price // 0.5 * 0.5) + 0.0001

    # Altair chart
    freq_chart = alt.Chart(price_freq).mark_bar(opacity=1).encode(
        x=alt.X(
            'prezzo_rounded:Q',
            title=None,
            bin=alt.Bin(step=0.5),
            axis=alt.Axis(grid=False)
        ),
        y=alt.Y(
            'frequency:Q',
            title=None,
            axis=alt.Axis(grid=False, labels=False)
        ),
        color=alt.condition(
            alt.datum.prezzo_rounded == highlight_value,
            alt.value("#4285F4"),    # your pizzeria
            alt.value("#808080B6")   # competitors
        ),
        tooltip=[
            alt.Tooltip('prezzo_rounded:Q', title='Prezzo', format='.1f'),
            alt.Tooltip('frequency:Q', title='Numero Pizzerie')
        ]
    ).properties(
        height=188,
        padding={"left": 5, "top": 0, "right": 5, "bottom": 0}
    )

    st.altair_chart(freq_chart, use_container_width=True)

def render_prices_diagram(competition_page_data, name_of_my_pizzeria):
    with st.container(border=True):
        chart_type = st.selectbox(
            "Seleziona tipologia",
            [
                "Quanto Costa la Tua Margherita?",
                "Quanto Costa la tua Pizza diavola?",
                "Quanto Costa la tua Pizza quattro stagioni?",
                "Quanto Costa la tua Pizza in media?"
            ],
            label_visibility="collapsed"
        )

        my_row = competition_page_data.loc[competition_page_data['Name'] == name_of_my_pizzeria]
        other_rows = competition_page_data.loc[competition_page_data['Name'] != name_of_my_pizzeria]

        prices_expanded = pd.json_normalize(other_rows["Prices"])
        avg_prices = prices_expanded.mean(numeric_only=True)

        if chart_type == "Quanto Costa la Tua Margherita?":
            render_price_diagram("margherita", my_row, avg_prices, prices_expanded)

        elif chart_type == "Quanto Costa la tua Pizza diavola?":
            render_price_diagram("diavola", my_row, avg_prices, prices_expanded)

        elif chart_type ==  "Quanto Costa la tua Pizza quattro stagioni?":
            render_price_diagram("quattro stagioni", my_row, avg_prices, prices_expanded)
        
        elif chart_type == "Quanto Costa la tua Pizza in media?":
            render_price_diagram("AVG_PRICE", my_row, avg_prices, prices_expanded)

def render_menu_items_and_stay_and_wait(competition_page_data, name_of_my_pizzeria):

    # Get my values and competitor averages
    my_row = competition_page_data.loc[competition_page_data['Name'] == name_of_my_pizzeria]
    other_rows = competition_page_data.loc[competition_page_data['Name'] != name_of_my_pizzeria]
    
    my_pizzas = my_row["Number of Menu Items"].iloc[0]
    avg_competitor_menu_items = other_rows["Number of Menu Items"].mean()

    my_stay_duration = my_row["Average Stay Duration (hours)"].iloc[0]
    competitor_stay_duration_expanded = other_rows["Average Stay Duration (hours)"].mean()
    my_wait_time = my_row["Maximum Wait Time (min)"].iloc[0]
    competitor_wait_time_expanded = other_rows["Maximum Wait Time (min)"].mean()

    
    # Update metrics with real data
    st.metric("**Nel Menu**", 
                f"{my_pizzas} pizze", 
                f"{my_pizzas - avg_competitor_menu_items:.1f} vs competitor", 
                border=True)
    
    with st.container(border=True): 
        # Update the metrics to remove the division by 60 since data is already in hours
        st.metric("**Permanenza media**", 
                    f"{my_stay_duration:.1f} ore", 
                    f"{(my_stay_duration - competitor_stay_duration_expanded):.1f} vs competitor", 
                    border=False)
        st.metric("**Prima di sedersi**", 
                    f"{int(my_wait_time)} min", 
                    f"{int(my_wait_time - competitor_wait_time_expanded)} vs competitor", 
                    border=False)

def render_general_ratings(competition_page_data, name_of_my_pizzeria):

    # Get my values and competitor averages
    my_row = competition_page_data.loc[competition_page_data['Name'] == name_of_my_pizzeria]
    other_rows = competition_page_data.loc[competition_page_data['Name'] != name_of_my_pizzeria]

    my_historical_rating = my_row["Rating"].iloc[0].get("GENERALE")
    avg_competitor_historical_rating = other_rows["Rating"].apply(lambda x: x.get("GENERALE")).mean()

    my_last_30_days_rating = my_row["Average Rating last 30 days"].iloc[0]
    avg_competitor_last_30_days_rating = other_rows["Average Rating last 30 days"].mean()

    with st.container(border=True):
        st.metric("Rating", 
                    my_historical_rating, 
                    f"{my_historical_rating - avg_competitor_historical_rating:.1f} vs competitor",
                    delta_color="normal")
        
        st.text("")

        my_last_30_days_rating

        st.metric("**Ultimi 30 giorni**", 
                    f"{my_last_30_days_rating} ✨", 
                    f"{my_last_30_days_rating - avg_competitor_last_30_days_rating:.1f} vs competitor",
                    delta_color="normal")
        
def render_comment_diagram(competition_page_data, name_of_my_pizzeria):
    my_row = competition_page_data.loc[competition_page_data['Name'] == name_of_my_pizzeria]

    with st.container(border=True):
        monthly = my_row["Monthly Review Counts"].iloc[0]
        last_4 = dict(list(monthly.items())[-4:])
        
         # --- Convert to DataFrame ---
        df = pd.DataFrame([
            {
                "month": month,
                "positive": counts["above3"],
                "negative": -counts["below_or_eq3"]  # negative for visualization
            }
            for month, counts in last_4.items()
        ])

        # Extract month short labels ("Gen", "Feb", etc.)
        month_map = {
            "01": "Gen", "02": "Feb", "03": "Mar", "04": "Apr",
            "05": "Mag", "06": "Giu", "07": "Lug", "08": "Ago",
            "09": "Set", "10": "Ott", "11": "Nov", "12": "Dic"
        }

        df["mese"] = df["month"].apply(lambda x: month_map[x.split("-")[1]])
        df["mese_full"] = df["month"]

        # --- Compute metric ---
        labelValueRecensioniMensili = df['positive'].iloc[-1] + abs(df['negative'].iloc[-1])
        valueRecensioniMensiliScorsoMese = df['positive'].iloc[-2] + abs(df['negative'].iloc[-2])

        monthlyDifference = (
            (labelValueRecensioniMensili - valueRecensioniMensiliScorsoMese)
            if valueRecensioniMensiliScorsoMese != 0 else 0
        )

        st.metric(
            "**Recensioni Mese Corrente**",
            f"{labelValueRecensioniMensili}",
            f"{monthlyDifference:.1f} rispetto al mese precedente"
        )

        # --- Build the Altair chart ---
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "mese:O",
                    title=None,
                    axis=alt.Axis(
                        grid=False,
                        labelAngle=0,
                        labelPadding=0,
                    ),
                    sort=["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug",
                        "Ago", "Set", "Ott", "Nov", "Dic"],
                ),
                y=alt.Y(
                    "value:Q",
                    title=None,
                    axis=alt.Axis(grid=False, labels=False)
                ),
                color=alt.Color(
                    "variable:N",
                    scale=alt.Scale(range=["#F12929", "#62d41c"]),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip("mese_full:N", title="Periodo"),
                    alt.Tooltip("tipo:N", title="Valutazione"),
                    alt.Tooltip("abs_value:Q", title="Recensioni", format=".0f"),
                ],
            )
            .transform_fold(["positive", "negative"], as_=["variable", "value"])
            .transform_calculate(
                abs_value="abs(datum.value)",
                tipo="datum.variable == 'positive' ? 'Positiva' : 'Negativa'"
            )
            .properties(
                height=110,
                padding={"left": 0, "top": 0, "right": 0, "bottom": 2},
            )
        )

        st.altair_chart(chart, use_container_width=True)

def render_comment_linechart(competition_page_data, name_of_my_pizzeria):
    my_row = competition_page_data.loc[competition_page_data['Name'] == name_of_my_pizzeria]

    with st.container(border=True):
        monthly = my_row["Monthly Reviews by Platform"].iloc[0]
        last_4_months = {
            platform: dict(list(month_counts.items())[-4:])
            for platform, month_counts in monthly.items()
        }

        # Chatgpt, from here please rewrite the altair linechart that shows for each platform reviews per month using the data in last_4_months
        
        # Replace markdown with metric
        st.write("Recensioni per Piattaforma")

        # Convert last_4_months → DataFrame
        df_list = []
        for platform, month_dict in last_4_months.items():
            for month, count in month_dict.items():
                df_list.append({
                    "platform": platform,
                    "month": month,
                    "reviews": count
                })

        df = pd.DataFrame(df_list)

        # Convert YYYY-MM → month short label (IT)
        month_map = {
            "01": "Gen", "02": "Feb", "03": "Mar", "04": "Apr",
            "05": "Mag", "06": "Giu", "07": "Lug", "08": "Ago",
            "09": "Set", "10": "Ott", "11": "Nov", "12": "Dic"
        }

        df["mese"] = df["month"].apply(lambda x: month_map[x.split("-")[1]])
        df["mese_full"] = df["month"]

        # Optional: Total line across all platforms
        df_total = df.groupby("mese")["reviews"].sum().reset_index()
        df_total["platform"] = "Totale"
        df = pd.concat([df, df_total], ignore_index=True)

        # Identify max for Y scaling
        max_reviews = np.ceil(df["reviews"].max())

        # Build line chart
        line_chart = (
            alt.Chart(df)
            .mark_line(point={"filled": False, "fill": "white", "size": 100}, opacity=0.9)
            .encode(
                x=alt.X(
                    "mese:O",
                    title=None,
                    axis=alt.Axis(
                        labelAngle=0,
                        grid=False,
                        labelPadding=10,
                    ),
                    sort=["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                          "Lug", "Ago", "Set", "Ott", "Nov", "Dic"],
                ),
                y=alt.Y(
                    "reviews:Q",
                    title=None,
                    scale=alt.Scale(domain=[0, max_reviews]),
                    axis=alt.Axis(grid=False, labels=False),
                ),
                color=alt.Color(
                    "platform:N",
                    scale=alt.Scale(
                        range=[
                            "#808080B6",  # Totale
                            "#4285F4",    # Google
                            "#5cc9bc",    # Deliveroo
                            "#6be76e",    # TripAdvisor
                            "#ff9100",    # The Fork
                            "#ff4081",    # Glovo
                            "#9c27b0",    # Just Eat
                        ]
                    ),
                    legend=alt.Legend(
                        title=None,
                        orient="top",
                        symbolSize=120,
                    ),
                ),
                tooltip=[
                    alt.Tooltip("platform:N", title="Piattaforma"),
                    alt.Tooltip("mese_full:N", title="Periodo"),
                    alt.Tooltip("reviews:Q", title="Recensioni", format=".0f"),
                ],
            )
            .properties(height=184, padding={"left": -5, "top": -5, "right": 0, "bottom": 0})
        )

        st.altair_chart(line_chart, use_container_width=True)

def render_subcategory_tab(competition_page_data, name_of_my_pizzeria, col_prefix, label):
    my_row = competition_page_data.loc[competition_page_data['Name'] == name_of_my_pizzeria]

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.container(border=True):
            # Get ratings for current category
            my_ratings = my_row["Monthly Category Ratings"].iloc[0][label.upper()]

            # Get last 6 months (order is preserved)
            last_6 = dict(list(my_ratings.items())[-6:])

            months = list(my_ratings.items())

            current_month_value = months[-1][1]
            previous_month_value = months[-2][1]
            rating_trend = current_month_value - previous_month_value

            st.metric(f"Rating {label}",
                    f"{current_month_value:.1f}",
                    f"{rating_trend:+.1f} vs mese precedente",
                    delta_color="normal")

            # -----------------------------
            # Build dataframe for Altair
            # -----------------------------
            df = pd.DataFrame([
                {"month": m, "rating": v}
                for m, v in last_6.items()
            ])

            # Map YYYY-MM → Italian short months
            month_map = {
                "01": "Gen", "02": "Feb", "03": "Mar", "04": "Apr",
                "05": "Mag", "06": "Giu", "07": "Lug", "08": "Ago",
                "09": "Set", "10": "Ott", "11": "Nov", "12": "Dic"
            }

            df["mese"] = df["month"].apply(lambda x: month_map[x.split("-")[1]])
            df["mese_full"] = df["month"]

            # -----------------------------
            # Compute y-axis domain
            # -----------------------------
            min_rating = max(1.0, df["rating"].min() - 0.2)
            max_rating = 5.0

            # -----------------------------
            # Build line chart
            # -----------------------------
            line_chart = (
                alt.Chart(df)
                .mark_line(point={"filled": False, "fill": "white", "size": 100})
                .encode(
                    x=alt.X(
                        "mese:O",
                        title=None,
                        axis=alt.Axis(
                            labelAngle=0,
                            grid=False,
                            labelPadding=20
                        ),
                        sort=["Gen","Feb","Mar","Apr","Mag","Giu",
                              "Lug","Ago","Set","Ott","Nov","Dic"]
                    ),
                    y=alt.Y(
                        "rating:Q",
                        title=None,
                        scale=alt.Scale(domain=[min_rating, max_rating]),
                        axis=alt.Axis(grid=False)
                    ),
                    color=alt.value("#4285F4"),
                    tooltip=[
                        alt.Tooltip("mese_full:N", title="Periodo"),
                        alt.Tooltip("rating:Q", title=f"Rating {label}", format=".1f")
                    ]
                )
                .properties(
                    height=150,
                    padding={"left": 5, "top": 5, "right": 0, "bottom": 5}
                )
            )

            st.altair_chart(line_chart, use_container_width=True)

    with col2:
        with st.container(border=True):

            # --------------------------------------------
            # 1. Extract current-month rating for this category
            # --------------------------------------------
            # Get the monthly ratings dictionary for all pizzerias
            all_ratings = competition_page_data["Monthly Category Ratings"].apply(lambda d: d[label.upper()])

            # Find latest month key (e.g. "2024-12")
            sample_row = all_ratings.iloc[0]
            latest_month = sorted(sample_row.keys())[-1]

            # Your pizzeria rating for latest month
            my_rating = all_ratings.loc[competition_page_data['Name'] == name_of_my_pizzeria].iloc[0][latest_month]

            # Competitors ratings for latest month
            competitor_ratings = all_ratings.loc[competition_page_data['Name'] != name_of_my_pizzeria].apply(lambda d: d[latest_month])
            avg_competitor_rating = competitor_ratings.mean()

            st.metric(
                f"Rating {label} ({latest_month})",
                f"{my_rating:.1f}",
                f"{(my_rating - avg_competitor_rating):+.1f} vs competitor",
                delta_color="normal"
            )

            # --------------------------------------------
            # 2. Build frequency distribution (0.2 bins)
            # --------------------------------------------
            def round_to_bin(x):
                return np.floor(x * 5) / 5   # → 0.2 increments (1.0, 1.2, 1.4...)

            competition_page_data["rating_bin"] = all_ratings.apply(lambda d: round_to_bin(d[latest_month]))

            # Frequency of bins
            rating_freq = competition_page_data.groupby("rating_bin").size().reset_index(name="frequency")

            # Ensure small offset to avoid float comparison issues
            my_rating_bin = round_to_bin(my_rating) + 0.0001
            rating_freq["rating_bin_shift"] = rating_freq["rating_bin"] + 0.0001

            # Compute global minimum for x-axis
            min_bin = competition_page_data["rating_bin"].min()

            # --------------------------------------------
            # 3. Altair histogram
            # --------------------------------------------
            freq_chart = (
                alt.Chart(rating_freq)
                .mark_bar(opacity=1)
                .encode(
                    x=alt.X(
                        "rating_bin_shift:Q",
                        title=None,
                        bin=alt.Bin(step=0.2),
                        scale=alt.Scale(domain=[min_bin, 5.0]),
                        axis=alt.Axis(
                            grid=False,
                            values=list(np.arange(min_bin, 5.1, 0.2))
                        )
                    ),
                    y=alt.Y(
                        "frequency:Q",
                        title=None,
                        axis=alt.Axis(grid=False, labels=False)
                    ),
                    color=alt.condition(
                        alt.datum.rating_bin_shift == my_rating_bin,
                        alt.value("#4285F4"),  # highlight your pizzeria
                        alt.value("#808080B6")  # competitors
                    ),
                    tooltip=[
                        alt.Tooltip("rating_bin:Q", title="Rating", format=".1f"),
                        alt.Tooltip("frequency:Q", title="Numero Pizzerie")
                    ]
                )
                .properties(
                    height=150,
                    padding={"left": 5, "top": 0, "right": 5, "bottom": 0}
                )
            )

            st.altair_chart(freq_chart, use_container_width=True)