import streamlit as st
import altair as alt
import pandas as pd


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
        
        

