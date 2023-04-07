import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json
import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta


# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Récupération de la clé API depuis les variables d'environnement
api_key = os.getenv("API_KEY")
#############################################################

# Coordonnées de latitude et de longitude pour Paris
LATITUDE = 48.8534
LONGITUDE = 2.3488
#############################################################

# Fonction pour récupérer la température moyenne pour une date donnée
def get_temperature(date):
    # Générer le lien avec la date et la clé API
    url = f"https://history.openweathermap.org/data/3.0/history/timemachine?lat={LATITUDE}&lon={LONGITUDE}&dt={date}&appid={api_key}"
    # Envoyer une requête GET à l'API et récupérer la réponse en format JSON
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    # Extraire la température moyenne de la réponse
    temperature = data["main"]["temp"]#["avg"]
    return temperature
get_temperature(1680788399)
# # Fonction pour calculer la température moyenne journalière pour une année donnée
# def get_daily_average_temperatures(year):
#     # Initialiser un dictionnaire pour stocker les températures par jour
#     daily_temperatures = {}
#     # Boucle sur chaque jour de l'année
#     for month in range(1, 13):
#         for day in range(1, 32):
#             # Générer le timestamp UNIX pour la date
#             date = f"{year}-{month:02d}-{day:02d}"
#             timestamp = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
#             # Récupérer la température moyenne pour la date
#             temperature = get_temperature(timestamp)
#             # Ajouter la température moyenne au dictionnaire
#             daily_temperatures[date] = temperature
#     # Calculer la température moyenne journalière pour l'année
#     daily_average_temperatures = {}
#     for month in range(1, 13):
#         for day in range(1, 32):
#             date = f"{year}-{month:02d}-{day:02d}"
#             # Extraire les températures pour les 24 heures de la journée
#             temperatures = [daily_temperatures[f"{date} {hour:02d}:00:00"] for hour in range(24)]
#             # Calculer la température moyenne pour la journée
#             daily_average_temperatures[date] = sum(temperatures) / len(temperatures)
#     return daily_average_temperatures

# # Récupérer les températures moyennes journalières pour les années 2019, 2020, 2021 et 2022
# temperatures_2019 = get_daily_average_temperatures(2019)
# temperatures_2020 = get_daily_average_temperatures(2020)
# temperatures_2021 = get_daily_average_temperatures(2021)
# temperatures_2022 = get_daily_average_temperatures(2022)

# # Afficher les températures moyennes pour chaque jour de chaque année
# print("Températures moyennes journalières pour Paris:")
# print("2019:", temperatures_2019)
# print("2020:", temperatures_2020)
# print("2021:", temperatures_2021)
# print("2022:", temperatures_2022)

