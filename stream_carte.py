import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

# Récupération du token Mapbox
map_token = os.getenv('MAPBOX_TOKEN')

# Connexion à la base de données SQLite
connexion = sqlite3.connect("db_objets_trouves.db")

# Ajout d'un selecteur pour l'année
year = st.selectbox("Select a year", ["2019", "2020", "2021", "2022"])

# Récupération des types d'objets disponibles dans la table 'objets_trouves'
objets_trouves_df = pd.read_sql_query("SELECT DISTINCT type_objet FROM objets_trouves", connexion)

# Création d'une liste des types d'objets à afficher dans le selecteur
objets_trouves_list = ["Tous"] + list(objets_trouves_df['type_objet'].values)

# Ajout d'un selecteur pour le type d'objet requis
objet_type = st.selectbox("Select an object type", objets_trouves_list)

# Récupération des données de la table 'objets_trouves' pour l'année et le type d'objet sélectionnés
if objet_type == "Tous":
    query = f"SELECT o.*, g.latitude, g.longitude FROM objets_trouves o JOIN gares_objets_perdus g ON o.gare = g.gare WHERE o.date LIKE '{year}-%'"
else:
    query = f"SELECT o.*, g.latitude, g.longitude FROM objets_trouves o JOIN gares_objets_perdus g ON o.gare = g.gare WHERE o.date LIKE '{year}-%' AND o.type_objet = '{objet_type}'"

df = pd.read_sql_query(query, connexion)

# Fermeture de la connexion à la base de données SQLite
connexion.close()

# Calcul de la somme des objets par type
df_somme = df.groupby('type_objet')['id'].count().reset_index()
df_somme = df_somme.rename(columns={'id': 'nombre'})

# Affichage de la somme des objets par type
st.write(df_somme)

# Configuration de l'accès à l'API de Mapbox
px.set_mapbox_access_token(map_token)

# Création de la carte
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="type_objet", size="id",
                  color_discrete_sequence=px.colors.qualitative.Safe,
                  zoom=10,
                  hover_name="gare", hover_data={"date": True, "type_objet": True, "id": True})

# Ajout du titre avec l'année sélectionnée
fig.update_layout(title=f"Objets trouvés dans les gares en {year}")

# Configuration des annotations pour la colonne 'frequantation' et 'taux_objets_perdus'
fig.update_traces(hovertemplate="<b>%{hovertext}</b><br><br>Date: %{customdata[0]}<br>Type d'objet: %{customdata[1]}<br>Nombre d'objets trouvés: %{customdata[2]}")

# Affichage de la carte dans Streamlit
st.plotly_chart(fig)