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

# ─────────────────────────────────────────────
# CHARGEMENT DES MODÈLES ML
# ─────────────────────────────────────────────

model_xwins = joblib.load('models/model_xwins.pkl')
model_draw = joblib.load('models/model_is_draw.pkl')

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
        self.ai_player = "O"  # IA joue en O
        self._creer_interface()

    def _get_ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.plateau[i] is None:
                # Simuler le coup
                self.plateau[i] = self.ai_player
                encoded = encoder_ligne(self.plateau)
                pred_xwins = model_xwins.predict_proba([encoded])[0][1]  # prob X wins
                pred_draw = model_draw.predict_proba([encoded])[0][1]   # prob draw
                # Score: pour O, minimiser xwins, maximiser draw
                score = -pred_xwins + pred_draw
                if score > best_score:
                    best_score = score
                    best_move = i
                self.plateau[i] = None  # annuler simulation
        return best_move

    def _jouer_ai(self):
        move = self._get_ai_move()
        if move is not None:
            self.jouer(move)

    def _creer_interface(self):

        # ── Statut ──────────────────────────────────────────────
        self.label_statut = tk.Label(
            self.root, text="Tour du joueur : X",
            font=("Helvetica", 13), pady=8
        )
        self.label_statut.pack()

        # ── Zone centrale : plateau | → | matrice ───────────────
        frame_main = tk.Frame(self.root)
        frame_main.pack(padx=20, pady=5)

        # -- Plateau --
        frame_plateau = tk.Frame(frame_main)
        frame_plateau.grid(row=0, column=0, sticky="n")

        tk.Label(frame_plateau, text="plateau",
                 font=("Helvetica", 9), fg="gray").grid(
            row=0, column=0, columnspan=3, pady=(0, 5))

        for i in range(9):
            btn = tk.Button(
                frame_plateau, text="",
                font=("Helvetica", 28, "bold"),
                width=3, height=1, relief="groove",
                command=lambda i=i: self.jouer(i)
            )
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=3, pady=3)
            self.boutons.append(btn)

        # -- Flèche --
        tk.Label(frame_main, text="→",
                 font=("Helvetica", 18), fg="gray").grid(
            row=0, column=1, padx=12, pady=(40, 0), sticky="n")

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
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Rejouer",
                  font=("Helvetica", 10),
                  command=self.reinitialiser, padx=12).pack(side="left", padx=5)

        tk.Button(frame_btn, text="Sauvegarder → CSV",
                  font=("Helvetica", 10),
                  command=self.sauvegarder, padx=12).pack(side="left", padx=5)

        self.label_info = tk.Label(
            self.root, text="", font=("Helvetica", 9), fg="green")
        self.label_info.pack(pady=(0, 10))

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