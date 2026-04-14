from manager.ABR import ABR

class EnchereLowBid:
    def __init__(self, cout_base=1.0, alpha=10.0):
        self.cout_base = cout_base
        self.alpha = alpha  # Intensité de la prime de risque
        self.abr = ABR()
        self.recette_vendeur = 0.0
        self.depenses_joueurs = {}
        self.total_mises = 0

    def calculer_cout(self, prix):
        """Formule de référence pour la prime de risque"""
        return self.cout_base + (self.alpha / (prix + 1))

    def enregistrer_mise(self, joueur, prix):
        prix = int(prix)
        
        # Insertion dans l'ABR
        self.abr.inserer(prix, joueur)
        self.total_mises += 1
        
        # Calcul des coûts
        cout = self.calculer_cout(prix)
        self.recette_vendeur += cout
        
        if joueur in self.depenses_joueurs:
            self.depenses_joueurs[joueur] += cout
        else:
            self.depenses_joueurs[joueur] = cout

    def determiner_gagnant(self):
        """Retourne le gagnant et gère le cas où il n'y a pas de gagnant"""
        prix_gagnant, joueur_gagnant = self.abr.rechercher_plus_bas_unique()
        return prix_gagnant, joueur_gagnant

    def generer_rapport(self):
        prix_g, joueur_g = self.determiner_gagnant()
        
        rapport = f"--- RESULTATS DE L'ENCHERE ---\n"
        rapport += f"Total des mises : {self.total_mises}\n"
        rapport += f"Recette du vendeur : {self.recette_vendeur:.2f} €\n"
        
        if joueur_g:
            rapport += f"GAGNANT : {joueur_g} avec l'offre de {prix_g} €\n"
        else:
            rapport += "AUCUN GAGNANT : Tous les prix ont été proposés plusieurs fois.\n"
            
        return rapport