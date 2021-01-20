import Game from './game.js'
import * as PATTERNS from './inputs_patterns.js';
import { transpose } from './util.js';

const startingPattern = transpose(PATTERNS.python);

const { x, y } = {
  x: startingPattern[0].length,
  y: startingPattern.length
}

const game = new Game(x,y,document.getElementById('board'),startingPattern);


const start = document.getElementById('start');
const stop = document.getElementById('stop');
start.addEventListener('click', e => {
  start.disabled = true;
  stop.disabled = false;
  game.run();
})

stop.addEventListener('click', e => {
  stop.disabled = true;
  start.disabled = false;
  game.stop();
})

document.getElementById('one-step').addEventListener('click', e => {
  if (game.running) {
    game.stop();
    game.runRound();
    game.renderScrollX();
    game.run();
  } else {
    game.runRound();
    game.renderScrollX();
  }
})

document.getElementById('clear').addEventListener('click', e => {
  game.stop();
  stop.disabled = true;
  start.disabled = false;
  game.clearBoard();
})

const slow = document.getElementById('slow');
const fast = document.getElementById('fast');

slow.addEventListener('click', e => {
  slow.disabled = true;
  fast.disabled = false;
  game.changeSpeed(1000);
})
fast.addEventListener('click', e => {
  fast.disabled = true;
  slow.disabled = false;
  game.changeSpeed(600);
})

document.getElementById('js').addEventListener('click', e => {
  start.disabled = true;
  stop.disabled = false;
  const jsPattern = transpose(PATTERNS.js);
  game.switchPatterns(jsPattern);
})
document.getElementById('python').addEventListener('click', e => {
  start.disabled = true;
  stop.disabled = false;
  const pythonPattern = transpose(PATTERNS.python);
  game.switchPatterns(pythonPattern);
})
document.getElementById('react').addEventListener('click', e => {
  start.disabled = true;
  stop.disabled = false;
  const reactPattern = transpose(PATTERNS.react);
  game.switchPatterns(reactPattern);
})
document.getElementById('ruby').addEventListener('click', e => {
  start.disabled = true;
  stop.disabled = false;
  const rubyPattern = transpose(PATTERNS.ruby);
  game.switchPatterns(rubyPattern);
})
document.getElementById('sql').addEventListener('click', e => {
  start.disabled = true;
  stop.disabled = false;
  const sqlPattern = transpose(PATTERNS.sql);
  game.switchPatterns(sqlPattern);
})
document.getElementById('rails').addEventListener('click', e => {
  start.disabled = true;
  stop.disabled = false;
  const railsPattern = transpose(PATTERNS.rails);
  game.switchPatterns(railsPattern);
})
