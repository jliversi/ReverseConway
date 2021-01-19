!function(t){var e={};function r(s){if(e[s])return e[s].exports;var n=e[s]={i:s,l:!1,exports:{}};return t[s].call(n.exports,n,n.exports,r),n.l=!0,n.exports}r.m=t,r.c=e,r.d=function(t,e,s){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:s})},r.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var s=Object.create(null);if(r.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)r.d(s,n,function(e){return t[e]}.bind(null,n));return s},r.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="",r(r.s=0)}([function(t,e,r){"use strict";r.r(e);const s=[[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]];var n=class{constructor(t,e,r,s){this.DIM_X=t,this.DIM_Y=e,this.board=Array.from({length:e},()=>Array.from({length:t},()=>!1)),this.ele=r,this.buildBoard(s),this.setupListeners()}buildBoard(t){const e=this.ele;this.eleArr=[];for(let r=0;r<this.DIM_Y;r++){const s=document.createElement("tr"),n=[];s.id=r,s.classList.add("row");for(let e=0;e<this.DIM_X;e++){const o=document.createElement("td");o.id=`${e},${r}`,t&&t[r][e]?(this.board[r][e]=!0,o.classList.add("cell","on")):o.classList.add("cell","off"),(r<2||e<2||r>this.DIM_Y-3||e>this.DIM_X-3)&&o.classList.add("edge"),s.appendChild(o),n.push(o)}e.appendChild(s),this.eleArr.push(n)}}setupListeners(){for(let t=0;t<this.eleArr.length;t++)for(let e=0;e<this.eleArr[0].length;e++){const r=this.eleArr[t][e],s=s=>{this.board[t]&&this.board[t][e]?(this.board[t][e]=!1,r.classList.add("off"),r.classList.remove("on")):(this.board[t][e]=!0,r.classList.add("on"),r.classList.remove("off"))};r.addEventListener("mousedown",s);const n=s=>{1!=s.buttons&&3!=s.buttons||(this.board[t]&&this.board[t][e]?(this.board[t][e]=!1,r.classList.add("off"),r.classList.remove("on")):(this.board[t][e]=!0,r.classList.add("on"),r.classList.remove("off")))};r.addEventListener("mouseover",n)}}neighborCoords(t,e){const r=s.map(([r,s])=>[t+r,e+s]);for(let t=0;t<r.length;t++){const e=r[t];e[0]==this.DIM_X?e[0]=0:e[0]<0&&(e[0]=this.DIM_X-1),e[1]==this.DIM_Y?e[1]=0:e[1]<0&&(e[1]=this.DIM_Y-1)}return r}numOnNeighbors(t,e){const r=this.neighborCoords(t,e);let s=0;for(let t=0;t<r.length;t++){const[e,n]=r[t];this.board[n]&&this.board[n][e]&&(s+=1)}return s}runRound(){const t=[],e=[];for(let r=0;r<this.board.length;r++)for(let s=0;s<this.board[0].length;s++){const n=this.numOnNeighbors(s,r);this.board[r][s]?(n<2||n>3)&&e.push([r,s]):3===n&&t.push([r,s])}t.forEach(([t,e])=>{this.board[t][e]=!0}),e.forEach(([t,e])=>{this.board[t][e]=!1})}render(){for(let t=0;t<this.board.length;t++)for(let e=0;e<this.board[0].length;e++){const r=this.eleArr[t][e];this.board[t]&&this.board[t][e]?(r.classList.add("on"),r.classList.remove("off")):(r.classList.add("off"),r.classList.remove("on"))}}run(t){this.running||(this.running=!0,this.intId=setInterval(()=>{this.runRound(),this.render()},t))}stop(){clearInterval(this.intId),this.running=!1}};const o=(t=>{const e=[];for(let r=t[0].length-1;r>=0;r--){const s=[];e.push(s);for(let e=0;e<t.length;e++)s.push(t[e][r])}return e})([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,1,1,0],[1,1,1,1,0,0,1,0,0],[0,1,1,1,0,0,1,0,0],[0,0,0,0,0,1,1,1,0],[1,1,0,0,1,0,1,0,0],[0,0,1,0,0,0,0,0,0],[1,0,0,0,1,1,0,1,0],[1,0,1,0,0,0,0,0,0],[1,1,0,1,0,0,0,1,0],[1,0,0,0,0,0,1,1,1],[0,0,1,1,1,0,0,0,1],[1,0,0,0,0,0,1,1,0],[1,1,0,0,0,1,1,0,0],[1,0,1,0,0,1,1,0,1],[0,0,1,0,1,1,0,0,1],[0,0,1,1,0,0,0,0,0],[0,0,0,0,0,1,0,1,0],[0,0,1,1,0,0,0,0,0],[0,0,1,1,0,1,1,0,1],[0,0,0,0,1,1,1,0,1],[0,1,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,1,1,0,0,0]]),{x:i,y:d}={x:o[0].length,y:o.length},l=new n(i,d,document.getElementById("board"),o);l.run(600),document.getElementById("start").addEventListener("click",t=>{l.run(600)}),document.getElementById("stop").addEventListener("click",t=>{l.stop()}),document.getElementById("one-step").addEventListener("click",t=>{l.runRound(),l.render()}),document.getElementById("log-on").addEventListener("click",t=>{const e=[];for(let t=0;t<l.board.length;t++)for(let r=0;r<l.board[0].length;r++)l.board[t][r]&&e.push([r,t]);console.log(e)})}]);