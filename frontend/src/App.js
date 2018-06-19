import React, { Component } from 'react';
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
                height: '1.7em',
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

class MakeNew extends Component {
    constructor(props) {
        super(props);
        this.frontInput = React.createRef();
        this.backInput = React.createRef();
    }
    handleClick() {
        const front = this.frontInput.current.value;
        const back = this.backInput.current.value;
        if (front.length === 0 || back.length === 0) {
            console.error('empty');
        }
        this.props.onSubmit({ front, back });
    }
    render() {
        return <div style={{
            border: '1px solid black',
            padding: '20px',
            margin: '20px',
            width: '500px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start'
        }}>
            Front
            <input ref={this.frontInput}  style={{
                width: '100%',
                height: '10em'
            }} />
            <div style={{ height: '1em' }} />
            Back
            <input ref={this.backInput} style={{
                width: '100%',
                height: '10em'
            }} />
            <div style={{ height: '1em' }} />
            <button onClick={this.handleClick.bind(this)}>submit</button>
        </div>
    }
}

class SubmitManager extends Component {
    handleSubmit(s) {
        console.log(s);
    }
    render() {
        return <MakeNew onSubmit={this.handleSubmit.bind(this)} />
    }
}

class ReviewManager extends Component {
    render() {
        return <Card front="f" back="b">
            <Option front="Again" top="soon"/>
            <Option front="Hard" top="1 hour"/>
            <Option front="Good" top="1 day"/>
            <Option front="Easy" top="1 year"/>
        </Card>
    }
}

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
        <button onClick={this.handleToggleMode.bind(this)}>flip</button>
        <div style={{
            display: 'flex',
            width: '100%',
            height: '60%',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
        }}>
            { this.state.reviewing ? <ReviewManager /> : <SubmitManager /> }
        </div>
      </div>
    );
  }
}

export default App;
