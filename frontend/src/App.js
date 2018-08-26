import React, { Component } from 'react';

import NewCardManager from './NewCardManager.js';
import ReviewManager from './ReviewManager.js';

import './App.css';

class App extends Component {
  constructor(props) {
      super(props);
      this.state = {
          reviewing: true,
      };
  }
  handleToggleMode() {
      this.setState({
          reviewing: !this.state.reviewing,
      });
  }
  render() {
    return (
      <div className="App" style={{
          height: '100vh',
      }}>
        <header className="App-header">
          <h1 className="App-title">LSTM</h1>
        </header>
        <button style={{
            marginTop: '3em',
        }} onClick={this.handleToggleMode.bind(this)}>{
            this.state.reviewing ? "add cards" : "review"}</button>
        <div style={{
            display: 'flex',
            width: '100%',
            height: '70%',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
        }}>
            { this.state.reviewing ? <ReviewManager /> : <NewCardManager /> }
        </div>
      </div>
    );
  }
}

export default App;
