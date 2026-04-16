import time
from manager.dataset import Dataset
from manager.enchere import EnchereLowBid
from simulation import simuler_multi_manches

assets = [
    "assets/lowbid_stress_200k.csv",
    # "assets/lowbid_multi_manches_500x40.csv",
    # "assets/lowbid_manche_demo.csv"
]

def lancer_enchere(dataset):
    """Lance une manche d'enchère à partir d'un dataset."""
    enchere = EnchereLowBid(cout_base=1.0, alpha=10.0)

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


def menu():
    print("=" * 15)
    print("    LOWBID    ")
    print("=" * 15)
    print("\nComment voulez-vous jouer ?")
    print("  1. Lancer un stresstest")
    print("  2. Générer une manche aléatoire")
    print("  3. Lancer la simulation multi-manches (500 manches)")
    print("  0. Quitter")
    print()

    choix = input("Votre choix : ").strip()

    if choix == "1":
        print(f"\nFichier utilisé : {assets[0]}")
        try:
            dataset = Dataset(name="Demo Manche", file_path=assets[0])
            dataset.afficher_apercu()

            debut = time.time()
            lancer_enchere(dataset)
            fin = time.time()
            print(f"Temps de calcul : {fin - debut:.3f} secondes")

        except FileNotFoundError as e:
            print(f"Erreur : {e}")

    elif choix == "2":
        # L'utilisateur choisit la taille de la manche, avec des valeurs par défaut si vide
        try:
            nb_joueurs = int(input("Nombre de joueurs aléatoires (défaut 10) : ").strip() or "10")
            prix_max = int(input("Prix maximum (défaut 20) : ").strip() or "20")
        except ValueError:
            print("Valeur invalide, utilisation des valeurs par défaut.")
            nb_joueurs, prix_max = 10, 20

        dataset = Dataset(name="Manche Aléatoire", nb_joueurs=nb_joueurs, prix_max=prix_max)
        dataset.afficher_apercu()

        debut = time.time()
        lancer_enchere(dataset)
        fin = time.time()
        print(f"Temps de calcul : {fin - debut:.3f} secondes")

    elif choix == "3":
        try:
            nb_manches = int(input("Nombre de manches (défaut 500) : ").strip() or "500")
            alpha = float(input("Valeur d'alpha (défaut 10.0) : ").strip() or "10.0")
        except ValueError:
            print("Valeur invalide, utilisation des valeurs par défaut.")
            nb_manches, alpha = 500, 10.0

        simuler_multi_manches(nb_manches=nb_manches, nb_joueurs=40, alpha=alpha)

    elif choix == "0":
        print("Au revoir !")
        return

    else:
        print("Choix invalide.")

    # Retour automatique au menu après chaque action
    print()
    menu()


if __name__ == "__main__":
    menu()