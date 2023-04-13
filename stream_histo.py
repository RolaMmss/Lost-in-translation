import streamlit as st
import pandas as pd
import plotly.express as px

# lire le fichier CSV dans un DataFrame pandas
df = pd.read_csv("objets-trouves.csv")

# convertir la colonne "date" en type datetime
df["date"] = pd.to_datetime(df["date"])

# extraire l'année et le mois dans deux colonnes distinctes
df["annee"] = df["date"].dt.year
df["mois"] = df["date"].dt.month

# filtrer les données entre 2019 et 2022
start_date = pd.Timestamp("2019-01-01")
end_date = pd.Timestamp("2022-12-31")
df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

# récupérer les types d'objets uniques
types_objets = df["type d'objet"].unique()

# Définition de la liste des mois en français
mois_fr = ["Tous", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

# Définition de la liste des gares
gares = ["Tous", "Paris Bercy", "Paris Saint-Lazare", "Paris Gare de Lyon", "Paris Gare du Nord", "Paris Montparnasse", "Paris Est", "Paris Austerlitz"]

# Ajout du sélecteur pour l'année et le mois
annee = st.selectbox("Choisissez une année", options=range(2019, 2023), index=3)  # valeur par défaut : 2022
mois = st.selectbox("Choisissez un mois", options=mois_fr, index=0)  # valeur par défaut : Tous

# Ajout du sélecteur pour la gare
gare = st.selectbox("Choisissez une gare", options=gares, index=0)  # valeur par défaut : Tous

# Ajout du sélecteur pour le type d'objet
select_type_objet = st.selectbox("Choisissez un type d'objet (optionnel)", options=["Tous"] + list(types_objets))
if select_type_objet != "Tous":
    df = df[df["type d'objet"] == select_type_objet]

# Filtrer les données en fonction de l'année, du mois et de la gare sélectionnés
if mois == "Tous" and gare == "Tous":
    filtered_data = df[(df["annee"] == annee)]
elif mois == "Tous":
    filtered_data = df[(df["annee"] == annee) & (df["gare"] == gare)]
elif gare == "Tous":
    filtered_data = df[(df["annee"] == annee) & (df["mois"] == mois_fr.index(mois))]
else:
    filtered_data = df[(df["annee"] == annee) & (df["mois"] == mois_fr.index(mois)) & (df["gare"] == gare)]

# Affichage du nombre d'objets perdus dans le titre
title = f"Nombre d'objets perdus en {mois} {annee} à la gare {gare}"
if select_type_objet != "Tous":
    title += f" pour le type d'objet : {select_type_objet}"
title += f" il y à  {len(filtered_data)} objets"
st.title(title)

# Affichage de l'histogramme dans Streamlit
st.plotly_chart(px.histogram(filtered_data, x="date", nbins=len(filtered_data), 
                              labels={"date": "Date", "count": "Nombre d'objets perdus"}))
