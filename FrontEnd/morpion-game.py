import tkinter as tk
import csv
import os
import joblib
import numpy as np

# ─────────────────────────────────────────────
# ENCODAGE
# ─────────────────────────────────────────────

COLONNES = [f"c{i}_{j}" for i in range(9) for j in ["x", "o"]]

def encoder_ligne(plateau):
    row = []
    for v in plateau:
        row.append(1 if v == "X" else 0)
        row.append(1 if v == "O" else 0)
    return row

COMBOS_GAGNANTS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def verifier_victoire(plateau, joueur):
    for combo in COMBOS_GAGNANTS:
        if all(plateau[i] == joueur for i in combo):
            return True
    return False

def generer_parties(fichier_csv="dataset_morpion.csv"):
    lignes = []
    seen = set()

    def jouer(plateau, joueur):
        cle = tuple(plateau)
        if cle in seen:
            return
        seen.add(cle)
        if verifier_victoire(plateau, "X"):
            label = "X"
        elif verifier_victoire(plateau, "O"):
            label = "O"
        elif all(v is not None for v in plateau):
            label = "nul"
        else:
            label = "en_cours"
        lignes.append(encoder_ligne(plateau) + [label])
        if label in ("X", "O", "nul"):
            return
        for i in range(9):
            if plateau[i] is None:
                nouveau = plateau[:]
                nouveau[i] = joueur
                jouer(nouveau, "O" if joueur == "X" else "X")

    jouer([None]*9, "X")
    with open(fichier_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLONNES + ["label"])
        writer.writerows(lignes)
    print(f"Dataset généré : {len(lignes)} positions → {fichier_csv}")

# ─────────────────────────────────────────────
# COULEURS
# ─────────────────────────────────────────────

COULEUR_X   = "#000000"   # X en noir
COULEUR_O   = "#CC0000"   # O en rouge
VERT_WIN    = "#A5D6A7"
GRIS_BG     = "#F0F0F0"
X_CLAIR     = "#E0E0E0"   # fond cellule matrice X
O_CLAIR     = "#FFCCBC"   # fond cellule matrice O
GRIS_TXT    = "#999999"

# Modes de jeu possibles
MODE_VS_HUMAN   = "vs_human"
MODE_VS_AI_ML   = "vs_ai_ml"
MODE_VS_AI_HYBRID = "vs_ai_hybrid"

# ─────────────────────────────────────────────
# CHARGEMENT DES MODÈLES ML
# ─────────────────────────────────────────────

model_xwins = joblib.load('models/x_wins_mlp_model.pkl')
model_draw = joblib.load('models/is_draw_mlp_model.pkl')

# ─────────────────────────────────────────────
# JEU TKINTER
# ─────────────────────────────────────────────

class Morpion:
    def __init__(self, root, fichier_csv="dataset_morpion.csv"):
        self.root = root
        self.root.title("Morpion — IA ML")
        self.root.resizable(False, False)
        self.fichier_csv = fichier_csv
        self.historique = []
        self.joueur_actuel = "X"
        self.plateau = [None] * 9
        self.boutons = []
        self.enc_labels = []
        self.mode = MODE_VS_AI_ML  # valeur initiale : IA (ML)
        self.ai_player = "O"  # IA joue en O quand activée
        self.mode_var = tk.StringVar(value=self.mode)
        self._creer_interface()

    def _changer_mode(self):
        self.mode = self.mode_var.get()
        if self.mode == MODE_VS_HUMAN:
            self.ai_player = None
        else:
            self.ai_player = "O"
        self.reinitialiser()

    def _eval_heuristique_ml(self, plateau):
        if verifier_victoire(plateau, "X"): return -1.0
        if verifier_victoire(plateau, "O"): return 1.0
        if all(v is not None for v in plateau): return 0.0
        encoded = encoder_ligne(plateau)
        pred_xwins = model_xwins.predict_proba([encoded])[0][1]
        pred_draw = model_draw.predict_proba([encoded])[0][1]
        return -pred_xwins + pred_draw

    def _minimax_hybride(self, plateau, depth, joueur, alpha=-float('inf'), beta=float('inf')):
        if verifier_victoire(plateau, "X") or verifier_victoire(plateau, "O") or all(v is not None for v in plateau):
            return self._eval_heuristique_ml(plateau)
        if depth == 0:
            return self._eval_heuristique_ml(plateau)

        if joueur == "O":
            best = -float('inf')
            for i in range(9):
                if plateau[i] is None:
                    plateau[i] = "O"
                    score = self._minimax_hybride(plateau, depth - 1, "X", alpha, beta)
                    plateau[i] = None
                    best = max(best, score)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            return best
        else:
            best = float('inf')
            for i in range(9):
                if plateau[i] is None:
                    plateau[i] = "X"
                    score = self._minimax_hybride(plateau, depth - 1, "O", alpha, beta)
                    plateau[i] = None
                    best = min(best, score)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
            return best

    def _get_ai_move(self):
        if self.mode == MODE_VS_AI_HYBRID:
            best_score = -float('inf')
            best_move = None
            for i in range(9):
                if self.plateau[i] is None:
                    self.plateau[i] = self.ai_player
                    score = self._minimax_hybride(self.plateau, depth=3, joueur="X")
                    self.plateau[i] = None
                    if score > best_score:
                        best_score = score
                        best_move = i
            return best_move

        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.plateau[i] is None:
                self.plateau[i] = self.ai_player
                encoded = encoder_ligne(self.plateau)
                pred_xwins = model_xwins.predict_proba([encoded])[0][1]  # prob X wins
                pred_draw = model_draw.predict_proba([encoded])[0][1]   # prob draw
                score = -pred_xwins + pred_draw
                if score > best_score:
                    best_score = score
                    best_move = i
                self.plateau[i] = None
        return best_move

    def _jouer_ai(self):
        if self.mode == MODE_VS_HUMAN:
            return
        move = self._get_ai_move()
        if move is not None:
            self.jouer(move)

    def _creer_interface(self):

        # ── Choix du mode de jeu ─────────────────────────────────
        frame_mode = tk.Frame(self.root)
        frame_mode.pack(pady=(8, 0))

        tk.Label(frame_mode, text="Mode de jeu :", font=("Helvetica", 10, "bold")).pack(side="left", padx=(0, 8))
        tk.Radiobutton(
            frame_mode, text="Humain vs Humain", variable=self.mode_var,
            value=MODE_VS_HUMAN, command=self._changer_mode
        ).pack(side="left")
        tk.Radiobutton(
            frame_mode, text="IA (ML)", variable=self.mode_var,
            value=MODE_VS_AI_ML, command=self._changer_mode
        ).pack(side="left", padx=(8, 0))
        tk.Radiobutton(
            frame_mode, text="IA (Hybride)", variable=self.mode_var,
            value=MODE_VS_AI_HYBRID, command=self._changer_mode
        ).pack(side="left", padx=(8, 0))

        # ── Statut ──────────────────────────────────────────────
        self.label_statut = tk.Label(
            self.root, text="Tour du joueur : X",
            font=("Helvetica", 18, "bold"), pady=12
        )
        self.label_statut.pack()

        # ── Zone centrale : plateau | → | matrice ───────────────
        frame_main = tk.Frame(self.root)
        frame_main.pack(padx=40, pady=10)

        # -- Plateau --
        frame_plateau = tk.Frame(frame_main)
        frame_plateau.grid(row=0, column=0, sticky="n")

        tk.Label(frame_plateau, text="plateau",
                 font=("Helvetica", 9), fg="gray").grid(
            row=0, column=0, columnspan=3, pady=(0, 5))

        for i in range(9):
            btn = tk.Button(
                frame_plateau, text="",
                font=("Helvetica", 23, "bold"),
                width=7, height=4, relief="groove",
                command=lambda i=i: self.jouer(i)
            )
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=8, pady=8)
            self.boutons.append(btn)

        # -- Flèche --
        tk.Label(frame_main, text="→",
                 font=("Helvetica", 28), fg="gray").grid(
            row=0, column=1, padx=30, pady=(80, 0), sticky="n")

        # -- Matrice --
        frame_matrice = tk.Frame(frame_main)
        frame_matrice.grid(row=0, column=2, sticky="n")

        tk.Label(frame_matrice, text="encodage  (9 × 2 features)",
                 font=("Helvetica", 9), fg="gray").grid(
            row=0, column=0, columnspan=3, pady=(0, 5))

        # En-têtes
        tk.Label(frame_matrice, text="",
                 font=("Courier", 9), width=5).grid(row=1, column=0)
        tk.Label(frame_matrice, text="_x",
                 font=("Courier", 9), fg="gray", width=5).grid(row=1, column=1)
        tk.Label(frame_matrice, text="_o",
                 font=("Courier", 9), fg="gray", width=5).grid(row=1, column=2)

        # Lignes c0 … c8  (alignées sur les 3 rangées du plateau)
        for i in range(9):
            tk.Label(frame_matrice, text=f"c{i}",
                     font=("Courier", 10), fg="gray",
                     anchor="e", width=4).grid(
                row=i + 2, column=0, padx=(0, 6), pady=3)

            lx = tk.Label(frame_matrice, text="0",
                          font=("Courier", 11, "bold"), width=3,
                          bg=GRIS_BG, fg=GRIS_TXT,
                          relief="groove", padx=4, pady=3)
            lx.grid(row=i + 2, column=1, padx=2, pady=3)

            lo = tk.Label(frame_matrice, text="0",
                          font=("Courier", 11, "bold"), width=3,
                          bg=GRIS_BG, fg=GRIS_TXT,
                          relief="groove", padx=4, pady=3)
            lo.grid(row=i + 2, column=2, padx=2, pady=3)

            self.enc_labels.append((lx, lo))

        # ── Boutons bas ─────────────────────────────────────────
        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=15)

        tk.Button(frame_btn, text="Rejouer",
                  font=("Helvetica", 12, "bold"),
                  command=self.reinitialiser, padx=15, pady=8).pack(side="left", padx=8)

        tk.Button(frame_btn, text="Sauvegarder → CSV",
                  font=("Helvetica", 12, "bold"),
                  command=self.sauvegarder, padx=15, pady=8).pack(side="left", padx=8)

        self.label_info = tk.Label(
            self.root, text="", font=("Helvetica", 11), fg="green")
        self.label_info.pack(pady=(0, 15))

    # ── Mise à jour de la matrice ────────────────────────────────
    def _mettre_a_jour_matrice(self):
        for i, val in enumerate(self.plateau):
            lx, lo = self.enc_labels[i]
            if val == "X":
                lx.config(text="1", bg=X_CLAIR,  fg=COULEUR_X)
                lo.config(text="0", bg=GRIS_BG,  fg=GRIS_TXT)
            elif val == "O":
                lx.config(text="0", bg=GRIS_BG,  fg=GRIS_TXT)
                lo.config(text="1", bg=O_CLAIR,   fg=COULEUR_O)
            else:
                lx.config(text="0", bg=GRIS_BG, fg=GRIS_TXT)
                lo.config(text="0", bg=GRIS_BG, fg=GRIS_TXT)

    # ── Coup joué ────────────────────────────────────────────────
    def jouer(self, index):
        if self.plateau[index]:
            return

        self.plateau[index] = self.joueur_actuel
        couleur = COULEUR_X if self.joueur_actuel == "X" else COULEUR_O
        self.boutons[index].config(
            text=self.joueur_actuel,
            fg=couleur,
            disabledforeground=couleur,
            state="disabled")
        self._mettre_a_jour_matrice()

        if verifier_victoire(self.plateau, self.joueur_actuel):
            label = self.joueur_actuel
        elif all(v is not None for v in self.plateau):
            label = "nul"
        else:
            label = "en_cours"

        self.historique.append(encoder_ligne(self.plateau) + [label])

        if label in ("X", "O"):
            self._mettre_en_valeur(self._combo_gagnant())
            self.label_statut.config(
                text=f"Victoire du joueur {self.joueur_actuel} !")
            self._desactiver_tout()
        elif label == "nul":
            self.label_statut.config(text="Match nul !")
        else:
            self.joueur_actuel = "O" if self.joueur_actuel == "X" else "X"
            self.label_statut.config(
                text=f"Tour du joueur : {self.joueur_actuel}")

            if self.mode == MODE_VS_HUMAN:
                return

            if self.joueur_actuel == self.ai_player:
                self.root.after(500, self._jouer_ai)  # Délai pour simuler réflexion

    def _combo_gagnant(self):
        for combo in COMBOS_GAGNANTS:
            if all(self.plateau[i] == self.joueur_actuel for i in combo):
                return combo
        return []

    def _mettre_en_valeur(self, combo):
        for i in combo:
            self.boutons[i].config(background=VERT_WIN)

    def _desactiver_tout(self):
        for btn in self.boutons:
            btn.config(state="disabled")

    # ── Sauvegarde CSV ───────────────────────────────────────────
    def sauvegarder(self):
        if not self.historique:
            self.label_info.config(text="Aucun coup joué.", fg="orange")
            return
        existe = os.path.exists(self.fichier_csv)
        with open(self.fichier_csv, "a", newline="") as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(COLONNES + ["label"])
            writer.writerows(self.historique)
        self.label_info.config(
            text=f"{len(self.historique)} états sauvegardés dans '{self.fichier_csv}'",
            fg="green")

    # ── Réinitialisation ─────────────────────────────────────────
    def reinitialiser(self):
        self.joueur_actuel = "X"
        self.plateau = [None] * 9
        self.historique = []
        self.label_statut.config(text="Tour du joueur : X")
        self.label_info.config(text="")
        for btn in self.boutons:
            btn.config(text="", state="normal",
                       background="SystemButtonFace", fg="black")
        self._mettre_a_jour_matrice()

# ─────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    Morpion(root, fichier_csv="dataset_morpion.csv")
    root.mainloop()