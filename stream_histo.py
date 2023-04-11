import streamlit as st
import pandas as pd
import plotly.express as px

# Définition de la liste des mois en français
mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

# Définition de la liste des gares
gares = ["Paris Bercy", "Paris Saint-Lazare", "Paris Gare de Lyon", "Paris Gare du Nord", "Paris Montparnasse", "Paris Est", "Paris Austerlitz"]

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

# Ajout du sélecteur pour l'année et le mois
annee = st.selectbox("Choisissez une année", options=range(2019, 2023), index=3)  # valeur par défaut : 2022
mois = st.selectbox("Choisissez un mois", options=mois_fr, index=0)  # valeur par défaut : janvier

# Ajout du sélecteur pour la gare
gare = st.selectbox("Choisissez une gare", options=gares)

# Filtrer les données en fonction de l'année, du mois et de la gare sélectionnés
filtered_data = df[(df["annee"] == annee) & (df["mois"] == mois_fr.index(mois) + 1) & (df["gare"] == gare)]

# Affichage du nombre d'objets perdus dans le titre
title = f"Nombre d'objets perdus en {mois} {annee} à la gare {gare} : {len(filtered_data)}"
st.title(title)

# Affichage de l'histogramme dans Streamlit
st.plotly_chart(px.histogram(filtered_data, x="date", nbins=len(filtered_data), 
                              labels={"date": "Date", "count": "Nombre d'objets perdus"}))
