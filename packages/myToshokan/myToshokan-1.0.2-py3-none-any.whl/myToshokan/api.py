import requests

def create_script(title, platform_name, content_platform_number, language_name, subtitles_data, session):
    """Sent the extracted subttiles to be processed by the API."""
    api_url = f"http://127.0.0.1:8000/api/create/one/script/{platform_name}/{content_platform_number}/{language_name}"
    response = session.post(api_url, json=subtitles_data)
    if response.status_code == 200:
        print(f"Script successfully created for {title} in: {language_name}.")
    else:
        print(f"Error while creating script for {title}: {response.status_code}")

def fetch_content_not_found(platform_name):
    """Récupère les contenus non trouvés pour une plateforme donnée."""
    api_url = f"http://127.0.0.1:8000/api/read/contents_not_found/{platform_name}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération des données depuis l'API: {response.status_code}")
        return []

def update_content_not_found(platform_name, content_platform_number, session):
  """Met à jour l'attribut subtitle_extractor_try en true."""
  api_url = f"http://127.0.0.1:8000/api/update/contents_not_found/urls/{content_platform_number}/{platform_name}"
  update_data = {'subtitle_extractor_try': True} 
  response = session.put(api_url, json=update_data)
  if response.status_code == 200:
    print(f"Mise à jour réussie pour {content_platform_number} en {platform_name}.")
  else:
    print(f"Erreur lors de la mise à jour pour {content_platform_number} en {platform_name}: {response.status_code}")

def fetch_one_script(platform_name, content_platform_number, language_name):
    """Récupère un script pour une plateforme, un contenu et une langue donnés."""
    api_url = f"http://127.0.0.1:8000/api/read/one/script/{platform_name}/{content_platform_number}/{language_name}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération des données depuis l'API: {response.status_code}")
        return []
