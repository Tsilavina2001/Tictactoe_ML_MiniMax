import pandas as pd
import os

# ---------------------------
# 1. Vérification du gagnant
# ---------------------------
def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for line in wins:
        if board[line[0]] != "" and all(board[i] == board[line[0]] for i in line):
            return board[line[0]]

    if "" not in board:
        return "draw"

    return None


# ---------------------------
# 2. Validation d'état
# ---------------------------
def is_valid(board):
    x = board.count("X")
    o = board.count("O")

    # X commence toujours
    if o > x or x - o > 1:
        return False

    winner = check_winner(board)

    # Cohérence gagnant
    if winner == "X" and x == o:
        return False
    if winner == "O" and x > o:
        return False

    return True


def is_x_turn(board):
    return board.count("X") == board.count("O")


# ---------------------------
# 3. Minimax + Alpha-Bêta
# ---------------------------
def minimax(board, is_maximizing, alpha=-float('inf'), beta=float('inf')):
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
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, True, alpha, beta)
                board[i] = ""
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


# ---------------------------
# 4. Encodage
# ---------------------------
def encode(board):
    features = []
    for cell in board:
        features.append(1 if cell == "X" else 0)
        features.append(1 if cell == "O" else 0)
    return features


# ---------------------------
# 5. Génération dataset
# ---------------------------
def generate_dataset():
    dataset = []
    seen_states = set()

    def explore(board):
        state_tuple = tuple(board)

        if state_tuple in seen_states:
            return

        if not is_valid(board):
            return

        seen_states.add(state_tuple)

        winner = check_winner(board)

        # 👉 IMPORTANT : on prend TOUS les états où c'est au tour de X
        if is_x_turn(board):

            if winner is None:
                score = minimax(board, True)
            else:
                score = 1 if winner == "X" else -1 if winner == "O" else 0

            x_wins = 1 if score == 1 else 0
            is_draw = 1 if score == 0 else 0

            dataset.append(encode(board) + [x_wins, is_draw])

        # 👉 Continuer seulement si pas terminal
        if winner is None:
            for i in range(9):
                if board[i] == "":
                    board[i] = "X" if is_x_turn(board) else "O"
                    explore(board)
                    board[i] = ""

    print("Génération en cours...")
    explore([""] * 9)

    # Colonnes
    columns = []
    for i in range(9):
        columns.append(f"c{i}_x")
        columns.append(f"c{i}_o")
    columns += ["x_wins", "is_draw"]

    df = pd.DataFrame(dataset, columns=columns)

    # Dossier
    if not os.path.exists("ressources"):
        os.makedirs("ressources")

    df.to_csv("ressources/dataset.csv", index=False)

    print(f"✅ Dataset généré : {len(df)} états")


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    generate_dataset()