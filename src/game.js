const DIRS = [
  [0,-1],
  [1,-1],
  [1,0],
  [1,1],
  [0,1],
  [-1,1],
  [-1,0],
  [-1,-1]
]

class Game {
  constructor(x,y,ele,inputArr) {
    this.DIM_X = x;
    this.DIM_Y = y;
    this.board = Array.from({ length: y }, () => Array.from({ length: x }, () => false));
    this.ele = ele;

    this.buildBoard(inputArr);
    this.setupListeners();
  }

  buildBoard(inputArr) {
    const table = this.ele;
    this.eleArr = [];
    for (let i = 0; i < this.DIM_Y; i++) {
      const row = document.createElement('tr');
      const eleRow = [];
      row.id = i;
      row.classList.add('row');
      for (let j = 0; j < this.DIM_X; j++) {
        const cell = document.createElement('td');
        cell.id = `${j},${i}`;
        if (inputArr && inputArr[i][j]) {
          this.board[i][j] = true
          cell.classList.add('cell', 'on')
        } else {
          cell.classList.add('cell', 'off')
        }
        if (i == 0 || j == 0 || i == (this.DIM_Y - 1) || j == (this.DIM_X - 1)) {
          cell.classList.add('edge')
        }
        row.appendChild(cell);
        eleRow.push(cell);
      }
      table.appendChild(row);
      this.eleArr.push(eleRow);
    }
  }

  setupListeners() {
    for (let i = 0; i < this.eleArr.length; i++) {
      for (let j = 0; j < this.eleArr[0].length; j++) {
        const ele = this.eleArr[i][j];
        const handleClick = e => {
          if (this.board[i] && this.board[i][j]) {
            this.board[i][j] = false;
            ele.classList.add('off');
            ele.classList.remove('on');
          } else {
            this.board[i][j] = true;
            ele.classList.add('on');
            ele.classList.remove('off');
          }
        }
        ele.addEventListener('mousedown', handleClick);

        const handleMouseover = e => {
          if (e.buttons == 1 || e.buttons == 3) {
            if (this.board[i] && this.board[i][j]) {
              this.board[i][j] = false;
              ele.classList.add('off');
              ele.classList.remove('on');
            } else {
              this.board[i][j] = true;
              ele.classList.add('on');
              ele.classList.remove('off');
            }
          }
        }

        ele.addEventListener('mouseover', handleMouseover);
      }
    }
  }

  neighborCoords(x,y) {
    const nbrArr = DIRS.map(([dx, dy]) => [x + dx, y + dy]);
    for (let i = 0; i < nbrArr.length; i++) {
      const nbr = nbrArr[i];
      if (nbr[0] == this.DIM_X) {
        nbr[0] = 0;
      } else if (nbr[0] < 0) {
        nbr[0] = this.DIM_X - 1;
      } 
      if (nbr[1] == this.DIM_Y) {
        nbr[1] = 0;
      } else if (nbr[1] < 0) {
        nbr[1] = this.DIM_Y - 1;
      }     
    }
    return nbrArr;
  }

  numOnNeighbors(x,y) {
    const nbrs = this.neighborCoords(x,y);
    let count = 0;
    for (let i = 0; i < nbrs.length; i++) {
      const [nbrX, nbrY] = nbrs[i];
      if (this.board[nbrY] && this.board[nbrY][nbrX]) {
        count += 1;
      }
    }
    return count;
  }

  runRound() {
    const toOn = [];
    const toOff = [];
    for (let i = 0; i < this.board.length; i++) {
      for (let j = 0; j < this.board[0].length; j++) {
        const nbrsOn = this.numOnNeighbors(j, i);
        if (this.board[i][j]) {
          if (nbrsOn < 2 || nbrsOn > 3) {
            toOff.push([i,j])
          }
        } else {
          if (nbrsOn === 3) {
            toOn.push([i,j])
          }
        }
      }
    }

    toOn.forEach(([y,x]) => {
      this.board[y][x] = true;
    })
    toOff.forEach(([y,x]) => {
      this.board[y][x] = false;
    })

  }

  render() {
    for (let i = 0; i < this.board.length; i++) {
      for (let j = 0; j < this.board[0].length; j++) {
        const ele = this.eleArr[i][j];
        if (this.board[i] && this.board[i][j]) {
          ele.classList.add('on');
          ele.classList.remove('off');
        } else {
          ele.classList.add('off');
          ele.classList.remove('on');
        }
      }
    }
  }

  run(interval) {
    if (this.running) {
      return;
    }
    this.running = true;
    this.intId = setInterval(() => {
      this.runRound();
      this.render();
    }, interval);
  }

  stop() {
    clearInterval(this.intId);
    this.running = false;
  }
}


export default Game;

