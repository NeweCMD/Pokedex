import requests

BASE_URL = "https://pokeapi.co/api/v2"

def recuperer_pokemon(nom):
    'permet de faire une requete API pour récuperer le pokémon par son nom et renvois sa réponse au format .json ou None'
    url = f"{BASE_URL}/pokemon/{nom.lower().strip()}"
    try:
        reponse = requests.get(url, timeout=10)
        reponse.raise_for_status()
        return reponse.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur : {e}")
        return None

def extraire_infos(donnees):
    'permet de récuperer les données d un pokemon en format .Json et renvoie un dictionnaire avec id, nom, liste des types, liste des statistiques, taille, poids, liens vers son sprite avant, sprite arriere et cri'
    if donnees != None :
        return {
            "id": donnees["id"],
            "nom": donnees["name"],
            "types": [t["type"]["name"] for t in donnees["types"]],
            "stats": {s["stat"]["name"]: s["base_stat"] for s in donnees["stats"]},
            "taille": donnees["height"] / 10,   # en mètres
            "poids": donnees["weight"] / 10,    # en kg
            "sprite_avant": donnees["sprites"]["front_default"],
            "sprite_arriere": donnees["sprites"]["back_default"],
            "cri": donnees["cries"]["latest"]
        }
    return None

def recup_liste_nom(nb=20):
    'récupère une liste de nom de pokémon de l API'
    liste_nom=[]
    param={"limit":nb}
    try:
        reponse = requests.get("https://pokeapi.co/api/v2/pokemon",param, timeout=10)
        reponse.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur : {e}")
        return None
    donnee=reponse.json()
    for elt in donnee["results"]:
        liste_nom.append(elt["name"])
    return liste_nom

if __name__ == "__main__":
    donnees = recuperer_pokemon("zorua")
    if donnees:
        print(extraire_infos(donnees))
    print(recup_liste_nom(1)) #1351 est le nombre de pokemon dans l'api en comptant toutes les différentes formes (méga, pyroar-male/female, etc...)