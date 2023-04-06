import requests
import pandas as pd

pd.set_option('display.max_columns', None)

station_names = ["Paris Bercy", "Paris Saint-Lazare", "Paris Gare de Lyon", "Paris Gare du Nord", "Paris Montparnasse", "Paris Est", "Paris Austerlitz"]
records = []

for name in station_names:
    for year in range(2019, 2023):
        url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=Paris&rows=10000&sort=date&facet=date&facet=gc_obo_gare_origine_r_name&facet=gc_obo_type_c&refine.gc_obo_gare_origine_r_name={name.replace(' ', '+')}&refine.date={year}"
        response = requests.get(url)
        data = response.json()
        records += data['records']

df = pd.json_normalize(records)
df = df.loc[:, ['fields.date', 'fields.gc_obo_gare_origine_r_name', 'fields.gc_obo_type_c']]
df = df.rename(columns={'fields.date': 'date', 'fields.gc_obo_gare_origine_r_name': 'gare', 'fields.gc_obo_type_c': 'type d\'objet'})
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# création du CSV 
df.to_csv("objets-trouves.csv", index=False)

df