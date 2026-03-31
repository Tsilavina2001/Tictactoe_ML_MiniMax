import pandas as pd
import os


# ---------------------------
# 1. Vérification du gagnant
# ---------------------------
def check_winner(board):
    """
    Détermine si un joueur a gagné ou si c'est un match nul.
    Entrée : liste de 9 cases.
    Sortie : 'X', 'O', 'draw' ou None.
    """
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colonnes
        [0, 4, 8], [2, 4, 6]  # diagonales
    ]

    for line in wins:
        if board[line[0]] != "" and all(board[i] == board[line[0]] for i in line):
            return board[line[0]]

    if "" not in board:
        return "draw"

    return None


# ---------------------------
# 2. Minimax + Alpha-Bêta
# ---------------------------
def minimax(board, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    """
    Calcule le résultat théorique en jeu parfait[cite: 42, 45].
    """
    result = check_winner(board)

    if result == "X": return 1
    if result == "O": return -1
    if result == "draw": return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, False, alpha, beta)
                board[i] = ""
                best = max(best, score)
                alpha = max(alpha, score)
                if beta <= alpha: break
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, True, alpha, beta)
                board[i] = ""
                best = min(best, score)
                beta = min(beta, score)
                if beta <= alpha: break
        return best


# ---------------------------
# 3. Utilitaires de validation
# ---------------------------
def is_x_turn(board):
    """Vérifie si c'est au tour de X de jouer[cite: 22]."""
    return board.count("X") == board.count("O")


def encode(board):
    """Encode le plateau en 18 features binaires (ci_x, ci_o)[cite: 16, 19]."""
    features = []
    for cell in board:
        features.append(1 if cell == "X" else 0)  # ci_x
        features.append(1 if cell == "O" else 0)  # ci_o
    return features


# ---------------------------
# 4. Génération du Dataset
# ---------------------------
def generate_dataset():
    dataset = []
    seen_states = set()  # Indispensable pour éviter les doublons dans le CSV

    def explore(board):
        state_tuple = tuple(board)
        if state_tuple in seen_states:
            return

        # On ne traite que les états non-terminaux pour le tour de X [cite: 41, 48]
        current_winner = check_winner(board)

        if current_winner is None and is_x_turn(board):
            # Appel Minimax pour obtenir l'outcome théorique [cite: 41, 48]
            score = minimax(board, True)

            # Cibles demandées [cite: 21, 49]
            x_wins = 1 if score == 1 else 0
            is_draw = 1 if score == 0 else 0

            features = encode(board)
            dataset.append(features + [x_wins, is_draw])
            seen_states.add(state_tuple)

        # Si la partie n'est pas finie, on continue l'exploration récursive
        if current_winner is None:
            for i in range(9):
                if board[i] == "":
                    board[i] = "X" if is_x_turn(board) else "O"
                    explore(board)
                    board[i] = ""

    print("Génération des états en cours (cela peut prendre une minute)...")
    explore([""] * 9)

    # Création des noms de colonnes selon le format spécifié
    columns = []
    for i in range(9):
        columns.append(f"c{i}_x")
        columns.append(f"c{i}_o")
    columns += ["x_wins", "is_draw"]

    # Création du dossier et export [cite: 50, 84]
    df = pd.DataFrame(dataset, columns=columns)
    if not os.path.exists('ressources'):
        os.makedirs('ressources')

    df.to_csv("ressources/dataset.csv", index=False)
    print(f"Succès ! Dataset généré avec {len(df)} états uniques dans ressources/dataset.csv")


if __name__ == "__main__":
    generate_dataset()