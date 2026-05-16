import pandas as pd
import matplotlib.pyplot as plt

# Lire les données
df = pd.read_csv("countries_gender_counts.csv")

# Trier par nombre de founders masculins
df = df.sort_values(by="male", ascending=False)

# Garder les 10 premiers pays
top10 = df.head(10)

# Taille de la figure
plt.figure(figsize=(15,8))

# Couleurs modernes
male_color = "#4F81BD"
female_color = "#C0504D"
unknown_color = "#9BBB59"

# Barres empilées
plt.bar(
    top10["Country/countries"],
    top10["male"],
    color=male_color,
    label="Male"
)

plt.bar(
    top10["Country/countries"],
    top10["female"],
    bottom=top10["male"],
    color=female_color,
    label="Female"
)

plt.bar(
    top10["Country/countries"],
    top10["unknown"],
    bottom=top10["male"] + top10["female"],
    color=unknown_color,
    label="Unknown"
)

# Titre principal
plt.title(
    "Gender Distribution in Unicorn Startups by Country",
    fontsize=18,
    fontweight="bold"
)

# Labels axes
plt.xlabel("Countries", fontsize=14)
plt.ylabel("Number of Founders", fontsize=14)

# Rotation noms pays
plt.xticks(rotation=45, fontsize=11)

# Taille axe Y
plt.yticks(fontsize=11)

# Grille discrète
plt.grid(
    axis='y',
    linestyle='--',
    alpha=0.4
)

# Légende
plt.legend(
    title="Gender",
    fontsize=11
)

# Layout propre
plt.tight_layout()

# Sauvegarder image HD
plt.savefig(
    "professional_gender_plot.png",
    dpi=300
)

# Afficher
plt.show()