from flask import Flask, request,render_template, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# --- CHARGEMENT DES MODÈLES ---
model_x = joblib.load('ressources/model_x_wins_final.pkl')
model_draw = joblib.load('ressources/model_is_draw_final.pkl')

# --- LOGIQUE DE JEU (Utilitaires) ---
WIN_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
    [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
]


def check_winner(board):
    for combo in WIN_COMBOS:
        if board[combo[0]] != "" and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    if "" not in board: return "draw"
    return None


def encode_board(board):
    features = []
    for cell in board:
        features.append(1 if cell == 'X' else 0)
        features.append(1 if cell == 'O' else 0)
    return pd.DataFrame([features])


# --- FONCTION D'ÉVALUATION ML (Pour les feuilles du Minimax) ---
def evaluate_position_ml(board):
    features = encode_board(board)
    # Score = P(X gagne) - P(O gagne n'existe pas ici, donc on pondère avec le nul)
    prob_win = model_x.predict_proba(features)[0][1]
    prob_draw = model_draw.predict_proba(features)[0][1]
    # On donne une valeur positive à la victoire et neutre/légère au nul
    return prob_win * 100 + prob_draw * 10


# --- ALGORITHME MINIMAX-HYBRIDE ---
def minimax_hybrid(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)

    # Cas terminaux de base
    if winner == "X": return 1000
    if winner == "O": return -1000
    if winner == "draw": return 0

    # Limite de profondeur atteinte : on utilise le ML !
    if depth == 0:
        return evaluate_position_ml(board)

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax_hybrid(board, depth - 1, alpha, beta, False)
                board[i] = ""
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha: break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax_hybrid(board, depth - 1, alpha, beta, True)
                board[i] = ""
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha: break
        return best_score


# --- ROUTES API ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_ml', methods=['POST'])
def predict_ml():
    """Mode IA (ML) Pur : Évalue chaque coup possible avec le ML uniquement"""
    board = request.json.get('board')
    best_move = -1
    best_val = -float('inf')

    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            val = evaluate_position_ml(board)
            board[i] = ""
            if val > best_val:
                best_val = val
                best_move = i
    return jsonify({"move": best_move})


@app.route('/predict_hybrid', methods=['POST'])
def predict_hybrid():
    """Mode IA (Hybride) : Minimax Profondeur 3 + Heuristique ML"""
    board = request.json.get('board')
    best_move = -1
    best_val = -float('inf')

    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            # On lance le minimax à profondeur 3 (on compte le coup actuel comme depth 1)
            val = minimax_hybrid(board, 2, -float('inf'), float('inf'), False)
            board[i] = ""
            if val > best_val:
                best_val = val
                best_move = i
    return jsonify({"move": best_move})


if __name__ == '__main__':
    app.run(debug=True, port=5000)