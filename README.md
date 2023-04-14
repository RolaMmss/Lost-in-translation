# Lost-in-translation
pour visualiser les graphique il faut utiliser le fichier stream_all.py 


# Librairies à installer:
    pip install nbformat
    pip install plotly

# Un token à récuperer:
    MAPBOX_TOKEN à partir de mapbox.com

# Un fichier archive.csv à télécharger à partir de open-meteo.com 

# Contexte du projet

Data Scientist à la SNCF - île de France, votre manager vous demande de vous pencher sur un sujet particulier, la gestion des objets trouvés.

En effet, chaque jour des dizaines d'objets sont perdus et retrouvés dans les gares parisiennes par les voyageurs, leur gestion est critique au niveau de la satisfaction client. Cependant le cout de leur gestion est critique également. On aimerait donc dimensionner au mieux le service en charge de les gérer mais pour cela il faut pouvoir anticiper de manière précise le volume d'objets trouvés chaque jour. Votre manager a une intuition qu'il aimerait vérifier: plus il fait froid plus les voyageurs sont chargés (manteau, écharppes, gant) plus ils ont donc de probabilité de les oublier. Mais empiler toutes ces couches prend du temps, ce qui pousse aussi à se mettre en retard et dans la précipitation, à oublier d'autres affaires encore. A l'aide des données de la SNCF et d'autres données, essayez de creuser cette piste.

++A partir de l’API open data de la sncf.++

    Requeter la base de données des objets trouvés pour récupérer les données entre 2019 et 2022 sur les gares parisiennes
    Stocker les données dans une BDD SQL de votre choix dont vous aurez au préalable réalisé le schéma.

++A partir d’internet:++

    Récupérer la liste des températures journalières sur Paris en France entre 2019 et 2022. (1 température moyenne par jour, à trouver ou à recalculer).

++Data analyse VISUALISATION. - (Sur un streamlit)++

    Calculez entre 2019 et 2022 la somme du nombre d’objets trouvés par semaine. Afficher sur un histogramme plotly la répartition de ces valeurs. (un point correspond à une semaine dont la valeur est la somme). (On peut choisir d’afficher ou non certains types d’objet).
    Afficher une carte de Paris avec le nombre d’objets trouvés en fonction de la fréquentation de voyageur de chaque gare. Possibilité de faire varier par année et par type d’objets

++Partie data analyse en vue de la DATA SCIENCE. - (sur un streamlit)++

    Afficher le nombre d’objets trouvés en fonction de la température sur un scatterplot. Est ce que le nombre d’objets perdus est corrélé à la temperature d'après ce graphique?
    Quelle est la médiane du nombre d’objets trouvés en fonction de la saison? Il y a t il une correlation entre ces deux variables d'après le graphique?
    Affichez le nombre d'objets trouvés en fonction du type de d'objet et de la saison sur un graphique. Il y a t il une correlation entre ces deux variables d'après le graphique?

++Intégrez à votre streamlit la conclusion globale de votre étude.++

++**Bonus data ingenieur: **++

Ajoutez un bouton à votre page streamlit qui permet la mise à jour des données de l'app (on va récupèrer toutes les données nécessire jusqu'à la dernière date disponible).