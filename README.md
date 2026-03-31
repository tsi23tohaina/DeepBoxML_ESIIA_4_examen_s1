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

- `ressources/` : Contient le dataset généré (`dataset.csv`).
- `FrontEnd/` : Interface utilisateur Tkinter pour jouer contre l'IA (`morpion-game.py`).
- `generateur/` : Script de génération du dataset (`generator_dataset.py`).
- `models/` : Modèles entraînés sauvegardés (`model_xwins.pkl`, `model_is_draw.pkl`).
- `results/` : Sorties d'analyse (e.g., `eda_correlation_heatmap.png`).
- `scripts/` : Scripts d'analyse et d'entraînement (`train_models.py`, `analyze_coefficients.py`, `evaluate_models.py`).
- `requirements.txt` : Dépendances Python.
- `README.md` : Ce fichier.

## Résultats ML
## Réponses aux questions

## Q1 — Analyse des coefficients

Pour les deux modèles (x_wins et is_draw), les coefficients les plus élevés en valeur absolue correspondent principalement à la case centrale, suivie des cases situées dans les coins. Les cases sur les bords ont généralement une influence plus faible.

Dans le modèle x_wins, une occupation du centre ou des coins par X possède des coefficients positifs élevés, ce qui augmente fortement la probabilité de victoire de X. À l’inverse, ces mêmes positions occupées par O ont des coefficients négatifs importants, réduisant les chances de victoire de X.

Dans le modèle is_draw, les coefficients élevés traduisent des configurations plus équilibrées entre X et O, où aucune position dominante ne se dégage clairement, ce qui favorise un match nul.

La case centrale est particulièrement influente, car elle intervient dans le plus grand nombre de combinaisons gagnantes possibles.

Ces résultats sont cohérents avec la stratégie humaine : les joueurs expérimentés privilégient le centre, puis les coins, car ces positions offrent plus d’opportunités de créer des alignements ou des doubles menaces, contrairement aux bords qui sont moins stratégiques.
## Q2
Le modèle `x_wins` est plus facile à apprendre que `is_draw` en raison du déséquilibre des classes : `x_wins` a 75.53% de classe 1 vs 24.47% de 0, tandis que `is_draw` a 81.8% de 0 vs 18.2% de 1. Cela entraîne un biais où `is_draw` ne prédit jamais la classe minoritaire (match nul), donnant une précision élevée (82.7%) mais un f1-score faible (74.8%) et une matrice de confusion montrant 0 prédictions correctes pour les nuls. En revanche, `x_wins` a un f1-score de 73.4% avec une meilleure répartition des erreurs. Pour améliorer `is_draw`, on pourrait utiliser du sur-échantillonnage (SMOTE) ou des poids de classe.
## Q3
Les métriques d'évaluation montrent que les modèles sont performants sur l'ensemble test (20% des données) :
- `x_wins` : Accuracy 78.8%, F1 73.4%, Precision 76.5%, Recall 78.8%. Matrice : [[18 94] [9 364]] – bon rappel pour la classe majoritaire, faible pour la minoritaire.
- `is_draw` : Accuracy 82.7%, F1 74.8%, Precision 68.4%, Recall 82.7%. Matrice : [[401 0] [84 0]] – prédit toujours "pas nul", ignorant les nuls.
Ces résultats indiquent un surapprentissage possible sur la classe majoritaire, avec besoin d'équilibrage pour de meilleures performances globales.
## Q4
L'IA intégrée dans `morpion-game.py` utilise les modèles pour jouer en O : à chaque tour, elle simule tous les coups possibles, encode l'état, prédit `x_wins` et `is_draw`, et choisit le coup minimisant `x_wins` + maximisant `is_draw` (score = -prob_xwins + prob_draw). Cela permet une stratégie défensive/intelligente. L'interface Tkinter affiche le plateau, la matrice encodée, et permet de jouer contre l'IA en temps réel. L'IA réagit en ~0.5s par coup, offrant une expérience fluide.
## Liens vers la vidéo
