import Game from './game.js'
import * as PATTERNS from './inputs_patterns.js';
import { transpose } from './util.js';

const startingPattern = transpose(PATTERNS.josh_dot_a);

const { x, y } = {
  x: startingPattern[0].length,
  y: startingPattern.length
}

const game = new Game(x,y,document.getElementById('board'),startingPattern);
game.run(600);


document.getElementById('start').addEventListener('click', e => {
  game.run(600);
})

document.getElementById('stop').addEventListener('click', e => {
  game.stop();
})

document.getElementById('one-step').addEventListener('click', e => {
  game.runRound();
  game.render();
})

document.getElementById('log-on').addEventListener('click', e => {
  const on = [];
  for (let i = 0; i < game.board.length; i++) {
    for (let j = 0; j < game.board[0].length; j++) {
      if (game.board[i][j]) {
        on.push([j,i]);
      }
    }
  }
  console.log(on);
})


