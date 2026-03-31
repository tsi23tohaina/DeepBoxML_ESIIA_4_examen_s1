import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Charger le dataset
data = pd.read_csv('ressources/dataset.csv')

# Séparer les features et les targets
features = data.drop(['x_wins', 'is_draw'], axis=1)
x_wins_target = data['x_wins']
is_draw_target = data['is_draw']

# Diviser en train/test
X_train, X_test, y_train_xwins, y_test_xwins = train_test_split(features, x_wins_target, test_size=0.2, random_state=42)
_, _, y_train_draw, y_test_draw = train_test_split(features, is_draw_target, test_size=0.2, random_state=42)

# Modèle pour x_wins
model_xwins = LogisticRegression(max_iter=10000)
model_xwins.fit(X_train, y_train_xwins)

# Prédictions et évaluation
y_pred_xwins = model_xwins.predict(X_test)
print("Modèle x_wins:")
print(f"Accuracy: {accuracy_score(y_test_xwins, y_pred_xwins)}")
print(classification_report(y_test_xwins, y_pred_xwins))

# Modèle pour is_draw
model_draw = LogisticRegression(max_iter=1000)
model_draw.fit(X_train, y_train_draw)

y_pred_draw = model_draw.predict(X_test)
print("\nModèle is_draw:")
print(f"Accuracy: {accuracy_score(y_test_draw, y_pred_draw)}")
print(classification_report(y_test_draw, y_pred_draw))

# Sauvegarder les modèles
joblib.dump(model_xwins, 'models/model_xwins.pkl')
joblib.dump(model_draw, 'models/model_is_draw.pkl')

print("\nModèles sauvegardés dans 'models/'")