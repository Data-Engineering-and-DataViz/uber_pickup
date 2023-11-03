
"""
Le travail avec streamlit
Le premiere des choses est l'importation de modules que nous allons utiliser
Quand on a fini d'ecrire le code d'une app streamlit, on peut la lancer
Le lancement d'une app strealit n'est pas different d'un autre 
script Python. A chaque fois qu'on veut voir l'app nous devons lancer l'app
avec la commande =>:
    streamlit run chemin_nom_du_script

Le nom et le chemin du script peuvent être une URL comme les scripts
stockes sur GitHub par exemple
On peut lancer ainsi =>:
    streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py

    
L'affichage de streamlit a trois butons en haut à droite, c'est là
que nous pouvons configurer quelques fonctionnement comme le hot-reload
à chaque fois qu'on fait des modification et enregistrement

Dans ce code nous chargeons une grande quantité de données, si à chaque
fois qu'on fait de modification le code doit se reexecuter et recharger
ces données cela peut prendre du temps et être moins performant. C'est là
que le système de cache de streamlit entre en jeu
"""
import streamlit as st 
import pandas as pd
import numpy as np

#Ajout du titre de l'app, comme tout bon app

st.title("U pickups in NYC data processing, FH")
#A partir de la, on peut même lancer le script et ajouter les autres modifs au fur et a mesure


DATE_COLUMN = "date/time"
DATA_URL = ("https://s3-us-west-2.amazonaws.com/"
        "streamlit-demo-data/uber-raw-data-sep14.csv.gz")

@st.cache_data
def load_data(nrows):
    """
    load_data est une fonction pure qui telecharge des donnees dans le dataframe de panda
    et les converti la colonne la date (sous forme de texte) en datetime.
    La fonction accepte un seul parametre (nrows), lequel specifies le nombre
    de lignes qu'on veut charger dans le dataframe.
    La quantité de données qu'on veut prendre ici pouvant être conséquante
    Le syteme de cache de streamlit peut nous aider et garder en mémoire cache les données
    déjà charger
    """
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


#On peut tester notre fonction chargement de donnees

#Ajout de texte pour montrer que les données sont en chargement
data_load_state = st.text("Loading data... ...")
# Chargement de 10,000 lignes de données dans le dataframe.
data = load_data(10000)
# data_load_state.text("Loading data ... done !")
data_load_state.text("Done ! (using st.cache_data)")

# ? Inspect the raw data
# st.subheader("Raw data")
# st.write(data)
# Ajout d'un checkbox
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)


"""
Dans le guide des concepts principaux, nous apprenons que la fonction
st.write permet de rendre tout ce qu'on lui passe. Dans notre cas ici
nous lui passons un dataframe de panda et il rend une table interactive.

st.write fait ce qui est mieux en fonction du type de données entrées.
Si nous remarquons qu'il ne fait pas ce que nous esperons, nous pouvons
utiliser une commande spécialisée comme st.dataframe
"""


#?Draw a histogram
"""
Si nous avons une idée sur les raw data et observer qu'est-ce qu'il contient.
Prenons un bon en avant et faisons des histogramme pour voir quel est
le taux d'occupation horaire de User à New York City.

1. Pour commencer, ajoutons un subheader juste en bas de la section raw data
2. Utilisez NumPy pour générer un histogramme qui décompose les heures de ramassage regroupées par heure :
3. Maintenant, utilisons la méthode Streamlit st.bar_chart() pour dessiner cet histogramme.

On peut enregistrer, l'app se met à jour et nous affiche l'histogramme.
Après un survol il semble que l'heure de la plus grande affluence est 17 (17h:00 ou 5 P.M.)

Pour dessiner cet histogramme nous avons utilisé la méthode native de Streamlit qui est
bar_chat(), mais il est important de savoir que Streamlit supporte des graffe plus complexe
comme Altair, Boken, Plotly, Matplotlib et plus encore. Nous pouvons retrouver les graphe
supporté ici: https://docs.streamlit.io/library/api-reference/charts
"""
st.subheader("Nombre de pickups par heure")

hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

print("L'histogramme est =>:", hist_values)

st.bar_chart(hist_values)

#? Plot data on a map
"""
L'usage de l'histogramme dans le dataset de Uber nous a permis
de déterminer quelle était l'heure de la plus grande affluence, mais
comment ferions-nous si nous voulons savoir où est-ce que cette grance
affluence a lieu à travers la ville. Alors que nous pouvons utiliser
les bars de graphes pour affichers ces données, il ne sera pas aisé de
l'interpréter sans être familier avec les coordonnées (lattitude, longitude) de la ville.
Pour afficher cette concentration, tentons d'utiliser la fonction
st.map() de Streamlit pour un aperçu des données sur une carte de la ville de New York.

1. Ajout d'une section subheader
2. On utilise la fonction st.map pour ploter les data
3. On enregistre le script. La carte est complètement interactive. On peut zoomer pour voir de près

L'histogramme nous avons dit que le temps d'affluence le plus élévé est 17h.
Nous pouvons redessiner la carte pour afficher la concentration de 17h:00

Pour déssiner cette carte nous avons utiliser la fonction st.map qui est une fonction
built in de Streamlit, mais si nous voulons visualiser des map complexe nous
pouvons utiliser st.pydeck_chart.

"""

st.subheader("Carte de tous les pickups")
st.map(data)


hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f"Carte de pickup à {hour_to_filter}h:00")
st.map(filtered_data)


#? Filter results with a slider
"""
Dans la dernière partie, lorsque nous dessiner le map, le temps utilisé
pour filtrer les resultats a été hardcodé dans le script, quel serait
si nous voulons lire dynamiquement le filtre de données en temps réel?
En utilisant les Widgets de Streamlit nous pouvons.
Ajoutons un slider avec la méthode st.slider()
1. Ajoutons la place de filtre de l'heure
2. On utilise le slider et on peut voir le resultat
"""

dinamic_hour_to_filter = st.slider("hour", 0, 23, 17)# min: Oh, max: 23h; default 17h
dinamic_filtered_data = data[data[DATE_COLUMN].dt.hour == dinamic_hour_to_filter]
st.subheader(f"Dinamic Carte de pickup à {dinamic_hour_to_filter}h:00")
st.map(dinamic_filtered_data)

#Use a button to toggle data
"""
Les sliders sont juste un moyen de changer dynamiquement la composition de notre app.
Utilisons la fonction st.checkbox pour ajouter un checkbox à l'app.
Nous utilisons ce checkbox pour afficher/masquer la table raw data au debut de l'app.

Nous avons déjà une idée de ce que nous avons obtenu. Après cela nous pouvons voir
tous les widgets que Streamlit expose à patir de API Reference: https://docs.streamlit.io/library/api-reference
https://docs.streamlit.io/library/api-reference
"""




