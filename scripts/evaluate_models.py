import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, classification_report

# Charger données
data = pd.read_csv('ressources/dataset.csv')
X = data.drop(['x_wins', 'is_draw'], axis=1)
y_x = data['x_wins']
y_draw = data['is_draw']

# split train/test
from sklearn.model_selection import train_test_split
X_train, X_test, y_x_train, y_x_test = train_test_split(X, y_x, test_size=0.2, random_state=42)
_, _, y_draw_train, y_draw_test = train_test_split(X, y_draw, test_size=0.2, random_state=42)

# Charger modèles
model_xwins = joblib.load('models/model_xwins.pkl')
model_draw = joblib.load('models/model_is_draw.pkl')

for name, model, y_test in [('x_wins', model_xwins, y_x_test), ('is_draw', model_draw, y_draw_test)]:
    y_pred = model.predict(X_test)
    print(f'--- Evaluation model {name} ---')
    print('Accuracy :', accuracy_score(y_test, y_pred))
    print('F1-score:', f1_score(y_test, y_pred, average='weighted', zero_division=0))
    print('Precision :', precision_score(y_test, y_pred, average='weighted', zero_division=0))
    print('Recall :', recall_score(y_test, y_pred, average='weighted', zero_division=0))
    print('Confusion matrix:')
    print(confusion_matrix(y_test, y_pred))
    print('Classification report:')
    print(classification_report(y_test, y_pred, zero_division=0))
    print('\n')
