
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

df = pd.read_csv(Path(__file__).resolve().parent / "data" / "titanic.csv")
# df = pd.read_csv("data/titanic.csv")
df.columns = df.columns.str.lower()

df["class"] = df["pclass"].map({1: "First", 2: "Second", 3: "Third"})
df["survival"] = df["survived"].map({0: "Died", 1: "Survived"})
df["port"] = df["embarked"].map({
    "C": "Cherbourg",
    "Q": "Queenstown",
    "S": "Southampton"
})

df["family_size"] = df["sibsp"] + df["parch"] + 1

df["title"] = df["name"].str.extract(r",\s*([^.]+)\.", expand=False)

df["age_group"] = pd.cut(
    df["age"],
    [0, 12, 18, 35, 60, 80],
    labels=["child", "teen", "young adult", "adult", "senior"]
)

ORDERS = {
    "class": ["First", "Second", "Third"],
    "survival": ["Died", "Survived"],
    "age_group": ["child", "teen", "young adult", "adult", "senior"]
}

COLORS = {
    "Died": "#D95D4A",
    "Survived": "#0F766E"
}

st.title("Titanic Survival Analysis Dashboard")

st.caption("Explore Titanic passenger data and survival statistics.")

# st.image("utils/titanic.jpeg")
st.image(str(Path(__file__).resolve().parent / "utils" / "titanic.jpeg"))

show_data = st.checkbox("Show sample data")

if show_data:
    st.dataframe(df.head(10), hide_index=True)

classes = st.multiselect(
    "Select classes",
    ORDERS["class"],
    default=ORDERS["class"]
)

gender = st.radio(
    "Select gender",
    ["Male", "Female"],
    horizontal=True
)

data = df[
    (df["class"].isin(classes)) &
    (df["sex"].str.lower() == gender.lower())
]

c1, c2 = st.columns(2)

with c1:
    fig = px.histogram(
        data,
        x="family_size",
        nbins=11,
        labels={
            "family_size": "Family size (incl. the passenger)"
        },
        title="How big were the families on board?"
    )

    fig.update_layout(
        bargap=0.1,
        yaxis_title="Passengers"
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:
    outcome = data["survival"].value_counts().reset_index()
    outcome.columns = ["survival", "count"]

    fig2 = px.pie(
        outcome,
        names="survival",
        values="count",
        hole=0.5,
        color="survival",
        color_discrete_map=COLORS,
        title="Died vs Survived"
    )

    st.plotly_chart(fig2, use_container_width=True)
