import pandas as pd
import os

class TicTacToeGenerator:
    def __init__(self, use_alpha_beta=True):
        self.data = []
        self.memo = {}
        self.visited_states = set()  # Optimisation : recherche de doublons en O(1)
        self.use_alpha_beta = use_alpha_beta
        self.win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

    def check_winner(self, board):
        for c in self.win_coords:
            if board[c[0]] == board[c[1]] == board[c[2]] != 0:
                return board[c[0]] # 1 pour X, -1 pour O
        if 0 not in board: return 0 # Match nul
        return None # Partie en cours

    def minimax(self, board, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        state = tuple(board)
        if state in self.memo: return self.memo[state]
        
        res = self.check_winner(board)
        if res is not None: return res

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = 1
                    score = self.minimax(board, False, alpha, beta)
                    board[i] = 0
                    best_score = max(score, best_score)
                    if self.use_alpha_beta:
                        alpha = max(alpha, score)
                        if beta <= alpha: break # Élagage
            self.memo[state] = best_score
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = -1
                    score = self.minimax(board, True, alpha, beta)
                    board[i] = 0
                    best_score = min(score, best_score)
                    if self.use_alpha_beta:
                        beta = min(beta, score)
                        if beta <= alpha: break # Élagage
            self.memo[state] = best_score
            return best_score

    def generate_all_states(self, board, turn_x):
        state = tuple(board)
        
        # Condition : uniquement au tour de X et si l'état n'a pas été déjà traité
        if turn_x and self.check_winner(board) is None:
            if state not in self.visited_states:
                outcome = self.minimax(list(board), True)
                self.data.append({'state': state, 'outcome': outcome})
                self.visited_states.add(state)

        # Arrêt si état terminal
        if self.check_winner(board) is not None: return

        # Exploration récursive
        for i in range(9):
            if board[i] == 0:
                board[i] = 1 if turn_x else -1
                self.generate_all_states(board, not turn_x)
                board[i] = 0

    def export_csv(self, output_path=None):
        if output_path is None:
            base = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(base, '..', 'ressources', 'dataset1.csv')

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        rows = []
        for item in self.data:
            board = item['state']
            res = item['outcome']
            row = []
            for val in board:
                if val == 1:    row.extend([1, 0])
                elif val == -1: row.extend([0, 1])
                else:           row.extend([0, 0])
            row.append(1 if res == 1 else 0)
            row.append(1 if res == 0 else 0)
            rows.append(row)

        cols = [f'c{i}_{p}' for i in range(9) for p in ['x', 'o']] + ['x_wins', 'is_draw']
        df = pd.DataFrame(rows, columns=cols)
        df.to_csv(output_path, index=False)
        print(f"Dataset généré : {len(df)} lignes uniques enregistrées → {output_path}")