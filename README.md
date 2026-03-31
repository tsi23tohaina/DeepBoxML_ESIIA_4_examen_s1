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
Le projet est organisé en plusieurs dossiers, chacun ayant un rôle bien défini dans le pipeline global :
├── frontend/ # Interface utilisateur (jeu interactif)
├── generateur/ # Implémentation des algorithmes (Minimax, Alpha-Beta)
├── resource/ # Données : dataset généré et analysé
├── requirements.txt # Dépendances du projet
└── README.md # Documentation du projet

### frontend/
Contient l’interface utilisateur permettant de jouer au morpion contre l’IA.  
Elle gère l’affichage du plateau, les interactions joueur, et la communication avec le modèle.

### generateur/
Regroupe les algorithmes de décision utilisés par l’IA :
- Minimax
- Alpha-Beta pruning  
Ces méthodes permettent d’évaluer les positions et de choisir les meilleurs coups.

### resource/
Contient les ressources liées aux données :
- Dataset généré
- Données utilisées pour l’entraînement et l’analyse
- Résultats expérimentaux

### requirements.txt
Liste des bibliothèques nécessaires à l’exécution du projet.

### README.md
Document principal décrivant le projet, son fonctionnement et son utilisation.

## Résultats ML
## Réponses aux questions

## Q1 — Analyse des coefficients

Pour les deux modèles (x_wins et is_draw), les coefficients les plus élevés en valeur absolue correspondent principalement à la case centrale, suivie des cases situées dans les coins. Les cases sur les bords ont généralement une influence plus faible.

Dans le modèle x_wins, une occupation du centre ou des coins par X possède des coefficients positifs élevés, ce qui augmente fortement la probabilité de victoire de X. À l’inverse, ces mêmes positions occupées par O ont des coefficients négatifs importants, réduisant les chances de victoire de X.

Dans le modèle is_draw, les coefficients élevés traduisent des configurations plus équilibrées entre X et O, où aucune position dominante ne se dégage clairement, ce qui favorise un match nul.

La case centrale est particulièrement influente, car elle intervient dans le plus grand nombre de combinaisons gagnantes possibles.

Ces résultats sont cohérents avec la stratégie humaine : les joueurs expérimentés privilégient le centre, puis les coins, car ces positions offrent plus d’opportunités de créer des alignements ou des doubles menaces, contrairement aux bords qui sont moins stratégiques.
## Q2
## Q3
## Q4
## Liens vers la vidéo
