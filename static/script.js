const boardElement = document.getElementById("board");
const statusText = document.getElementById("status");
const resetBtn = document.getElementById("resetBtn");
const modeSelect = document.getElementById("modeSelect"); // Ajoute un <select> dans ton HTML

let cells = [];
let gameActive = true;
let currentPlayer = "O"; // L'humain commence souvent par O, l'IA est X

function createBoard() {
    boardElement.innerHTML = "";
    cells = [];
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement("div");
        cell.classList.add("cell");
        cell.addEventListener("click", () => handleHumanClick(i));
        boardElement.appendChild(cell);
        cells.push(cell);
    }
}

// Récupère l'état actuel du plateau pour l'envoyer au Python
function getBoardState() {
    return cells.map(cell => cell.textContent);
}

async function handleHumanClick(index) {
    if (!gameActive || cells[index].textContent !== "") return;

    const mode = document.getElementById("modeSelect").value;

    if (mode === "human") {
        // Logique classique entre deux humains
        cells[index].textContent = currentPlayer;
        if (checkGameOver()) return;
        currentPlayer = currentPlayer === "X" ? "O" : "X";
        statusText.textContent = `Tour du joueur ${currentPlayer}`;
    } else {
        // Logique vs IA (Humain est toujours O, IA est X)
        if (currentPlayer !== "O") return;

        cells[index].textContent = "O";
        if (checkGameOver()) return;

        currentPlayer = "X";
        statusText.textContent = "L'IA réfléchit...";
        await makeAIMove();
    }
}

async function makeAIMove() {
    const currentBoard = getBoardState();
    const mode = modeSelect.value; // "ml" ou "hybride"

    // On choisit la route selon le mode sélectionné
    const route = mode === "hybride" ? "/predict_hybrid" : "/predict_ml";

    try {
        const response = await fetch(`http://localhost:5000${route}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board: currentBoard })
        });

        const data = await response.json();
        const move = data.move;

        if (move !== -1) {
            cells[move].textContent = "X";
            cells[move].classList.add("x-mark");

            if (!checkGameOver()) {
                currentPlayer = "O";
                statusText.textContent = "À vous de jouer (O)";
            }
        }
    } catch (error) {
        console.error("Erreur de connexion au serveur Flask :", error);
        statusText.textContent = "Erreur: Serveur Python non lancé";
    }
}

// Fonction de vérification locale pour arrêter le jeu
function checkGameOver() {
    const board = getBoardState();
    const winPatterns = [
        [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]
    ];

    for (let pattern of winPatterns) {
        const [a, b, c] = pattern;
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            statusText.textContent = `Le joueur ${board[a]} a gagné !`;
            gameActive = false;
            return true;
        }
    }

    if (!board.includes("")) {
        statusText.textContent = "Match nul !";
        gameActive = false;
        return true;
    }
    return false;
}

resetBtn.addEventListener("click", () => {
    gameActive = true;
    currentPlayer = "O";
    statusText.textContent = "À vous de jouer (O)";
    createBoard();
});

createBoard();