import tkinter as tk
from tkinter import font as tkfont
import csv
import os
import sys

# Ajoute le dossier "generateur" situé en parallèle de "FrontEnd"
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generateur'))
try:
    from generator_dataset import TicTacToeGenerator
except ImportError:
    print("Attention: module generator_dataset introuvable. Assurez-vous des chemins.")
    # Fallback pour tester l'interface si le générateur n'est pas là
    class TicTacToeGenerator:
        def __init__(self, use_alpha_beta=True): pass
        def generate_all_states(self, a, b): pass
        def export_csv(self, output_path): pass
        def minimax(self, board, is_max): return 0

# ─────────────────────────────────────────────
# COLONNES & UTILITAIRES
# ─────────────────────────────────────────────

COLONNES = [f"c{i}_{p}" for i in range(9) for p in ["x", "o"]] + ["x_wins", "is_draw"]

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

def encoder_ligne(plateau, gen):
    board = [1 if v=="X" else (-1 if v=="O" else 0) for v in plateau]
    outcome = gen.minimax(list(board), True)
    row = []
    for v in plateau:
        row.append(1 if v == "X" else 0)
        row.append(1 if v == "O" else 0)
    row.append(1 if outcome == 1 else 0)
    row.append(1 if outcome == 0 else 0)
    return row

# ─────────────────────────────────────────────
# COULEURS ET STYLES (Design plus moderne)
# ─────────────────────────────────────────────
BG_APP      = "#F4F6F9"
BG_FRAME    = "#FFFFFF"
COULEUR_X   = "#2C3E50"  # Bleu nuit
COULEUR_O   = "#E74C3C"  # Rouge
VERT_WIN    = "#2ECC71"
GRIS_BG     = "#E2E8F0"
X_CLAIR     = "#D5DBDB"
O_CLAIR     = "#FADBD8"
GRIS_TXT    = "#7F8C8D"
BTN_ACCENT  = "#3498DB"
BTN_ACCENT_TXT = "#FFFFFF"

# ─────────────────────────────────────────────
# JEU TKINTER MULTI-ÉCRANS
# ─────────────────────────────────────────────

class Morpion:

    def __init__(self, root, fichier_csv=None):
        self.root = root
        self.root.title("Morpion — Encodage ML")
        self.root.geometry("750x650") # Fenêtre un peu plus grande
        self.root.configure(bg=BG_APP)
        self.root.resizable(False, False)

        # Polices personnalisées
        self.font_titre = tkfont.Font(family="Helvetica", size=32, weight="bold")
        self.font_sous_titre = tkfont.Font(family="Helvetica", size=14)
        self.font_btn = tkfont.Font(family="Helvetica", size=12, weight="bold")

        if fichier_csv is None:
            base = os.path.dirname(os.path.abspath(__file__))
            fichier_csv = os.path.join(base, '..', 'ressources', 'dataset1.csv')
        self.fichier_csv = fichier_csv

        # Variables d'état
        self.historique = []
        self.joueur_actuel = "X"
        self.plateau = [None] * 9
        self.boutons = []
        self.enc_labels = []
        
        self.mode_alpha_beta = tk.BooleanVar(value=True)
        self.mode_jeu = tk.StringVar(value="multi") 

        # Initialisation IA
        self.gen = TicTacToeGenerator(use_alpha_beta=True)
        self._generer_dataset()

        # Dictionnaire pour stocker les différents écrans
        self.frames = {}
        self._creer_tous_les_ecrans()
        
        # Afficher le premier écran
        self.afficher_ecran("Accueil")

    # ── Gestion de la navigation (Transitions) ───────────────────
    def _creer_tous_les_ecrans(self):
        self.frames["Accueil"] = self._creer_ecran_accueil()
        self.frames["Modes"] = self._creer_ecran_modes()
        self.frames["Jeu"] = self._creer_ecran_jeu()

    def afficher_ecran(self, nom_ecran):
        """Masque tous les écrans et affiche celui demandé."""
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Effet de "transition" simple en affichant le nouveau frame
        self.frames[nom_ecran].pack(fill="both", expand=True)

        if nom_ecran == "Jeu":
            self.reinitialiser()

    # ── Écran 1 : Accueil ────────────────────────────────────────
    def _creer_ecran_accueil(self):
        frame = tk.Frame(self.root, bg=BG_APP)
        
        # Centrage vertical
        container = tk.Frame(frame, bg=BG_APP)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Morpion IA", font=self.font_titre, bg=BG_APP, fg="#2C3E50").pack(pady=(0, 10))
        tk.Label(container, text="Génération de Dataset & Minimax", font=self.font_sous_titre, bg=BG_APP, fg="#7F8C8D").pack(pady=(0, 40))

        btn_commencer = tk.Button(
            container, text="COMMENCER", font=self.font_btn, 
            bg=BTN_ACCENT, fg=BTN_ACCENT_TXT, activebackground="#2980B9", 
            activeforeground="white", relief="flat", width=20, height=2,
            command=lambda: self.afficher_ecran("Modes")
        )
        btn_commencer.pack()
        
        return frame

    # ── Écran 2 : Choix des modes ────────────────────────────────
    def _creer_ecran_modes(self):
        frame = tk.Frame(self.root, bg=BG_APP)
        
        container = tk.Frame(frame, bg=BG_FRAME, padx=40, pady=40, relief="flat")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Configuration", font=("Helvetica", 20, "bold"), bg=BG_FRAME).pack(pady=(0, 30))

        # --- Choix Mode de jeu ---
        tk.Label(container, text="Adversaire :", font=("Helvetica", 12, "bold"), bg=BG_FRAME).pack(anchor="w")
        
        frame_radio1 = tk.Frame(container, bg=BG_FRAME)
        frame_radio1.pack(fill="x", pady=10)
        
        tk.Radiobutton(frame_radio1, text="Joueur 2 (Local)", variable=self.mode_jeu, value="multi", bg=BG_FRAME, font=("Helvetica", 11)).pack(anchor="w")
        tk.Radiobutton(frame_radio1, text="IA Minimax (Invincible)", variable=self.mode_jeu, value="ia_minimax", bg=BG_FRAME, font=("Helvetica", 11)).pack(anchor="w")
        tk.Radiobutton(frame_radio1, text="IA Custom (Dataset)", variable=self.mode_jeu, value="ia_custom", bg=BG_FRAME, font=("Helvetica", 11)).pack(anchor="w")

        # --- Choix Algorithme ---
        tk.Label(container, text="Moteur de Dataset :", font=("Helvetica", 12, "bold"), bg=BG_FRAME).pack(anchor="w", pady=(20, 0))
        
        frame_radio2 = tk.Frame(container, bg=BG_FRAME)
        frame_radio2.pack(fill="x", pady=10)

        tk.Radiobutton(frame_radio2, text="Alpha-Bêta (Rapide)", variable=self.mode_alpha_beta, value=True, bg=BG_FRAME, font=("Helvetica", 11), command=self._changer_mode_dataset).pack(anchor="w")
        tk.Radiobutton(frame_radio2, text="Classique (Lent)", variable=self.mode_alpha_beta, value=False, bg=BG_FRAME, font=("Helvetica", 11), command=self._changer_mode_dataset).pack(anchor="w")

        # --- Boutons Navigation ---
        frame_btns = tk.Frame(container, bg=BG_FRAME)
        frame_btns.pack(fill="x", pady=(30, 0))

        tk.Button(frame_btns, text="Retour", font=("Helvetica", 11), relief="flat", bg="#BDC3C7", width=12, command=lambda: self.afficher_ecran("Accueil")).pack(side="left")
        tk.Button(frame_btns, text="Jouer", font=("Helvetica", 11, "bold"), relief="flat", bg=VERT_WIN, fg="white", width=12, command=lambda: self.afficher_ecran("Jeu")).pack(side="right")

        return frame

    # ── Écran 3 : Jeu (Plateau + Matrice) ─────────────────────────
    def _creer_ecran_jeu(self):
        frame = tk.Frame(self.root, bg=BG_APP)

        # Bouton Retour (en haut à gauche)
        frame_top = tk.Frame(frame, bg=BG_APP)
        frame_top.pack(fill="x", padx=10, pady=10)
        tk.Button(frame_top, text="← Changer de mode", font=("Helvetica", 10), relief="flat", bg="#E0E0E0", command=lambda: self.afficher_ecran("Modes")).pack(side="left")

        # Statut
        self.label_statut = tk.Label(frame, text="Tour du joueur : X", font=("Helvetica", 16, "bold"), bg=BG_APP)
        self.label_statut.pack(pady=10)

        # Zone centrale (Plateau + Flèche + Matrice)
        frame_main = tk.Frame(frame, bg=BG_APP)
        frame_main.pack(pady=10)

        # -- Plateau --
        frame_plateau = tk.Frame(frame_main, bg=BG_APP)
        frame_plateau.grid(row=0, column=0, sticky="n", padx=20)

        for i in range(9):
            btn = tk.Button(
                frame_plateau, text="", font=("Helvetica", 32, "bold"),
                width=3, height=1, relief="ridge", bg="white",
                command=lambda i=i: self.jouer(i)
            )
            btn.grid(row=(i // 3), column=i % 3, padx=2, pady=2)
            self.boutons.append(btn)

        # -- Flèche --
        tk.Label(frame_main, text="→", font=("Helvetica", 24), bg=BG_APP, fg="gray").grid(row=0, column=1, padx=20, pady=(60, 0), sticky="n")

        # -- Matrice --
        frame_matrice = tk.Frame(frame_main, bg=BG_FRAME, padx=10, pady=10, relief="flat")
        frame_matrice.grid(row=0, column=2, sticky="n", padx=20)

        tk.Label(frame_matrice, text="Encodage Features", font=("Helvetica", 10, "bold"), bg=BG_FRAME, fg="#34495E").grid(row=0, column=0, columnspan=3, pady=(0, 10))

        tk.Label(frame_matrice, text="", bg=BG_FRAME).grid(row=1, column=0)
        tk.Label(frame_matrice, text=" X", font=("Courier", 10, "bold"), bg=BG_FRAME, fg=COULEUR_X).grid(row=1, column=1)
        tk.Label(frame_matrice, text=" O", font=("Courier", 10, "bold"), bg=BG_FRAME, fg=COULEUR_O).grid(row=1, column=2)

        for i in range(9):
            tk.Label(frame_matrice, text=f"c{i}", font=("Courier", 10), bg=BG_FRAME, fg="gray").grid(row=i+2, column=0, padx=(0,10), pady=2)
            lx = tk.Label(frame_matrice, text="0", font=("Courier", 11, "bold"), width=3, bg=GRIS_BG, fg=GRIS_TXT, relief="flat")
            lx.grid(row=i+2, column=1, padx=2, pady=2)
            lo = tk.Label(frame_matrice, text="0", font=("Courier", 11, "bold"), width=3, bg=GRIS_BG, fg=GRIS_TXT, relief="flat")
            lo.grid(row=i+2, column=2, padx=2, pady=2)
            self.enc_labels.append((lx, lo))

        # -- Prédiction Minimax --
        frame_pred = tk.Frame(frame, bg=BG_APP)
        frame_pred.pack(pady=15)
        tk.Label(frame_pred, text="Prédiction Minimax :", font=("Helvetica", 11), bg=BG_APP, fg="gray").pack(side="left", padx=5)
        self.label_pred = tk.Label(frame_pred, text="—", font=("Helvetica", 11, "bold"), bg=BG_APP, fg="gray")
        self.label_pred.pack(side="left")

        # -- Boutons Bas --
        frame_btn = tk.Frame(frame, bg=BG_APP)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Rejouer", font=("Helvetica", 11), bg="#95A5A6", fg="white", relief="flat", width=15, command=self.reinitialiser).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Sauvegarder → CSV", font=("Helvetica", 11, "bold"), bg=BTN_ACCENT, fg="white", relief="flat", width=20, command=self.sauvegarder).pack(side="left", padx=10)

        self.label_info = tk.Label(frame, text="", font=("Helvetica", 10), bg=BG_APP, fg="green")
        self.label_info.pack(pady=5)

        return frame

    # ── Logique interne (Génération & Mises à jour) ──────────────
    def _generer_dataset(self):
        # (Ton code intact)
        pass # Remplacé par un pass car dans l'original il imprime et génère, je garde ta logique en dessous
        import time
        use_ab = self.mode_alpha_beta.get()
        print(f"Génération du dataset...")
        start = time.time()
        gen_export = TicTacToeGenerator(use_alpha_beta=use_ab)
        gen_export.generate_all_states([0]*9, True)
        gen_export.export_csv(output_path=self.fichier_csv)
        print(f"Terminé en {time.time() - start:.2f} secondes.")

    def _changer_mode_dataset(self):
        use_ab = self.mode_alpha_beta.get()
        self.gen = TicTacToeGenerator(use_alpha_beta=use_ab)
        self._generer_dataset()

    def _mettre_a_jour_matrice(self):
        for i, val in enumerate(self.plateau):
            lx, lo = self.enc_labels[i]
            if val == "X":
                lx.config(text="1", bg=X_CLAIR, fg=COULEUR_X)
                lo.config(text="0", bg=GRIS_BG,  fg=GRIS_TXT)
            elif val == "O":
                lx.config(text="0", bg=GRIS_BG,  fg=GRIS_TXT)
                lo.config(text="1", bg=O_CLAIR,   fg=COULEUR_O)
            else:
                lx.config(text="0", bg=GRIS_BG, fg=GRIS_TXT)
                lo.config(text="0", bg=GRIS_BG, fg=GRIS_TXT)

    def _mettre_a_jour_prediction(self):
        board = [1 if v=="X" else (-1 if v=="O" else 0) for v in self.plateau]
        outcome = self.gen.minimax(list(board), True)
        if outcome == 1:
            self.label_pred.config(text="X va gagner", fg=COULEUR_X)
        elif outcome == -1:
            self.label_pred.config(text="O va gagner", fg=COULEUR_O)
        else:
            self.label_pred.config(text="Match nul", fg="#888888")

    # ── Mécanique de Jeu ─────────────────────────────────────────
    def _coup_ia(self):
        board = [1 if v=="X" else (-1 if v=="O" else 0) for v in self.plateau]
        meilleur_score = float('inf')
        meilleur_coup = None
        for i in range(9):
            if board[i] == 0:
                board[i] = -1
                score = self.gen.minimax(list(board), True)
                board[i] = 0
                if score < meilleur_score:
                    meilleur_score = score
                    meilleur_coup = i
        if meilleur_coup is not None:
            self.jouer(meilleur_coup)

    def _coup_ia_custom(self):
        pass

    def jouer(self, index):
        if self.plateau[index]:
            return

        self.plateau[index] = self.joueur_actuel

        couleur = COULEUR_X if self.joueur_actuel == "X" else COULEUR_O
        self.boutons[index].config(text=self.joueur_actuel, fg=couleur, disabledforeground=couleur, state="disabled")
        self._mettre_a_jour_matrice()

        if verifier_victoire(self.plateau, self.joueur_actuel):
            label = self.joueur_actuel
        elif all(v is not None for v in self.plateau):
            label = "nul"
        else:
            label = "en_cours"

        self.historique.append(encoder_ligne(self.plateau, self.gen))

        if label in ("X", "O"):
            self._mettre_en_valeur(self._combo_gagnant())
            self.label_statut.config(text=f"Victoire du joueur {self.joueur_actuel} !", fg=VERT_WIN)
            self.label_pred.config(text="—", fg="gray")
            self._desactiver_tout()
        elif label == "nul":
            self.label_statut.config(text="Match nul !", fg="gray")
            self.label_pred.config(text="—", fg="gray")
        else:
            self.joueur_actuel = "O" if self.joueur_actuel == "X" else "X"
            self.label_statut.config(text=f"Tour du joueur : {self.joueur_actuel}", fg="black")
            self._mettre_a_jour_prediction()
            mode = self.mode_jeu.get()
            if mode == "ia_minimax" and self.joueur_actuel == "O":
                self.root.after(400, self._coup_ia)
            elif mode == "ia_custom" and self.joueur_actuel == "O":
                self.root.after(400, self._coup_ia_custom)

    def _combo_gagnant(self):
        for combo in COMBOS_GAGNANTS:
            if all(self.plateau[i] == self.joueur_actuel for i in combo):
                return combo
        return []

    def _mettre_en_valeur(self, combo):
        for i in combo:
            self.boutons[i].config(background=VERT_WIN, disabledforeground="white")

    def _desactiver_tout(self):
        for btn in self.boutons:
            btn.config(state="disabled")

    def sauvegarder(self):
        if not self.historique:
            self.label_info.config(text="Aucun coup joué.", fg="orange")
            return
        os.makedirs(os.path.dirname(self.fichier_csv), exist_ok=True)
        existe = os.path.exists(self.fichier_csv)
        with open(self.fichier_csv, "a", newline="") as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(COLONNES)
            writer.writerows(self.historique)
        self.label_info.config(text=f"{len(self.historique)} états sauvegardés dans CSV.", fg="green")

    def reinitialiser(self):
        self.joueur_actuel = "X"
        self.plateau = [None] * 9
        self.historique = []
        self.label_statut.config(text="Tour du joueur : X", fg="black")
        self.label_info.config(text="")
        self.label_pred.config(text="—", fg="gray")
        for btn in self.boutons:
            btn.config(text="", state="normal", background="white", fg="black")
        self._mettre_a_jour_matrice()

# ─────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = Morpion(root)
    root.mainloop()