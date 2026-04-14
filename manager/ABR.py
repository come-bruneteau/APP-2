class Noeud:
    """Représente un prix unique dans l'enchère."""
    def __init__(self, prix, joueur):
        self.prix = prix  # On stocke les joueurs dans une liste pour gérer les doublons de prix 
        self.joueurs = [joueur]
        self.gauche = None
        self.droite = None



class ABR:
    """Structure principale pour gérer les mises dynamiquement[cite: 74, 102]."""
    """ installation des def de l'ABR """
    def __init__(self):
        self.racine = None


    def inserer(self, prix, joueur):
        """Insère une mise dans l'ABR."""
        if self.racine is None:
            self.racine = Noeud(prix, joueur)
        else:
            self._inserer_recursif(self.racine, prix, joueur)


    def _inserer_recursif(self, noeud, prix, joueur):
        if prix == noeud.prix:  # Si le prix existe déjà, on ajoute le joueur à la liste 
            noeud.joueurs.append(joueur)
        elif prix < noeud.prix:
            if noeud.gauche is None:
                noeud.gauche = Noeud(prix, joueur)
            else:
                self._inserer_recursif(noeud.gauche, prix, joueur)
        else:
            if noeud.droite is None:
                noeud.droite = Noeud(prix, joueur)
            else:
                self._inserer_recursif(noeud.droite, prix, joueur)


    def _parcours_infixe_recursif(self, noeud, resultats):
        if noeud:
            self._parcours_infixe_recursif(noeud.gauche, resultats)
            resultats.append((noeud.prix, noeud.joueurs))
            self._parcours_infixe_recursif(noeud.droite, resultats)


    def parcours_infixe(self):
        """Affiche l'état de l'enchère par prix triés."""
        resultats = []
        self._parcours_infixe_recursif(self.racine, resultats)
        return resultats


    def rechercher_successeur(self, prix):
        """Trouve le prix immédiatement supérieur présent dans l'arbre."""
        courant = self.racine
        successeur = None
        while courant:
            if prix < courant.prix:
                successeur = courant
                courant = courant.gauche
            else:
                courant = courant.droite
        return successeur


    def rechercher_predecesseur(self, prix):
        """Trouve le prix immédiatement inférieur présent dans l'arbre."""
        courant = self.racine
        predecesseur = None
        while courant:
            if prix > courant.prix:
                predecesseur = courant
                courant = courant.droite
            else:
                courant = courant.gauche
        return predecesseur

    def _rechercher_plus_bas_unique_recursif(self, noeud):
        if noeud is None:
            return None, None
        
        # 1. On cherche d'abord dans le sous-arbre gauche (les prix les plus petits)
        prix_gagnant, joueur_gagnant = self._rechercher_plus_bas_unique_recursif(noeud.gauche)
        if prix_gagnant is not None:
            return prix_gagnant, joueur_gagnant
        
        # 2. On vérifie le nœud courant (est-il unique ?)
        if len(noeud.joueurs) == 1:
            return noeud.prix, noeud.joueurs[0]
        
        # 3. S'il n'est pas unique, on cherche dans le sous-arbre droit
        return self._rechercher_plus_bas_unique_recursif(noeud.droite)

    def rechercher_plus_bas_unique(self):
        """Recherche le plus bas prix proposé par une seule personne."""
        return self._rechercher_plus_bas_unique_recursif(self.racine)