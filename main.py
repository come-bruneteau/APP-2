from manager.dataset import Dataset
from manager.enchere import EnchereLowBid

assets = [
    "assets/lowbid_manche_demo.csv",
    # "assets/lowbid_multi_manches_500x40.csv", # A décommenter pour la partie simulation
    # "assets/lowbid_stress_200k.csv"
]

try:
    dataset_demo = Dataset(name="Demo Manche", file_path=assets[0])
    
    # Initialisation de l'enchère avec cout_base=1 et alpha=10
    enchere = EnchereLowBid(cout_base=1.0, alpha=10.0)
    
    # Simulation : on lit les données et on enregistre les mises
    # On suppose que le CSV n'a pas d'en-tête et est au format: joueur, prix
    for ligne in dataset_demo.data:
        if len(ligne) >= 2:
            joueur = ligne[0].strip()
            valeur_prix = ligne[1].strip()
            
            # On gère l'erreur au cas où la ligne contient du texte (comme l'en-tête "prix")
            try:
                prix = int(valeur_prix)
                enchere.enregistrer_mise(joueur, prix)
            except ValueError:
                # C'est probablement l'en-tête, on l'ignore simplement
                continue
            
    # Affichage du parcours infixe pour vérifier la répartition
    print("--- ETAT DE L'ABR (Prix triés) ---")
    etat = enchere.abr.parcours_infixe()
    for prix, joueurs in etat:
        print(f"Prix {prix} : {len(joueurs)} mise(s) par {joueurs}")
    
    print("\n" + enchere.generer_rapport())

except Exception as e:
    print(f"Erreur lors de l'exécution : {e}")