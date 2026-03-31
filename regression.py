import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

# ---------------------------
# 1. Chargement des données
# ---------------------------
df = pd.read_csv('ressources/dataset.csv')

# Séparation des features (X) et des cibles (y1, y2)
X = df.drop(columns=['x_wins', 'is_draw'])
y_x_wins = df['x_wins']
y_is_draw = df['is_draw']

# Split Train/Test (80% / 20%)
X_train, X_test, y1_train, y1_test, y2_train, y2_test = train_test_split(
    X, y_x_wins, y_is_draw, test_size=0.2, random_state=42
)

# ---------------------------
# 2. Modèle A : x_wins
# ---------------------------
print("--- Entraînement Modèle A (x_wins) ---")
model_x = LogisticRegression(max_iter=1000)
model_x.fit(X_train, y1_train)
y1_pred = model_x.predict(X_test)

print(f"Accuracy: {accuracy_score(y1_test, y1_pred):.4f}")
print(f"F1-Score: {f1_score(y1_test, y1_pred):.4f}")
print(classification_report(y1_test, y1_pred, zero_division=0))

# ---------------------------
# 3. Modèle B : is_draw
# ---------------------------
print("\n--- Entraînement Modèle B (is_draw) ---")
model_draw = LogisticRegression(max_iter=1000)
model_draw.fit(X_train, y2_train)
y2_pred = model_draw.predict(X_test)

print(f"Accuracy: {accuracy_score(y2_test, y2_pred):.4f}")
print(f"F1-Score: {f1_score(y2_test, y2_pred):.4f}")
print(classification_report(y2_test, y2_pred, zero_division=0))


# ---------------------------
# 4. Analyse des coefficients (Q1 & Étape 2)
# ---------------------------
def plot_coefficients(model, title):
    coefs = model.coef_[0]
    # Séparer les coefficients pour X (indices pairs) et O (indices impairs)
    coefs_x = coefs[0::2].reshape(3, 3)
    coefs_o = coefs[1::2].reshape(3, 3)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.heatmap(coefs_x, annot=True, cmap='coolwarm', ax=ax[0])
    ax[0].set_title(f'{title} - Influence de X')

    sns.heatmap(coefs_o, annot=True, cmap='coolwarm', ax=ax[1])
    ax[1].set_title(f'{title} - Influence de O')
    plt.show()


# Visualisation pour les deux modèles
plot_coefficients(model_x, "Modèle x_wins")
plot_coefficients(model_draw, "Modèle is_draw")