/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/game.js":
/*!*********************!*\
  !*** ./src/game.js ***!
  \*********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\nconst DIRS = [\n  [0,-1],\n  [1,-1],\n  [1,0],\n  [1,1],\n  [0,1],\n  [-1,1],\n  [-1,0],\n  [-1,-1]\n]\n\nclass Game {\n  constructor(x,y,ele) {\n    this.DIM_X = x;\n    this.DIM_Y = y;\n    this.board = Array.from({ length: y }, () => Array.from({ length: x }, () => false));\n    this.ele = ele;\n\n    this.buildBoard();\n    this.setupListeners();\n  }\n\n  buildBoard() {\n    const table = this.ele;\n    this.eleArr = [];\n    for (let i = 0; i < this.DIM_Y; i++) {\n      const row = document.createElement('tr');\n      const eleRow = [];\n      row.id = i;\n      row.classList.add('row');\n      for (let j = 0; j < this.DIM_X; j++) {\n        const cell = document.createElement('td');\n        cell.id = `${j},${i}`;\n        cell.classList.add('cell', 'off')\n        row.appendChild(cell);\n        eleRow.push(cell);\n      }\n      table.appendChild(row);\n      this.eleArr.push(eleRow);\n    }\n  }\n\n  setupListeners() {\n    for (let i = 0; i < this.eleArr.length; i++) {\n      for (let j = 0; j < this.eleArr[0].length; j++) {\n        const ele = this.eleArr[i][j];\n        const handleClick = e => {\n          if (this.board[i] && this.board[i][j]) {\n            this.board[i][j] = false;\n            ele.classList.add('off');\n            ele.classList.remove('on');\n          } else {\n            this.board[i][j] = true;\n            ele.classList.add('on');\n            ele.classList.remove('off');\n          }\n        }\n        ele.addEventListener('mousedown', handleClick);\n\n        const handleMouseover = e => {\n          if (e.buttons == 1 || e.buttons == 3) {\n            if (this.board[i] && this.board[i][j]) {\n              this.board[i][j] = false;\n              ele.classList.add('off');\n              ele.classList.remove('on');\n            } else {\n              this.board[i][j] = true;\n              ele.classList.add('on');\n              ele.classList.remove('off');\n            }\n          }\n        }\n\n        ele.addEventListener('mouseover', handleMouseover);\n      }\n    }\n  }\n\n  neighborCoords(x,y) {\n    const nbrArr = DIRS.map(([dx, dy]) => [x + dx, y + dy]);\n    for (let i = 0; i < nbrArr.length; i++) {\n      const nbr = nbrArr[i];\n      if (nbr[0] == this.DIM_X) {\n        nbr[0] = 0;\n      } else if (nbr[0] < 0) {\n        nbr[0] = this.DIM_X - 1;\n      } \n      if (nbr[1] == this.DIM_Y) {\n        nbr[1] = 0;\n      } else if (nbr[1] < 0) {\n        nbr[1] = this.DIM_Y - 1;\n      }     \n    }\n    return nbrArr;\n  }\n\n  numOnNeighbors(x,y) {\n    const nbrs = this.neighborCoords(x,y);\n    let count = 0;\n    for (let i = 0; i < nbrs.length; i++) {\n      const [nbrX, nbrY] = nbrs[i];\n      if (this.board[nbrY] && this.board[nbrY][nbrX]) {\n        count += 1;\n      }\n    }\n    return count;\n  }\n\n  runRound() {\n    const toOn = [];\n    const toOff = [];\n    for (let i = 0; i < this.board.length; i++) {\n      for (let j = 0; j < this.board[0].length; j++) {\n        const nbrsOn = this.numOnNeighbors(j, i);\n        if (this.board[i][j]) {\n          if (nbrsOn < 2 || nbrsOn > 3) {\n            toOff.push([i,j])\n          }\n        } else {\n          if (nbrsOn === 3) {\n            toOn.push([i,j])\n          }\n        }\n      }\n    }\n\n    toOn.forEach(([y,x]) => {\n      this.board[y][x] = true;\n    })\n    toOff.forEach(([y,x]) => {\n      this.board[y][x] = false;\n    })\n\n  }\n\n  render() {\n    for (let i = 0; i < this.board.length; i++) {\n      for (let j = 0; j < this.board[0].length; j++) {\n        const ele = this.eleArr[i][j];\n        if (this.board[i] && this.board[i][j]) {\n          ele.classList.add('on');\n          ele.classList.remove('off');\n        } else {\n          ele.classList.add('off');\n          ele.classList.remove('on');\n        }\n      }\n    }\n  }\n\n  run(interval) {\n    if (this.running) {\n      return;\n    }\n    this.running = true;\n    this.intId = setInterval(() => {\n      this.runRound();\n      this.render();\n    }, interval);\n  }\n\n  stop() {\n    clearInterval(this.intId);\n    this.running = false;\n  }\n}\n\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (Game);\n\n//# sourceURL=webpack:///./src/game.js?");

/***/ }),

/***/ "./src/index.js":
/*!**********************!*\
  !*** ./src/index.js ***!
  \**********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _game_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./game.js */ \"./src/game.js\");\n\n\nconst { x, y } = {\n  x: 50,\n  y: 8\n}\n\nconst game = new _game_js__WEBPACK_IMPORTED_MODULE_0__[\"default\"](x,y,document.getElementById('board'));\n\ndocument.getElementById('start').addEventListener('click', e => {\n  game.run(50);\n})\n\ndocument.getElementById('stop').addEventListener('click', e => {\n  game.stop();\n})\n\ndocument.getElementById('one-step').addEventListener('click', e => {\n  game.runRound();\n  game.render();\n})\n\ndocument.getElementById('log-on').addEventListener('click', e => {\n  const on = [];\n  for (let i = 0; i < game.board.length; i++) {\n    for (let j = 0; j < game.board[0].length; j++) {\n      if (game.board[i][j]) {\n        on.push([j,i]);\n      }\n    }\n  }\n  console.log(on);\n})\n\n\n\n\n//# sourceURL=webpack:///./src/index.js?");

/***/ })

/******/ });