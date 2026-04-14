# Projet APP 2 - Algorithmique Avancée 3 : Moteur d'Enchères "LowBid"

## 📝 Contexte du Projet
Ce projet s'inscrit dans le cadre de l'Apprentissage Par Problème (APP) du module Algorithmique Avancée 3. 

L'objectif est de développer le moteur d'enchères inversées pour la startup **LowBid**. Le principe du jeu est simple : **le plus bas prix unique gagne**. 
Pour éviter que tous les joueurs ne misent 0 €, une "prime de risque" est appliquée : plus la mise est basse, plus elle coûte cher. Le coût d'une mise est calculé via la formule : 
$cout\_mise(prix) = cout\_base + a/(prix+1)$

## 📂 Structure du Projet
Le projet est organisé de manière modulaire afin de séparer la logique de la structure de données, les règles de l'enchère et l'exécution :

```text
APP2
│
├── assets/                 # Jeux de données au format CSV
│   ├── lowbid_manche_demo.csv
│   ├── lowbid_multi_manches_500x40.csv
│   └── lowbid_stress_200k.csv
│
├── manager/                # Coeur logique de l'application
│   ├── ABR.py                 # Implémentation de l'Arbre Binaire de Recherche
│   ├── dataset.py             # Gestion et chargement des fichiers CSV
│   └── enchere.py             # Règles de l'enchère et calculs financiers
│
├── main.py                    # Script principal : exécution d'une manche de démonstration
├── simulation.py              # Script de simulation : 500 manches et test de stratégies
└── README.md                  # Documentation du projet
```

## 🚀 Utilisation
Assurez-vous d'avoir Python 3 installé sur votre machine. Aucune bibliothèque externe n'est requise.

### 1. Lancer une manche de démonstration :
Ce script lit le fichier `lowbid_manche_demo.csv`, insère les mises dans l'ABR, affiche l'arbre trié et donne le gagnant ainsi que la recette du vendeur.

```bash
python main.py
```

### 2. Lancer la simulation multi-manches :
Ce script simule 500 manches avec 40 joueurs répartis en trois stratégies différentes (Aléatoire, Spammeur, Stratège) pour analyser la viabilité économique du modèle.

```bash
python simulation.py
```

## 🧠 Choix Techniques & Algorithmiques
### L'Arbre Binaire de Recherche (ABR)
La structure de données centrale de ce projet est un **ABR personnalisé** (interdiction d'utiliser le tri natif de Python).
* **Gestion des doublons :** Chaque nœud de l'arbre représente un prix. Si plusieurs joueurs misent le même prix, ils sont ajoutés à une liste au sein du même nœud.
* **Tri naturel :** Un parcours infixe (gauche, nœud, droite) permet d'obtenir la liste des mises triées de manière croissante.
* **Recherche du gagnant :** La recherche du plus bas prix unique se fait récursivement en privilégiant le sous-arbre gauche, puis le nœud courant, puis le sous-arbre droit.

### Limites et Complexité
* **Cas moyen :** L'insertion et la recherche s'effectuent en $O(\log n)$.
* **Pire cas (Dégénérescence) :** Si les mises sont insérées dans un ordre déjà trié (ex: 1, 2, 3, 4...), l'ABR dégénère en une liste chaînée et la complexité chute à $O(n)$. Pour un environnement de production réel avec un flux continu, un arbre auto-équilibré (comme un arbre AVL ou Rouge-Noir) serait une évolution nécessaire.

## 📊 Analyse Stratégique
La simulation de 500 manches a permis de tester 3 profils de joueurs :

1. **Le Spammeur (Mise de 0 à 2) :** Perdant. Les spammeurs s'annulent mutuellement en créant des doublons, et la prime de risque draine leurs fonds.
2. **L'Aléatoire (Mise de 0 à 50) :** Maintient un taux de victoire modéré mais manque d'optimisation.
3. **Le Stratège (Mise de 3 à 8) :** Gagnant. En évitant la zone de forte collision (0-2), il trouve souvent un prix unique tout en minimisant l'impact de la prime de risque.

Côté vendeur, le modèle "LowBid" est validé : la prime de risque assure une recette moyenne par manche largement supérieure à la valeur intrinsèque de l'objet mis en jeu.

## Organisation au sein de l'équipe

|Membre|Rôle|Responsabilité|
|:--|---|:--|
|Sam Vautier|Responsable Algorithmique et Structure de Données|Implémenter la classe ABR et la gestion des noeuds|
|Côme Bruneteau|Développeur Logique Métier et Simulation|Coder l'algorithme de recherche du plus bas prix unique|
|Ruben Vogel-Lucas|Analyste de Données et Performance|Gérer le  chargement des données (fichier CSV) ou la génération de données de test.|
|Arthur Roubinet|Responsable Intégration, IHM et Rapport|Développer l'interface permettant aux humains de jouer contre l'ordinateur|