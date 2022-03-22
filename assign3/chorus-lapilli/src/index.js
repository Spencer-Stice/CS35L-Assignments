import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
function Square(props){
    return (
	    <button className="square" onClick={props.onClick}>
	    {props.value}
	</button>
    );
}

class Board extends React.Component {
    constructor(props){
	super(props);
	this.state = {
	    squares: Array(9).fill(null),
	    xIsNext: true,
	    threeX: false,
	    threeO: false,
	    xNum: 0,
	    oNum: 0,
	    prevSpot: null,
	    nextSpot: 0,
	};
    }

    handleClick(i){
	const squares = this.state.squares.slice();
	if(calculateWinner(squares) != null)
	    return;
	if ((this.state.xIsNext && this.state.threeX) || (!this.state.xIsNext && this.state.threeO) || calculateWinner(squares)){
	    if(squares[i] && this.state.threeX && this.state.threeO){
		if(squares[i] == 'X' && !this.state.xIsNext)
		    return;
		if(squares[i] == 'O' && this.state.xIsNext)
		    return;
		this.setState({
		    prevSpot: i
		});
	    }
	    else if(this.state.prevSpot != null && this.state.threeX && this.state.threeO){
		if(squares[i])
		    return;
		if((this.state.xIsNext && squares[4] == 'X') || (!this.state.xIsNext && squares[4] == 'O')){
		    squares[i] = this.state.xIsNext ? 'X' : 'O';
		    squares[this.state.prevSpot] = null;
		    if((!calculateWinner(squares) && this.state.prevSpot != 4)){
			squares[i] = null;
			squares[this.state.prevSpot] = this.state.xIsNext ? 'X' : 'O';
			return;
		    }
		}
		if(this.state.prevSpot == 0 && (i != 1 && i != 3 && i != 4)){
		    return;
		}
		if(this.state.prevSpot == 1 && (i != 0 && i != 2 && i != 3 && i != 4 && i != 5)){
		    return;
		}
		if(this.state.prevSpot == 2 && (i != 1 && i != 4 && i != 5)){
		    return;
		}
		if(this.state.prevSpot == 3 && (i != 0 && i != 4 && i != 6 && i != 1 && i != 7)){
		    return;
		}
		if(this.state.prevSpot == 5 && (i != 1 && i != 2 && i != 4 && i != 7 && i != 8)){
		    return;
		}
		if(this.state.prevSpot == 6 && (i != 3 && i != 4 && i != 7)){
		    return;
		}
		if(this.state.prevSpot == 7 && (i != 6 && i != 3 && i != 4 && i != 5 && i != 8)){
		    return;
		}
		if(this.state.prevSpot == 8 && (i != 7 && i != 4 && i != 5)){
		    return;
		}
		squares[i] = this.state.xIsNext ? 'X' : 'O';
		squares[this.state.prevSpot] = null;
		this.setState({
		    xIsNext: !this.state.xIsNext,
		    prevSpot: null
		})
	    }
	    this.setState({
		squares: squares
	    })
	    return;
	}
	if(squares[i] == 'X' || squares[i] == 'O')
	    return;
	squares[i] = this.state.xIsNext ? 'X' : 'O';
	if(this.state.xIsNext){
	    this.setState({
		xNum: this.state.xNum + 1
	    });
	    if(this.state.xNum == 2)
		this.setState({
		    threeX: true
		});
	}
	else{
	    this.setState({
		oNum: this.state.oNum + 1
	    });
	    if(this.state.oNum == 2)
		this.setState({
		    threeO: true,
		    xIsNext: !this.state.xIsNext
		});
	}
	if(!this.state.threeX && !this.state.threeO){
	this.setState({
	    squares: squares,
	    xIsNext: !this.state.xIsNext,
	});
	}
	this.setState({
	    squares: squares
	});
    }
    renderSquare(i) {
	return (<Square
       	value={this.state.squares[i]}
	onClick={() => this.handleClick(i)}
	    />
	);
    }

    render() {
	const winner = calculateWinner(this.state.squares);
	let status;
	if (winner) {
	    status = 'Winner: ' + winner;
	} else {
	    status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
	}

    return (
      <div>
        <div className="status">{status}</div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  render() {
    return (
      <div className="game">
        <div className="game-board">
          <Board />
        </div>
        <div className="game-info">
          <div>{/* status */}</div>
          <ol>{/* TODO */}</ol>
        </div>
      </div>
    );
  }
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);
