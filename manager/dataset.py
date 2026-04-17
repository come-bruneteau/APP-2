import csv
import random
import os
 
class Dataset:

#mode fichier csv

    def __init__(self, name, file_path=None, nb_joueurs=10, prix_max=20):
        self.name = name
        self.data = []
 
        if file_path:

            if not file_path.endswith('.csv'):
                raise ValueError("File path must end with '.csv'")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Fichier introuvable : {file_path}")
            
            with open(file_path, 'r') as f:
                self.data = list(csv.reader(f, delimiter=','))
        else:
            self.data = self._generer(nb_joueurs, prix_max)

        
    #mode génération aléatoire

    def _generer(self, nb_joueurs, prix_max):
        """Génère données aléatoire, chaque joueur propose un prix entier."""
        data = []
        for i in range(nb_joueurs):
            joueur = f"Joueur_{i+1}"
            prix = random.randint(0, prix_max)
            data.append([joueur, str(prix)])
        return data
 
    def sauvegarder_csv(self, file_path):
        """Sauvegarde le jeu de données généré dans un fichier CSV."""
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)
        print(f"Données sauvegardés dans : {file_path}")
 
    def __len__(self):
        return len(self.data)