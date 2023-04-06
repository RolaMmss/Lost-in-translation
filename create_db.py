import sqlite3
#####################################################
connexion = sqlite3.connect("db_objets_trouves.db")   #Se connecter à la base de données

curseur = connexion.cursor() #SQL.sh pour apprender SQL
#####################################################
curseur.execute(""" 
       CREATE TABLE IF NOT EXISTS objets_trouves(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nom_gare TEXT NOT NULL,
          date TEXT NOT NULL UNIQUE,
          type TEXT NOT NULL
            )
""")
connexion.commit()