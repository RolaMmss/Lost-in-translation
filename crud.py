import pandas as pd
import sqlite3



# Connecter à la base de données
conn = sqlite3.connect('db_objets-trouves.db')
# Charger le fichier CSV dans un DataFrame Pandas
df = pd.read_csv('objets-trouves.csv')

# Enregistrer le DataFrame dans la base de données
df.to_sql('db_objets_trouves', conn, if_exists='replace', index=False)

# Fermer la connexion
conn.close()
