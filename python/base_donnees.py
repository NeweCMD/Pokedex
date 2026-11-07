import sqlite3
from requetes_api import recuperer_pokemon,extraire_infos
import time


NOM_FICHIER_BASE = "mes_pokemon.db"

def connecter():
    'permet de connecter le code avec la base de données dans "NOM_FICHIER_BASE" ici "mes_pokemon.db".'
    connec = sqlite3.connect(NOM_FICHIER_BASE)
    connec.row_factory = sqlite3.Row
    connec.execute("PRAGMA foreign_keys = ON")
    return connec

def creer_table():
    'fait la requête SQL pour que la base de données "mes_pokemon.db" ait la table pokemon avec tous ses champs avec leur type.'
    with connecter() as connec:
        connec.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL UNIQUE,
        type_1 TEXT,
        type_2 TEXT,
        hp INTEGER NOT NULL,
        attaque INTEGER NOT NULL,
        defense INTEGER NOT NULL,
        sp_attaque INTEGER NOT NULL,
        sp_defense INTEGER NOT NULL,
        vitesse INTEGER NOT NULL,
        taille REAL NOT NULL,
        poids REAL NOT NULL,
        sprite_avant TEXT,
        sprite_arriere TEXT,
        cri TEXT
        )""")


def enregistrer_pokemon(infos_pokemon):
        'permet de rajouter un pokemon dans la bdd en utilisant les informations de la fonction extraire_infos'
        if infos_pokemon!= None:
            with connecter() as connec:
                connec.execute(
                    """INSERT OR REPLACE INTO pokemon (id,nom,type_1,type_2,hp,attaque,defense,sp_attaque,sp_defense,vitesse,taille,poids,sprite_avant,sprite_arriere,cri)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                    infos_pokemon["id"],
                    infos_pokemon["nom"],
                    infos_pokemon["types"][0],
                    infos_pokemon["types"][1] if len( infos_pokemon["types"] )>1 else None,
                    infos_pokemon["stats"]["hp"],
                    infos_pokemon["stats"]["attack"],
                    infos_pokemon["stats"]["defense"],
                    infos_pokemon["stats"]["special-attack"],
                    infos_pokemon["stats"]["special-defense"],
                    infos_pokemon["stats"]["speed"],
                    infos_pokemon["taille"],
                    infos_pokemon["poids"],
                    infos_pokemon["sprite_avant"],
                    infos_pokemon["sprite_arriere"],
                    infos_pokemon["cri"],
                    ),
                )

def recherche_poke_nom(nom_pokemon):
    'fait la requête SQL pour trouver un pokemon avec son nom si il est dans la BDD, renvoi un sqlite3.Row object et donc à utiliser avec la fonction dict()'
    with connecter() as connec:
          ligne=connec.execute(
               """SELECT * FROM pokemon WHERE nom = ?""",
               (
                    nom_pokemon.lower().strip(),
                )
          ).fetchone()
    return ligne

def recherche_poke_nom_partiel(nom_pokemon_partiel):
    'fait la requête SQL pour trouver un pokemon avec son nom si il est dans la BDD, renvoi une liste de sqlite3.Row object et donc à utiliser avec la fonction dict()[0]'
    with connecter() as connec:
          liste_ligne=connec.execute(
               """SELECT * FROM pokemon WHERE nom LIKE ?
               ORDER BY id
               LIMIT 20""",
               (
                  nom_pokemon_partiel.lower().strip() + "%",
                )
          ).fetchall()
    return liste_ligne

def chercher_par_criteres(type_1=None, type_2=None, hp=0,attaque=0,defense=0,sp_attaque=0,sp_defense=0,vitesse=0,taille=0.0,poids=0.0):
    'fait la requête SQL pour trouver des pokemons dans la BDD avec certains critères, renvoi une liste de sqlite3.Row object et donc à utiliser avec la fonction dict() sur chaque élément de la liste'
    valeurs_retenues= []
    condition_retenues= []
    if type_1 != None:
          valeurs_retenues.append(type_1)
          valeurs_retenues.append(type_1)
          condition_retenues.append("(type_1 = ? OR type_2 = ?)")
    if type_2 != None:
          valeurs_retenues.append(type_2)
          valeurs_retenues.append(type_2)
          condition_retenues.append("(type_2 = ? OR type_1 = ?)")          
    if hp != 0:
          valeurs_retenues.append(hp)
          condition_retenues.append("hp >= ?")
    if attaque != 0:
          valeurs_retenues.append(attaque)
          condition_retenues.append("attaque >= ?")
    if defense != 0:
          valeurs_retenues.append(defense)
          condition_retenues.append("defense >= ?")
    if sp_attaque != 0:
          valeurs_retenues.append(sp_attaque)
          condition_retenues.append("sp_attaque >= ?")
    if sp_defense != 0:
          valeurs_retenues.append(sp_defense)
          condition_retenues.append("sp_defense >= ?")
    if vitesse != 0:
          valeurs_retenues.append(vitesse)
          condition_retenues.append("vitesse >= ?")
    if taille != 0.0:
          valeurs_retenues.append(taille)
          condition_retenues.append("taille >= ?")
    if poids != 0.0:
          valeurs_retenues.append(poids) 
          condition_retenues.append("poids >= ?") 

    requete_sql="SELECT * FROM pokemon"
    if len(condition_retenues)>0:
        requete_sql += " WHERE "
        requete_sql += " AND ".join(condition_retenues)
    requete_sql += " ORDER BY id "        
    with connecter() as connec:
        return connec.execute(requete_sql,valeurs_retenues).fetchall()
           



"""*****************************************************partie création d'équipe*******************************************"""

def creer_table_equipe():
    'fait la requête SQL pour que la base de données "mes_pokemon.db" ait la table equipe avec tous ses champs avec leur type.'
    with connecter() as connec:
      connec.execute("""
      CREATE TABLE IF NOT EXISTS equipe (
      placement INTEGER PRIMARY KEY CHECK (placement BETWEEN 1 AND 6),
      id_pokemon INTEGER NOT NULL,
      FOREIGN KEY (id_pokemon) REFERENCES pokemon(id)
      )""")

def ajouter_equipe(pokemon_id):
      """permet de rajouter un pokemon dans la BDD equipe si elle n'est pas pleine (doublons autorisé)"""
      with connecter() as connec:
            ligne=connec.execute("""SELECT placement FROM equipe""").fetchall()
            places_prises=[]
            for elt in ligne:
                  places_prises.append(elt["placement"]) 
            try:
                  for i in range(1,7):
                        if i not in places_prises:
                              connec.execute("""INSERT INTO equipe (placement, id_pokemon)
                              VALUES(?,?)""",
                                    (
                                    i,
                                    pokemon_id
                                    )
                              )
                              return True
                  return False
            except sqlite3.IntegrityError:
                 return False

def retire_equipe(placement):
      """permet de retirer le pokemon dans la BDD equipe si l'emplacement n'est pas vide"""
      with connecter() as connec:
           connec.execute("""DELETE FROM equipe WHERE placement = ?""",
           (
            placement,    
           )
           )

def lire_equipe():
      """permet de récuperer la liste des membres de l'équipe avec leurs informations"""
      with connecter() as connec:
            equipe=connec.execute("""SELECT placement,pokemon.id,nom,sprite_avant 
            FROM equipe JOIN pokemon ON equipe.id_pokemon = pokemon.id ORDER BY equipe.placement""").fetchall()
      return equipe

if __name__ == "__main__":
      creer_table()
      print("**************************** gestion d'équipe ************************************")


      creer_table_equipe()
      for i in range(1,7):
           retire_equipe(i)
      print(ajouter_equipe(555))
      print(ajouter_equipe(666))
      print(ajouter_equipe(6666))
      eq=lire_equipe()
      for elt in eq:
           print(dict(elt))