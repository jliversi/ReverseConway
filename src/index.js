import Game from './game.js'

const { x, y } = {
  x: 9,
  y: 23
}

const game = new Game(x,y,document.getElementById('board'));

document.getElementById('start').addEventListener('click', e => {
  game.run(50);
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


