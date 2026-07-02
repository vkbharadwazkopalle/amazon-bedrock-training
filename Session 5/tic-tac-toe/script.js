// Tic‑Tac‑Toe game logic with sound effects
const boardElement = document.getElementById('game');
const statusElement = document.getElementById('status');
const resetButton = document.getElementById('reset');

const EMPTY = '';
const PLAYER_X = 'X';
const PLAYER_O = 'O';

// Audio setup
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playTone(frequency, duration) {
  const oscillator = audioCtx.createOscillator();
  const gainNode = audioCtx.createGain();
  oscillator.frequency.value = frequency;
  oscillator.type = 'sine';
  oscillator.connect(gainNode);
  gainNode.connect(audioCtx.destination);
  oscillator.start();
  oscillator.stop(audioCtx.currentTime + duration / 1000);
}

function playClick() {
  playTone(300, 100); // short click
}

function playWin() {
  // simple ascending tone
  const notes = [220, 247, 262, 294, 330, 349, 392];
  let time = audioCtx.currentTime;
  notes.forEach(freq => {
    const osc = audioCtx.createOscillator();
    osc.frequency.value = freq;
    osc.type = 'sine';
    osc.connect(audioCtx.destination);
    osc.start(time);
    osc.stop(time + 0.3);
    time += 0.3;
  });
}

class TicTacToe {
  constructor() {
    this.board = Array(9).fill(EMPTY);
    this.currentPlayer = PLAYER_X;
    this.gameOver = false;
    this.initBoard();
    this.updateStatus();
  }

  initBoard() {
    boardElement.innerHTML = '';
    this.board.forEach((cell, idx) => {
      const div = document.createElement('div');
      div.className = 'cell';
      div.dataset.index = idx;
      div.addEventListener('click', () => this.handleCellClick(idx));
      boardElement.appendChild(div);
    });
  }

  handleCellClick(index) {
    if (this.gameOver || this.board[index] !== EMPTY) return;
    this.board[index] = this.currentPlayer;
    playClick();
    this.renderBoard();
    if (this.checkWinner(this.currentPlayer)) {
      this.gameOver = true;
      statusElement.textContent = `${this.currentPlayer} wins!`;
      playWin();
    } else if (this.board.every(cell => cell !== EMPTY)) {
      this.gameOver = true;
      statusElement.textContent = 'Draw!';
    } else {
      this.currentPlayer = this.currentPlayer === PLAYER_X ? PLAYER_O : PLAYER_X;
      this.updateStatus();
    }
  }

  renderBoard() {
    const cells = boardElement.querySelectorAll('.cell');
    this.board.forEach((value, idx) => {
      cells[idx].textContent = value;
    });
  }

  updateStatus() {
    statusElement.textContent = `Turn: ${this.currentPlayer}`;
  }

  checkWinner(player) {
    const winPatterns = [
      [0,1,2], [3,4,5], [6,7,8],
      [0,3,6], [1,4,7], [2,5,8],
      [0,4,8], [2,4,6]
    ];
    return winPatterns.some(pattern =>
      pattern.every(idx => this.board[idx] === player)
    );
  }

  reset() {
    this.board = Array(9).fill(EMPTY);
    this.currentPlayer = PLAYER_X;
    this.gameOver = false;
    this.initBoard();
    this.updateStatus();
  }
}

const game = new TicTacToe();
resetButton.addEventListener('click', () => game.reset());