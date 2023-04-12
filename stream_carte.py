import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import sqlite3

load_dotenv()

# Récupération du token Mapbox
map_token = os.getenv('MAPBOX_TOKEN')

# Connexion à la base de données SQLite
connexion = sqlite3.connect("db_objets_trouves.db")

# Ajout d'un selecteur pour l'année
year = st.selectbox("", ["2019", "2020", "2021", "2022"])

# Ajout d'un selecteur pour le type d'objet
objet_type = st.selectbox("", ["Tous"] + list(pd.read_sql_query("SELECT DISTINCT type_objet FROM objets_trouves", connexion)['type_objet'].values))

if objet_type == "Tous":
    # Récupération des données de la table 'gares_objets_perdus' pour l'année sélectionnée
    df = pd.read_sql_query(f"SELECT gop.*, ot.type_objet FROM gares_objets_perdus gop JOIN objets_trouves ot ON gop.gare = ot.gare WHERE gop.annee = {year}", connexion)
else:
    # Récupération des données de la table 'gares_objets_perdus' pour l'année sélectionnée et le type d'objet sélectionné
    df = pd.read_sql_query(f"SELECT gop.*, ot.type_objet FROM gares_objets_perdus gop JOIN objets_trouves ot ON gop.gare = ot.gare WHERE gop.annee = {year} AND ot.type_objet = '{objet_type}'", connexion)

# Formatage de la colonne 'frequantation' avec des séparateurs de milliers
df['frequantation'] = df['frequantation'].apply(lambda x: '{:,}'.format(x))

# Fermeture de la connexion à la base de données SQLite
connexion.close()

# Groupement des données par type d'objet et comptage du nombre total d'objets pour chaque type
count_by_type = df.groupby('type_objet')['Nbr_perdu'].count()

# Affichage du nombre d'objets par type
st.write(count_by_type)

# Configuration de l'accès à l'API de Mapbox
px.set_mapbox_access_token(map_token)

# Création de la carte
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="Nbr_perdu", size="Nbr_perdu",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15,
                  center={"lat": 48.8566, "lon": 2.3522}, zoom=10,
                  hover_name="gare", hover_data={"frequantation": True, "Nbr_perdu": True, "type_objet": True})

# Ajout du titre avec l'année sélectionnée
fig.update_layout(title=f"Objets perdus dans les gares en {year}")

# Configuration des annotations pour la colonne 'frequantation'
fig.update_traces(hovertemplate="<b>%{hovertext}</b><br><br>Frequantation: %{customdata[0]}<br>Objets perdus: %{customdata[1]}<br>Type d'objet: %{customdata[2]}")

# Affichage de la carte dans Streamlit
st.plotly_chart(fig)
