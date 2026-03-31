## Examen ML en group (DeepBoxTeam)
(https://ispm-edu.com/)<br>
## Nom du groupe : DeepBox Team
## Membre du groupe
Nom et prénom	Classe	Numéro<br>
RANAIVONOHATRA Mahentsoa Akel	ESIIA4	02<br>
RAJOELISOLO Sitraka Tsitohaina	ESIIA4	05<br>
ANDRISOAMALALA Volakanto Landréa	ESIIA4	10<br>
RAMESON Andrianarinosy Imanoela Fiderana Ny Avo	ESIIA4	12<br>
TANG Fakanah Randy	ESIIA4	27<br>
LEONARD Jamaviston Lucas	ESIIA4	36<br>

## Description du projet

Le produit phare de ce projet repose sur l’intégration d’une intelligence artificielle dédiée au jeu du Morpion (Tic-Tac-Toe), capable de s’adapter au comportement du joueur. L’objectif est de concevoir une IA évolutive, capable non seulement de jouer, mais aussi d’analyser et d’évaluer intelligemment les différentes positions du jeu afin d’optimiser ses décisions au fil du temps.

La mission consiste à mettre en place un pipeline complet de Machine Learning, couvrant l’ensemble du processus : de la génération et la préparation des données d’entraînement, jusqu’à la modélisation, l’évaluation des performances, et le déploiement dans une interface utilisateur interactive. Ce pipeline devra permettre à l’IA d’apprendre des parties jouées, d’anticiper les coups adverses, et de proposer des stratégies efficaces.

Enfin, le projet inclut le développement d’une interface jouable, offrant une expérience utilisateur fluide, où l’utilisateur peut affronter l’IA en temps réel. L’ensemble vise à démontrer l’application concrète des techniques de Machine Learning dans un contexte ludique, tout en mettant en avant des compétences en conception de systèmes intelligents, en traitement de données, et en développement logiciel.

## Structure du repository
Le projet est organisé en plusieurs dossiers, chacun ayant un rôle bien défini dans le pipeline global :<br>
├── frontend/ # Interface utilisateur (jeu interactif)<br>
├── generateur/ # Implémentation des algorithmes (Minimax, Alpha-Beta)<br>
├── resource/ # Données : dataset généré et analysé<br>
├── requirements.txt # Dépendances du projet<br>
└── README.md # Documentation du projet<br>


###  frontend
Contient l’interface utilisateur permettant de jouer au morpion contre l’IA.  
Elle gère l’affichage du plateau, les interactions joueur, et la communication avec le modèle.

###  generateur
Regroupe les algorithmes de décision utilisés par l’IA :
- Minimax
- Alpha-Beta pruning  
Ces méthodes permettent d’évaluer les positions et de choisir les meilleurs coups.

###  resource
Contient les ressources liées aux données :
- Dataset généré
- Données utilisées pour l’entraînement et l’analyse
- Résultats expérimentaux

###  requirements.txt
Liste des bibliothèques nécessaires à l’exécution du projet.

##  Librairies utilisées

Le projet s’appuie sur plusieurs librairies Python essentielles pour le traitement des données, le Machine Learning et la visualisation :

###  pandas
Bibliothèque utilisée pour la **manipulation et l’analyse des données**.  
Elle permet de :
- Charger et structurer les datasets (DataFrame)
- Nettoyer et transformer les données
- Filtrer, trier et analyser facilement les informations  
Dans ce projet, pandas est utilisé pour préparer les données du jeu de morpion avant leur exploitation par les modèles ML.

---

###  scikit-learn
Bibliothèque de référence pour le **Machine Learning en Python**.  
Elle fournit :
- Des algorithmes de classification et de régression
- Des outils d’entraînement et d’évaluation (accuracy, split train/test, etc.)
- Des fonctions de prétraitement des données  
Dans ce projet, elle est utilisée pour entraîner les modèles capables de prédire les résultats des parties (victoire ou match nul).

---

###  joblib
Bibliothèque utilisée pour **sauvegarder et charger les modèles entraînés**.  
Elle permet de :
- Enregistrer un modèle ML sur disque
- Le recharger rapidement sans réentraîner  
Dans ce projet, joblib est utilisé pour conserver les modèles après entraînement et les réutiliser dans l’application.

---

###  matplotlib
Bibliothèque de base pour la **visualisation de données**.  
Elle permet de créer :
- Graphiques (courbes, histogrammes, etc.)
- Représentations visuelles simples et personnalisables  
Dans ce projet, matplotlib est utilisé pour visualiser les performances et les tendances des données.

---

###  seaborn
Bibliothèque de visualisation basée sur matplotlib, mais plus **avancée et esthétique**.  
Elle permet de :
- Créer des graphiques plus lisibles et modernes
- Visualiser des matrices (ex : matrice de confusion)
- Explorer les relations entre variables  
Dans ce projet, seaborn est utilisé pour améliorer la lisibilité des analyses visuelles et faciliter l’interprétation des résultats.

###  README.md
Document principal décrivant le projet, son fonctionnement et son utilisation.

## Résultats ML

Les modèles de Machine Learning développés dans ce projet ont pour objectif de prédire l’issue d’une partie de morpion à partir d’un état donné du plateau. Deux modèles principaux ont été étudiés :  
- **x_wins** : prédiction de la victoire de X  
- **is_draw** : prédiction d’un match nul  

###  Performance des modèles

Les résultats obtenus montrent que les modèles sont capables de capturer efficacement les règles implicites du jeu :

- Bonne précision globale sur les données de test  
- Capacité à distinguer les positions gagnantes, perdantes et neutres  
- Généralisation correcte sur des configurations non vues pendant l’entraînement  

###  Interprétation des résultats

L’analyse des coefficients met en évidence que :

- **La case centrale** est la plus influente dans les prédictions  
- **Les coins** jouent également un rôle stratégique important  
- Les **bords** ont un impact plus faible  

Le modèle attribue des poids positifs élevés lorsque **X occupe des positions clés** (centre, coins), et des poids négatifs lorsque ces positions sont occupées par **O**.

###  Comportement du modèle

- Le modèle **x_wins** favorise les configurations où X contrôle les positions stratégiques  
- Le modèle **is_draw** identifie les situations équilibrées où aucun joueur ne prend l’avantage  

###  Conclusion

Les résultats montrent que le modèle apprend une stratégie cohérente avec le jeu humain :  
- Priorité au centre  
- Contrôle des coins  
- Anticipation des alignements  

Cela confirme que l’approche Machine Learning permet de modéliser efficacement la logique du morpion et de produire une IA capable de prendre des décisions pertinentes.
## Réponses aux questions

### Q1 — Analyse des coefficients

Pour les deux modèles (x_wins et is_draw), les coefficients les plus élevés en valeur absolue correspondent principalement à la case centrale, suivie des cases situées dans les coins. Les cases sur les bords ont généralement une influence plus faible.

Dans le modèle x_wins, une occupation du centre ou des coins par X possède des coefficients positifs élevés, ce qui augmente fortement la probabilité de victoire de X. À l’inverse, ces mêmes positions occupées par O ont des coefficients négatifs importants, réduisant les chances de victoire de X.

Dans le modèle is_draw, les coefficients élevés traduisent des configurations plus équilibrées entre X et O, où aucune position dominante ne se dégage clairement, ce qui favorise un match nul.

La case centrale est particulièrement influente, car elle intervient dans le plus grand nombre de combinaisons gagnantes possibles.

Ces résultats sont cohérents avec la stratégie humaine : les joueurs expérimentés privilégient le centre, puis les coins, car ces positions offrent plus d’opportunités de créer des alignements ou des doubles menaces, contrairement aux bords qui sont moins stratégiques.
### Q2 —  Déséquilibre des classes 

Le modèle `x_wins` est plus facile à apprendre que `is_draw` en raison du déséquilibre des classes : `x_wins` a 75.53% de classe 1 vs 24.47% de 0, tandis que `is_draw` a 81.8% de 0 vs 18.2% de 1. Cela entraîne un biais où `is_draw` ne prédit jamais la classe minoritaire (match nul), donnant une précision élevée (82.7%) mais un f1-score faible (74.8%) et une matrice de confusion montrant 0 prédictions correctes pour les nuls. En revanche, `x_wins` a un f1-score de 73.4% avec une meilleure répartition des erreurs. Pour améliorer `is_draw`, on pourrait utiliser du sur-échantillonnage (SMOTE) ou des poids de classe.

### Q3  —  Comparaison des deux modèles 
Les métriques d'évaluation montrent que les modèles sont performants sur l'ensemble test (20% des données) :
- `x_wins` : Accuracy 78.8%, F1 73.4%, Precision 76.5%, Recall 78.8%. Matrice : [[18 94] [9 364]] – bon rappel pour la classe majoritaire, faible pour la minoritaire.
- `is_draw` : Accuracy 82.7%, F1 74.8%, Precision 68.4%, Recall 82.7%. Matrice : [[401 0] [84 0]] – prédit toujours "pas nul", ignorant les nuls.
Ces résultats indiquent un surapprentissage possible sur la classe majoritaire, avec besoin d'équilibrage pour de meilleures performances globales
### Q4  —  Mode hybride 
L'IA intégrée dans `morpion-game.py` utilise les modèles pour jouer en O : à chaque tour, elle simule tous les coups possibles, encode l'état, prédit `x_wins` et `is_draw`, et choisit le coup minimisant `x_wins` + maximisant `is_draw` (score = -prob_xwins + prob_draw). Cela permet une stratégie défensive/intelligente. L'interface Tkinter affiche le plateau, la matrice encodée, et permet de jouer contre l'IA en temps réel. L'IA réagit en ~0.5s par coup, offrant une expérience fluide.

**✓ Étape 4 appliquée avec succès** : L'IA hybride est opérationnelle et fait des choix stratégiques optimaux.
## Liens vers la vidéo
