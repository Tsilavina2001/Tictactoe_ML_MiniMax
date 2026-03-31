const board = document.getElementById("board");
const statusText = document.getElementById("status");
const resetBtn = document.getElementById("resetBtn");

let cells = [];
let currentPlayer = "X";
let gameActive = true;

// const winPatterns = [
//   [0,1,2], [3,4,5], [6,7,8],
//   [0,3,6], [1,4,7], [2,5,8],
//   [0,4,8], [2,4,6]
// ];

function createBoard() {
  board.innerHTML = "";
  cells = [];

  for (let i = 0; i < 9; i++) {
    const cell = document.createElement("div");
    cell.classList.add("cell");
    cell.addEventListener("click", () => handleClick(i));
    board.appendChild(cell);
    cells.push(cell);
  }
}

function handleClick(index) {
  if (!gameActive || cells[index].textContent !== "") return;

  cells[index].textContent = currentPlayer;

//   if (checkWin()) {
//     statusText.textContent = ` Joueur ${currentPlayer} a gagné !`;
//     gameActive = false;
//     return;
//   }

//   if (cells.every(cell => cell.textContent !== "")) {
//     statusText.textContent = "Match nul ";
//     gameActive = false;
//     return;
//   }
  getEtat()
  currentPlayer = currentPlayer === "X" ? "O" : "X";
  statusText.textContent = `Tour du joueur ${currentPlayer}`;
}

// function checkWin() {
//   return winPatterns.some(pattern => {
//     return pattern.every(index => {
//       return cells[index].textContent === currentPlayer;
//     });
//   });
// }
const getEtat = ()=>{
    const etat = []
    for (let index = 0; index < board.children.length; index++) {
        etat.push(board.children[index].textContent)
    }
    console.log(etat);
    
    
}
function resetGame() {
  currentPlayer = "X";
  gameActive = true;
  statusText.textContent = "Tour du joueur X";
  createBoard();
}

resetBtn.addEventListener("click", resetGame);

// Initialisation
createBoard();