import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ---------------------------------------------------------
# 1. Chargement et préparation des données
# ---------------------------------------------------------
df = pd.read_csv('ressources/dataset.csv')
X = df.drop(columns=['x_wins', 'is_draw'])
y_x = df['x_wins']
y_draw = df['is_draw']

# Division en ensembles d'entraînement et de test (80/20)
X_train, X_test, yx_train, yx_test, yd_train, yd_test = train_test_split(
    X, y_x, y_draw, test_size=0.2, random_state=42
)

# ---------------------------------------------------------
# 2. Entraînement des deux modèles Random Forest
# ---------------------------------------------------------
print("--- [Étape 3] Entraînement des Random Forests ---")

# Modèle pour prédire si X gagne
rf_x = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42)
rf_x.fit(X_train, yx_train)

# Modèle pour prédire si c'est un match nul
rf_draw = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42)
rf_draw.fit(X_train, yd_train)

# ---------------------------------------------------------
# 3. Évaluation des performances
# ---------------------------------------------------------
def afficher_stats(model, X_t, y_t, nom_cible):
    preds = model.predict(X_t)
    print(f"\nRésultats pour {nom_cible}:")
    print(f"Accuracy: {accuracy_score(y_t, preds):.4f}")
    print(classification_report(y_t, preds, zero_division=0))

afficher_stats(rf_x, X_test, yx_test, "X_WINS")
afficher_stats(rf_draw, X_test, yd_test, "IS_DRAW")

# ---------------------------------------------------------
# 4. Sauvegarde pour l'Étape 4 (Interface)
# ---------------------------------------------------------
joblib.dump(rf_x, 'ressources/model_x_wins_final.pkl')
joblib.dump(rf_draw, 'ressources/model_is_draw_final.pkl')

print("\nModèles sauvegardés avec succès dans 'ressources/'.")