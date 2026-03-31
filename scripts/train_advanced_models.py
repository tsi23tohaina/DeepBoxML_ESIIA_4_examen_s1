import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, classification_report
import joblib

try:
    from xgboost import XGBClassifier
    has_xgb = True
except ImportError:
    has_xgb = False


def run_and_report(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1w = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    prew = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rew = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    print(f"--- {name} ---")
    print(f" Accuracy: {acc:.4f}")
    print(f" F1-score (weighted): {f1w:.4f}")
    print(f" Precision (weighted): {prew:.4f}")
    print(f" Recall (weighted): {rew:.4f}")
    print(" Confusion matrix:\n", cm)
    print(" Classification report:\n", classification_report(y_test, y_pred, zero_division=0))
    print("\n")

    joblib.dump(model, f"models/{name.lower()}_model.pkl")
    return {
        'model': name,
        'accuracy': acc,
        'f1_weighted': f1w,
        'precision_weighted': prew,
        'recall_weighted': rew,
        'confusion_matrix': cm.tolist()
    }


if __name__ == "__main__":
    data = pd.read_csv('ressources/dataset.csv')
    X = data.drop(['x_wins', 'is_draw'], axis=1)
    y_x = data['x_wins']
    y_draw = data['is_draw']

    results = []

    for target_name, y in [('x_wins', y_x), ('is_draw', y_draw)]:
        print(f"===== Cible: {target_name} =====")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        models = [
            ('DecisionTree', DecisionTreeClassifier(random_state=42)),
            ('RandomForest', RandomForestClassifier(n_estimators=200, random_state=42)),
            ('MLP', MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42))
        ]
        if has_xgb:
            models.insert(2, ('XGBoost', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)))

        for name, model in models:
            stats = run_and_report(f"{target_name}_{name}", model, X_train, X_test, y_train, y_test)
            stats['target'] = target_name
            results.append(stats)

    df_results = pd.DataFrame([{
        'target': r['target'],
        'model': r['model'],
        'accuracy': r['accuracy'],
        'f1_weighted': r['f1_weighted'],
        'precision_weighted': r['precision_weighted'],
        'recall_weighted': r['recall_weighted']
    } for r in results])

    df_results.to_csv('results/advanced_model_comparison.csv', index=False)
    print('Sauvegarde des résultats dans results/advanced_model_comparison.csv')
