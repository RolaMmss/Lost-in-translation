import plotly.express as px
import pandas as pd
import sqlite3
import streamlit as st
import numpy as np

# se connecter à la base de données SQLite
connexion = sqlite3.connect("db_objets_trouves.db")

# lire les données de la table "meteo_objets_trouves" dans un DataFrame pandas
df = pd.read_sql_query("SELECT date, temperature, nbr_perdu FROM meteo_objets_trouves", connexion)

# calculer la droite de régression linéaire
coef = np.polyfit(df["temperature"], df["nbr_perdu"], deg=1)
poly1d_fn = np.poly1d(coef)

# affichage du titre
st.title("Relation entre la température et le nombre d'objets perdus")

# affichage du scatterplot avec la droite de régression linéaire
fig = px.scatter(df, x="temperature", y="nbr_perdu")
fig.add_scatter(x=df["temperature"], y=poly1d_fn(df["temperature"]), mode="lines", name="regression line")

# Affichage de la figure dans Streamlit
st.plotly_chart(fig)
