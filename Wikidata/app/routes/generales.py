from ..app import app
from flask import render_template
import requests


@app.route('/') 
# route de la racine pour la page d'accueil
def home():
    return render_template('pages/accueil.html')

@app.route('/retrieve_wikidata/<id>', methods=['GET'])
# route de l'application
def retrieve_wikidata(id):
    #API Wikidata
    wd_url = f'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={id}&format=json'
    # l'Url de l'API wikidata
    response = requests.get(wd_url) #envoi de la requête à l'API avec requests 
    data = response.json()

    if 'entities' in data: # vérifie si entities est dans data
        entity_data = data['entities'].get(id, {})
        metadata = {
            """
            crée un dictionnaire avec le code de la réponse HTTP
            ces données sont ensuite appelée grâce à Jinja dans la page html retrieve_wikidata
            """
            'status_code': response.status_code,
            'content_type': response.headers.get('Content-Type')
        }
        return render_template('pages/retrieve_wikidata.html', 
                               id=id, 
                               metadata=metadata, 
                               entity_data=entity_data, 
                               error=None)
    else:
        # si entities n'est pas dans data, n'affiche que l'id mais pas les métadonnées avec une erreur
        return render_template('pages/retrieve_wikidata.html', 
                               id=id, 
                               metadata=None, 
                               entity_data=None, 
                               error="Aucune donnée valide trouvée.")
