import requests
import os

def obtenir_image(id_pokemon, url):
    if url != None:
        dossier=os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets", "sprites")
        os.makedirs(dossier, exist_ok=True)
        fichier=str(id_pokemon) +".png"
        chemin_fichier=os.path.join(dossier,fichier)
        if os.path.exists(chemin_fichier):
            return chemin_fichier
        else:
            try:
                reponse=requests.get(url, timeout=10)
                reponse.raise_for_status()
                with open(chemin_fichier,"wb") as f:
                    f.write(reponse.content)
                return chemin_fichier
            except requests.exceptions.RequestException:
                print("erreur : requests.exceptions.RequestException")
                return None
    return None

if __name__ == "__main__":
    print(obtenir_image(244, "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/244.png"))