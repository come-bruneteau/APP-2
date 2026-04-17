import time
from manager.dataset import Dataset
from manager.enchere import EnchereLowBid
from simulation import simuler_multi_manches

assets = [
    "assets/lowbid_stress_200k.csv",
    # "assets/lowbid_multi_manches_500x40.csv",
    # "assets/lowbid_manche_demo.csv"
]


max_manche = 200

def lancer_enchere(dataset, alpha=10.0):
    """Lance une manche d'enchère à partir d'un dataset."""
    enchere = EnchereLowBid(cout_base=1.0, alpha=alpha)

    # On parcourt les lignes du dataset et on enregistre chaque mise dans l'ABR
    for ligne in dataset.data:
        if len(ligne) >= 2:
            joueur = ligne[0].strip()
            valeur_prix = ligne[1].strip()
            try:
                prix = int(valeur_prix)
                enchere.enregistrer_mise(joueur, prix)
            except ValueError:
                # Ignore les lignes invalides ou les en-têtes CSV
                continue

    # Parcours infixe = affichage des prix dans l'ordre croissant grâce à l'ABR
    print("\n--- ETAT DE L'ABR (Prix triés) ---")
    etat = enchere.abr.parcours_infixe()
    for prix, joueurs in etat:
        print(f"  Prix {prix} : {len(joueurs)} mise(s) par {joueurs}")

    print("\n" + enchere.generer_rapport())

    # on retourne le gagnant pour savoir si on doit rejouer
    prix_g, joueur_g = enchere.determiner_gagnant()
    return joueur_g is not None


#saisie parametre avk contraintes

def saisir_parametres():
    """Demande les paramètres et vérifie que prix_max est cohérent avec nb_joueurs."""
    try:
        nb_joueurs = int(input("Nombre de joueurs (défaut 10) : ").strip() or "10")
        prix_max = int(input("Prix maximum (défaut 20) : ").strip() or "20")
        alpha = float(input("Valeur d'alpha (défaut 10.0) : ").strip() or "10.0")
    except ValueError:
        print("Valeur invalide, utilisation des valeurs par défaut.")
        nb_joueurs, alpha = 10, 10.0
    return nb_joueurs, prix_max, alpha

    

#Menu


def menu():
    print("=" * 15)
    print("    LOWBID    ")
    print("=" * 15)
    print("\nComment voulez-vous jouer ?")
    print("  1. Lancer un stresstest")
    print("  2. Générer une partie aléatoire")
    print("  3. Lancer la simulation multi-manches (500 manches)")
    print("  0. Quitter")
    print()

    choix = input("Votre choix : ").strip()



#Choix 1


    if choix == "1":
        print(f"\nFichier utilisé : {assets[0]}")
        try:
            dataset = Dataset(name="Stress Test", file_path=assets[0])
            

            debut = time.time()
            lancer_enchere(dataset)
            fin = time.time()
            print(f"Temps de calcul : {fin - debut:.5f} secondes")

        except FileNotFoundError as e:
            print(f"Erreur : {e}")





#Choix 2

     

    elif choix == "2":
        nb_joueurs, prix_max, alpha = saisir_parametres()
 
        manche = 1
        gagnant_trouve = False
             
        debut = time.time()

        while not gagnant_trouve and manche <= max_manche:
            print(f"\n--- MANCHE {manche}/{max_manche} (alpha={alpha}) ---")
            dataset = Dataset(name=f"Manche {manche}", nb_joueurs=nb_joueurs, prix_max=prix_max)

            
            gagnant_trouve = lancer_enchere(dataset, alpha=alpha)
            
           
 
            if not gagnant_trouve and manche<max_manche :
                print(f"Aucun gagnant à la manche {manche}, on relance...")
                manche += 1
            elif not gagnant_trouve and manche==max_manche:
                print(f"Aucun gagnant à la manche {manche}")
                break
            
        # Bilan final
        if gagnant_trouve:
            print(f"\nGagnant trouvé après {manche} manche(s) ")
        else:
            print(f"\nAucun gagnant après {max_manche} manches.")
        fin = time.time()
        print(f"Temps de calcul : {fin - debut:.5f} secondes")




#Choix 3


    elif choix == "3":
        try:
            nb_manches = int(input("Nombre de manches (défaut 500) : ").strip() or "500")
            alpha = float(input("Valeur d'alpha (défaut 10.0) : ").strip() or "10.0")
        except ValueError:
            print("Valeur invalide, utilisation des valeurs par défaut.")
            nb_manches, alpha = 500, 10.0
        debut = time.time()
        simuler_multi_manches(nb_manches=nb_manches, nb_joueurs=40, alpha=alpha)
        fin = time.time()
        print(f"Temps de calcul : {fin - debut:.5f} secondes")
    elif choix == "0":
        print("Ciao")
        return

    else:
        print("Choix invalide.")


    # Retour automatique au menu après chaque action

    print()
    menu()




if __name__ == "__main__":
    menu()