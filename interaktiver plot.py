import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv("countries_gender_counts.csv")

# Nettoyer / préparer
df["total"] = df["male"] + df["female"] + df["unknown"]
top10 = df.sort_values("total", ascending=False).head(10)

# Transformer les colonnes male/female/unknown en format long
df_long = top10.melt(
    id_vars=["Country/countries", "total"],
    value_vars=["male", "female", "unknown"],
    var_name="Gender",
    value_name="Count"
)

# Graphique interactif
fig = px.bar(
    df_long,
    x="Country/countries",
    y="Count",
    color="Gender",
    title="Interactive Gender Distribution in Unicorn Startups by Country",
    labels={
        "Country/countries": "Country",
        "Count": "Number of Founders",
        "Gender": "Gender"
    },
    hover_data=["total"],
    barmode="stack",
    text="Count"
)

# Design professionnel
fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_tickangle=-45,
    legend_title_text="Founder Gender",
    height=650,
    width=1100
)

fig.update_traces(textposition="inside")

# Sauvegarde en HTML interactif
fig.write_html("interactive_gender_distribution.html")

# Afficher dans le navigateur
fig.show()