import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class Card extends Component {
    constructor(props) {
        super(props);
        this.state = {
            flipped: false,
        }
    }
    handleFlip(e) {
        this.setState({
            flipped: true,
        });
    }
    render() {
        return <div style={{
            border: '1px solid black',
            padding: '20px',
            margin: '20px',
            width: '500px',
        }}>
            <div><h1>{this.props.front}</h1></div>

            {/*not flipped*/}

            <div style={{
                visibility: this.state.flipped ? 'visible' : 'hidden',
            }}><hr /><h1>{this.props.back}</h1></div>

            <div style={{
                height: '2em',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'flex-end'
            }}>
            {!this.state.flipped
                ? <div style={{
                    verticalAlign: 'bottom',
                    width: "100%",
                }} onClick={this.handleFlip.bind(this)}>
                <button style={{width: '12em'}}>flip</button></div>
                : this.props.children
            }
            </div>
        </div>
    }
}

class Option extends Component {
    render() {
        return <div style={{
            display: "inline-flex",
            flexDirection: "column",
        }}>
        <div style={{
            fontSize: '0.6em'
        }}>
        {this.props.top}
        </div>
        <button style={{
            width: '6em',
            marginLeft: '0.15em',
            marginRight: '0.15em',
        }}>{this.props.front}</button>
        </div>
    }
}

class App extends Component {
  handleChooseOption(x) {
      console.log(x);
  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">LSTM</h1>
        </header>
        <div style={{
            display: 'flex',
            width: '100%',
            alignItems: 'center',
            flexDirection: 'column',
        }}>
            <Card front="f" back="b">
                <Option front="Again" top="soon"/>
                <Option front="Hard" top="1 hour"/>
                <Option front="Good" top="1 day"/>
                <Option front="Easy" top="1 year"/>
            </Card>
        </div>
      </div>
    );
  }
}

export default App;
