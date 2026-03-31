import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Étape 1 : EDA et préparation des données
print("--- Etape 1: EDA et préparation des données ---")

data = pd.read_csv('ressources/dataset.csv')
print(f"Total lignes: {len(data)}")

# Distribution des cibles
for target in ['x_wins', 'is_draw']:
    counts = data[target].value_counts().sort_index()
    print(f"\nDistribution de {target}:")
    print(counts)
    perc = counts / counts.sum() * 100
    print('Pourcentages :')
    print(perc.round(2))

# balance x_wins vs is_draw
print("\nCroisement x_wins / is_draw:")
print(pd.crosstab(data['x_wins'], data['is_draw']))

# Graphique EDA additionnel : distribution des cibles
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.countplot(x='x_wins', data=data, palette='Blues')
plt.title('Distribution x_wins')
plt.xlabel('x_wins')
plt.ylabel('Count')

plt.subplot(1, 2, 2)
sns.countplot(x='is_draw', data=data, palette='Oranges')
plt.title('Distribution is_draw')
plt.xlabel('is_draw')
plt.ylabel('Count')

plt.tight_layout()
plt.savefig('results/eda_target_distribution.png')
print("Graphique de distribution des cibles sauvegardé dans eda_target_distribution.png")
try:
    plt.show(block=False)
except Exception:
    pass

# Quelle case est le plus occupée par X dans les positions gagnantes de X ?
x_win_states = data[data['x_wins'] == 1]
occupancy_x = []
for i in range(9):
    col = f'c{i}_x'
    occupancy_x.append((i, x_win_states[col].mean()))
occupancy_x = sorted(occupancy_x, key=lambda x: x[1], reverse=True)
print("\nFréquence d'occupation par X pour les états où X gagne (case:ratio):")
for i, ratio in occupancy_x:
    print(f"c{i}: {ratio:.3f}")

# heatmap de corrélation
corr = data.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=False, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Heatmap de corrélation (dataset Morpion)')
plt.tight_layout()
plt.savefig('results/eda_correlation_heatmap.png')
print("Heatmap sauvegardée dans eda_correlation_heatmap.png")
try:
    plt.show(block=False)
except Exception:
    pass

# Étape 2: Baseline régression logistique (déjà entraîné)
print("\n--- Etape 2: Baseline Régression Logistique ---")
print("Le script de formation existant `train_models.py` a déjà produit les deux modèles.")

# Coefficients des modèles si disponibles
try:
    import joblib
    model_xwins = joblib.load('models/model_xwins.pkl')
    model_draw = joblib.load('models/model_is_draw.pkl')
    features = data.drop(['x_wins', 'is_draw'], axis=1)

    coeffs_xwins = pd.DataFrame({'Feature': features.columns, 'Coefficient': model_xwins.coef_[0]})
    coeffs_xwins['Abs_Coeff'] = coeffs_xwins['Coefficient'].abs()
    coeffs_xwins = coeffs_xwins.sort_values('Abs_Coeff', ascending=False)
    print("\nTop 10 coefficients x_wins:")
    print(coeffs_xwins.head(10))

    coeffs_draw = pd.DataFrame({'Feature': features.columns, 'Coefficient': model_draw.coef_[0]})
    coeffs_draw['Abs_Coeff'] = coeffs_draw['Coefficient'].abs()
    coeffs_draw = coeffs_draw.sort_values('Abs_Coeff', ascending=False)
    print("\nTop 10 coefficients is_draw:")
    print(coeffs_draw.head(10))
except FileNotFoundError:
    print("Modèles non trouvés : exécutez d'abord 'train_models.py'.")
