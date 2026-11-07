import json
import os
import base_donnees as bd

if __name__=="__main__":
    with bd.connecter() as connec:
        liste_pokemon=connec.execute("""SELECT * FROM pokemon ORDER BY id""").fetchall()
    liste_dict=[]
    for pokemon in liste_pokemon:
        liste_dict.append(dict(pokemon))
    dossier_json=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","docs")
    os.makedirs(dossier_json, exist_ok=True)
    fichier_json=os.path.join(dossier_json,"pokemon.json")
    with open(fichier_json, "w", encoding="utf-8") as f:
        json.dump(liste_dict, f, ensure_ascii=False, indent=2, separators=(",", ":"))
    print(len(liste_dict)," pokemons exportes vers pokedex/docs/fichier_json")