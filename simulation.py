import random
from manager.enchere import EnchereLowBid

def simuler_multi_manches(nb_manches=500, nb_joueurs=40, alpha=10.0):
    print(f"\n=== LANCEMENT DE LA SIMULATION ({nb_manches} manches, alpha={alpha}) ===")
    
    # Statistiques globales
    victoires = {"Aleatoire": 0, "Spammeur": 0, "Stratege": 0}
    depenses_totales = {"Aleatoire": 0.0, "Spammeur": 0.0, "Stratege": 0.0}
    recette_vendeur_totale = 0.0
    valeur_gain_moyen = 100.0 # On suppose que l'objet gagné vaut 100€

    # Répartition des joueurs (ex: 40 joueurs divisés en 3 stratégies)
    joueurs_par_strat = nb_joueurs // 3

    for manche in range(nb_manches):
        enchere = EnchereLowBid(cout_base=1.0, alpha=alpha)
        
        # Chaque joueur fait sa mise selon sa stratégie
        for i in range(nb_joueurs):
            if i < joueurs_par_strat:
                strategie = "Aleatoire"
                prix = random.randint(0, 50) # Joue au hasard
            elif i < 2 * joueurs_par_strat:
                strategie = "Spammeur"
                prix = random.randint(0, 2)  # Vise systématiquement le fond
            else:
                strategie = "Stratege"
                prix = random.randint(3, 8)  # Évite les 0-2 (trop contestés) et vise juste au-dessus
            
            # Format du nom pour retrouver la stratégie à la fin: "Stratege_25"
            nom_joueur = f"{strategie}_{i}"
            enchere.enregistrer_mise(nom_joueur, prix)
            
            # Suivi des dépenses des joueurs
            depenses_totales[strategie] += enchere.calculer_cout(prix)

        # Bilan de la manche
        recette_vendeur_totale += enchere.recette_vendeur
        prix_gagnant, joueur_gagnant = enchere.determiner_gagnant()
        
        if joueur_gagnant:
            nom_strategie = joueur_gagnant.split('_')[0]
            victoires[nom_strategie] += 1

    # --- AFFICHAGE DES RÉSULTATS ---
    print(f"Recette moyenne du vendeur par manche : {recette_vendeur_totale / nb_manches:.2f} €")
    print("\n--- PERFORMANCES DES STRATÉGIES ---")
    
    for strat in victoires.keys():
        taux_victoire = (victoires[strat] / nb_manches) * 100
        depense_moyenne_par_manche = (depenses_totales[strat] / joueurs_par_strat) / nb_manches
        
        # Gain = (Valeur de l'objet * nb_victoires) - (Total dépensé par ce groupe) 
        # divisé par le nombre de joueurs appliquant cette stratégie
        gain_net_moyen = ((valeur_gain_moyen * victoires[strat]) - depenses_totales[strat]) / joueurs_par_strat
        
        print(f"[{strat.upper()}]")
        print(f"  Taux de victoire : {taux_victoire:.1f}%")
        print(f"  Coût moyen par mise : {depense_moyenne_par_manche:.2f} €")
        print(f"  Bilan financier net (gain moyen par joueur) : {gain_net_moyen:.2f} €\n")

# Lancement de la simulation après la manche de démonstration
if __name__ == "__main__":
    simuler_multi_manches(nb_manches=500, nb_joueurs=40, alpha=10.0)