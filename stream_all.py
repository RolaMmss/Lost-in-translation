import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
map_token = os.getenv('MAPBOX_TOKEN')
connexion = sqlite3.connect("db_objets_trouves.db")
px.set_mapbox_access_token(map_token)

# Sidebar pour sélectionner l'onglet
onglet = st.sidebar.selectbox("Choisissez un onglet", ["Histogramme", "Carte objet perdu", "Carte frequantation" ,"Scatter","saison","saison median", "histo bar"])

# Histogramme  ///////////////////////////////////////////////////////////////////////////////////////
if onglet == "Histogramme":
        # affichage du titre
    st.title("Histogramme des nombre d'objets perdus par rapport a la date et le type d'objets ")

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
    # title = f"Nombre d'objets perdus en {mois} {annee} à la gare {gare}"
    # if select_type_objet != "Tous":
    #     title += f" pour le type d'objet : {select_type_objet}"
    # title += f" il y à  {len(filtered_data)} objets"
    # st.title(title)

    # Affichage de l'histogramme dans Streamlit
    st.plotly_chart(px.histogram(filtered_data, x="date", nbins=len(filtered_data), 
                                labels={"date": "Date", "count": "Nombre d'objets perdus"}))


    # Carte ///////////////////////////////////////////////////////////////////////////////////////
elif onglet == "Carte objet perdu":
    st.title("Objets trouvés dans les gares par type d'objets ")
    
    
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
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="id",
                    color_continuous_scale=px.colors.sequential.Reds, size_max=10,
                    zoom=10,
                    hover_name="gare", hover_data={"date": True, "type_objet": True, "id": True})


    # Ajout du titre avec l'année sélectionnée
    fig.update_layout(title=f"Objets trouvés dans les gares en {year}")

    # Configuration des annotations pour la colonne 'frequantation' et 'taux_objets_perdus'
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br><br>Date: %{customdata[0]}<br>Type d'objet: %{customdata[1]}<br>Nombre d'objets trouvés: %{customdata[2]}")

    # Affichage de la carte dans Streamlit
    st.plotly_chart(fig)
    
# Carte ///////////////////////////////////////////////////////////////////////////////////////
elif onglet == "Carte frequantation":
    st.title("Carte frequentation dans les gares de Paris ")

    # Connexion à la base de données SQLite
    connexion = sqlite3.connect("db_objets_trouves.db")

    # Ajout d'un selecteur pour l'année
    year = st.selectbox("Select a year", ["2019", "2020", "2021", "2022"])

    # Récupération des données de la table 'objet_perdu_annee' pour l'année sélectionnée
    query = f"SELECT * FROM gares_objets_perdus WHERE annee = {year}"
    df = pd.read_sql_query(query, connexion)

    # Formatage de la colonne 'frequantation' avec des séparateurs de milliers
    df['frequantation'] = df['frequantation'].apply(lambda x: '{:,}'.format(x))

    # Fermeture de la connexion à la base de données SQLite
    connexion.close()

    # Configuration de l'accès à l'API de Mapbox
    px.set_mapbox_access_token(map_token)

    # Création de la carte
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="Nbr_perdu", size="Nbr_perdu",
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15,
                    center={"lat": 48.8566, "lon": 2.3522}, zoom=10,
                    hover_name="gare", hover_data={"frequantation": True, "Nbr_perdu": True})

    # Ajout du titre avec l'année sélectionnée
    fig.update_layout(title=f"Objets perdus dans les gares en {year}")

    # Configuration des annotations pour la colonne 'frequantation'
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br><br>Frequantation: %{customdata[0]}<br>Objets perdus: %{customdata[1]}")

    # Affichage de la carte dans Streamlit
    st.plotly_chart(fig)


# Scatter ///////////////////////////////////////////////////////////////////////////////////////
elif onglet == "Scatter":
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
    st.write(" Après avoir effectué l'analyse, il n'a pas été trouvé de corrélation significative entre le nombre d'objets perdus et la température. En effet, la droite de régression linéaire obtenue ne montre pas une évolution nette du nombre d'objets perdus en fonction de la température. Ainsi, on peut conclure que la température n'a pas d'impact direct sur le nombre d'objets perdus dans cette étude.  ")
    # Affichage de la figure dans Streamlit
    st.plotly_chart(fig)
    
# saison ///////////////////////////////////////////////////////////////////////////////////////
elif onglet == "saison":
    st.title("nombre d'objets perdus par saison")

    # lire les données de la table "meteo_objets_trouves" dans un DataFrame pandas
    df = pd.read_sql_query("SELECT date, temperature, nbr_perdu FROM meteo_objets_trouves", connexion)

    # convertir la colonne "date" en datetime
    df['date'] = pd.to_datetime(df['date'])

    # Ajouter une colonne "saison" basée sur les mois et les jours
    df['saison'] = pd.cut(df['date'].dt.month + df['date'].dt.day / 100,
                        [0, 3.21, 6.21, 9.23, 31.21],
                        labels=['hiver', 'printemps', 'été', 'automne'], include_lowest=True)

    # Calculer la médiane du nombre d'objets perdus par saison
    mediane_nbr_perdu_par_saison = df.groupby('saison')['nbr_perdu'].median()

    

    fig = px.histogram(df, x="saison", y="nbr_perdu", color="saison",
                    title=" ")
    fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
    st.plotly_chart(fig)
    
# saison ///////////////////////////////////////////////////////////////////////////////////////
elif onglet == "saison median":
    # titre de l'application Streamlit
    st.title("Distribution du nombre d'objets perdus par saison")

    # lire les données de la table "meteo_objets_trouves" dans un DataFrame pandas
    df = pd.read_sql_query("SELECT date, temperature, nbr_perdu FROM meteo_objets_trouves", connexion)

    # convertir la colonne "date" en datetime
    df['date'] = pd.to_datetime(df['date'])

    # Ajouter une colonne "saison" basée sur les mois et les jours
    df['saison'] = pd.cut(df['date'].dt.month + df['date'].dt.day / 100,
                        [0, 3.21, 6.21, 9.23, 31.21],
                        labels=['hiver', 'printemps', 'été', 'automne'], include_lowest=True)

    # Ajouter une colonne "année" basée sur la colonne "date"
    df['année'] = df['date'].dt.year

    # Sélectionner les années disponibles dans les données
    années_disponibles = df['année'].unique()

    # Sélectionner l'année à afficher à partir d'un sélecteur
    année_selectionnée = st.selectbox('Sélectionner une année', années_disponibles)

    # Filtrer les données pour l'année sélectionnée
    df_année_selectionnée = df[df['année'] == année_selectionnée]

    # Calculer la médiane du nombre d'objets perdus par saison pour l'année sélectionnée
    mediane_nbr_perdu_par_saison = df_année_selectionnée.groupby('saison')['nbr_perdu'].median()

    # Créer un boxplot avec Plotly Express pour l'année sélectionnée
    fig = px.box(df_année_selectionnée, x="saison", y="nbr_perdu", color="saison",
                title=f"Distribution du nombre d'objets perdus par saison pour l'année {année_selectionnée}")
    fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
    st.plotly_chart(fig)

# histo bar ///////////////////////////////////////////////////////////////////////////////////////
elif onglet == "histo bar":

    # lire le fichier CSV dans un DataFrame pandas
    df = pd.read_csv("objets-trouves.csv")

    # convertir la colonne "date" en type datetime
    df["date"] = pd.to_datetime(df["date"])

    # filtrer les données entre 2019 et 2022
    start_date = pd.Timestamp("2019-01-01")
    end_date = pd.Timestamp("2022-12-31")
    # du lundi au dimanche 
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # renommer la colonne "type d'objet" en "Nbr_perdu"
    df = df.rename(columns={"type d'objet": "Nbr_perdu"})

    # grouper les données par semaine et calculer la somme du nombre d'objets pour chaque semaine
    weekly_sum = df.groupby(pd.Grouper(key="date", freq="w"))["Nbr_perdu"].count().reset_index()

    # créer la figure avec Plotly
    fig = px.histogram(df, x="date", nbins=len(weekly_sum), color="Nbr_perdu",
                    color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(xaxis_title="Date (Semaine)", yaxis_title="Nombre d'objets perdus")

    # afficher la figure
    st.plotly_chart(fig)