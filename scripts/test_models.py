import pandas as pd
import joblib
import numpy as np

# Charger un modèle (exemple: MLP pour x_wins)
model = joblib.load('models/x_wins_mlp_model.pkl')

# Exemple d'état de jeu (vide)
board = [0] * 9  # 9 cases vides

# Encoder comme dans le dataset (18 features: c0_x, c0_o, ..., c8_x, c8_o)
def encode_board(board):
    row = []
    for val in board:
        if val == 1:  # X
            row.extend([1, 0])
        elif val == -1:  # O
            row.extend([0, 1])
        else:  # vide
            row.extend([0, 0])
    return row

encoded = encode_board(board)
print("État encodé:", encoded)

# Prédiction
pred_prob = model.predict_proba([encoded])
pred_class = model.predict([encoded])

print("Probabilité de gagner pour X:", pred_prob[0][1])
print("Classe prédite (1=X gagne, 0=non):", pred_class[0])

# Test avec un état gagnant pour X (ex: X au centre et coins)
board_win = [1, 0, 1, 0, 1, 0, 1, 0, 0]  # X au centre et coins
encoded_win = encode_board(board_win)
pred_win = model.predict_proba([encoded_win])
print("État gagnant pour X - Probabilité:", pred_win[0][1])

# Pour tester is_draw
model_draw = joblib.load('models/is_draw_mlp_model.pkl')
pred_draw = model_draw.predict_proba([encoded])
print("Probabilité de match nul:", pred_draw[0][1])