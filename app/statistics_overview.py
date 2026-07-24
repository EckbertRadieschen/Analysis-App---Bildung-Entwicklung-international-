import plotly.express as px
import streamlit as st


import plotly.express as px
import streamlit as st


def create_category_statistics_bar_chart(
    category_type: str,
    evaluation: dict
):
    """
    Erstellt ein Balkendiagramm für Kategorie-Statistiken.

    category_type: "development" oder "education"

    evaluation: Dictionary mit label und value_column
    """

    

    df = st.session_state["category_statistics"].copy()

    df = df[df["category_type"] == category_type].copy()

    value_column = evaluation["value_column"]
    evaluation_type = evaluation["label"]

    df = df.sort_values(value_column,ascending=True)

    title_first_part = (
        "Entwicklungskategorien" 
        if category_type == "development"
        else "Bildungskategorien"
    )

    chart_title = f"{title_first_part} - {evaluation_type}"

    fig = px.bar(
        df,
        x=value_column,
        y="category",
        orientation="h",
        text=value_column
    )

    fig.update_xaxes(showticklabels=False)

    fig.update_layout(
        xaxis_title=evaluation["label"],
        yaxis_title="",
        showlegend=False,
        height=500,
        title=chart_title,
            title_x=0.5,
            title_xanchor="center"
    )

    if value_column == "relevance_ratio":
        fig.update_traces(
            texttemplate="%{text:.2%}"
        )
    else:
        fig.update_traces(
            texttemplate="%{text:.2f}"
        )

    return fig


def statistics_overview_content():

    evaluation = st.session_state["statistics_evaluation"]

    fig_dev = create_category_statistics_bar_chart("development", evaluation)
    fig_edu = create_category_statistics_bar_chart("education", evaluation)

    

    chart_column_1, chart_blank, chart_column_2 = st.columns([6, 1, 6])

    with chart_column_1:
        st.plotly_chart(
            fig_dev,
            key="statistics_dev_category_bar"
        )
    with chart_column_2:    
        st.plotly_chart(
            fig_edu,
            key="statistics_edu_category_bar"
        )