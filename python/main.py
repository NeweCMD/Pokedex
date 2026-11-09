import base_donnees as bd 
import requetes_api as rapi 
import time

def obtenir_pokemon(nom):
    '''permet de récuperer les informations d un pokemon, renvoi un sqlite3.Row object et donc à utiliser avec la fonction dict(), ou None si le pokémon est inexistant,
    affiche aussi si le pokémon était deja dans la BDD ou pas, si il ne l était pas alors il est ajouté dans la BDD.'''
    poke = bd.recherche_poke_nom(nom)
    if poke != None:
        print("ce pokemon vient de la BDD")
        return poke
    else :
        poke = rapi.extraire_infos(rapi.recuperer_pokemon(nom))
        if poke != None:
            bd.enregistrer_pokemon(poke)
            poke = bd.recherche_poke_nom(nom)
            print("ce pokemon vient de l'API")
            return poke
        else:
            print("ce pokemon n'existe pas")
            return None

def telecharger_catalogue(limite=20):
    '''telecharge dans la BDD tous les pokémons de l api et leurs differentes formes, à ne lancer que une fois au debut,
    le compteur ne marche pas si il y a deja des pokemon dans la BDD, 
    limite corresponds au nombre de pokemon que l'on veut telecharger avec leur differentes formes (1351), renvoie à la fin le nombre de pokemon telecharges et les potentielles erreurs'''
    bd.creer_table()
    bd.creer_table_equipe()
    nb_none= 0
    liste_nom=rapi.recup_liste_nom(limite)
    for pos,elt in enumerate(liste_nom,start=1):
        if bd.recherche_poke_nom(elt) == None:
            print(pos, " / ", limite, elt)
            poke = obtenir_pokemon(elt)
            if poke == None:
                nb_none += 1
            time.sleep(0.2)
    return (limite-nb_none," telecharges", nb_none," echecs")
            
if __name__=="__main__":
    print("****************************** obtenir_pokemon **********************************")
    print(dict(obtenir_pokemon("Mewtwo")))
    print("****************************** telecharger_catalogue **********************************")
    print(telecharger_catalogue(1351))
