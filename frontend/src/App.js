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
        console.log(this.props);
        return <div style={{
            border: '1px solid black',
            padding: '20px',
            margin: '20px',
            width: '500px',
        }}>
            <pre>{/*JSON.stringify(this.props)*/}</pre>
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
    handleClick() {
        this.props.onClick(this.props.ease);
    }
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
        <button onClick={this.props.onClick} style={{
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

class NewCardManager extends Component {
    constructor(props) {
        super(props);
        this.state = {
            number: 0,
        }
    }
    handleSubmit(s) {
        fetch('http://localhost:5000/cards', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(s),
        }).then(response => {
            this.setState({
                number: this.state.number + 1,
            });
        });
    }
    render() {
        return <MakeNew key={this.state.number} onSubmit={this.handleSubmit.bind(this)} />
    }
}

class ReviewManager extends Component {
    constructor(props) {
        super(props);
        this.state = {
            uuid: '',
            front: '',
            back: '',
            type: null,
            hypothetical_next_dues: [],
      };
    }
    handleClick(ease) {
        console.log('ease=', ease);
        fetch('http://localhost:5000/do_rep', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'uuid': this.state.uuid,
                'ease': ease,
            }),
        }).then(response => {
            console.log('response=', response);
            // todo: don't do this
            window.location.reload();
        });
    }
    componentDidMount() {
        fetch('http://localhost:5000/review').then(response => {
            response.json().then(response => {
                if (!response) return;
                this.setState({
                    uuid: response.uuid,
                    front: response.front,
                    back: response.back,
                    type: response.type,
                    hypothetical_next_dues: response.hypothetical_next_dues,
                })
            })
        });
    }
    shouldDisplay1() {
        return this.state.type === 2;
    }
    render() {
        if (this.state.uuid === '') {
            return <div>Nothing to review</div>
        }
        return <Card
            front={this.state.front}
            back={this.state.back}
            type={this.state.type}
        >
            <Option onClick={this.handleClick.bind(this, 0)} front="Again" top={this.state.hypothetical_next_dues[0]}/>
            {this.shouldDisplay1() ? <Option onClick={this.handleClick.bind(this, 1)} front="Hard" top={this.state.hypothetical_next_dues[1]}/> : null}
            <Option onClick={this.handleClick.bind(this, 2)} front="Good" top={this.state.hypothetical_next_dues[2]}/>
            <Option onClick={this.handleClick.bind(this, 3)} front="Easy" top={this.state.hypothetical_next_dues[3]}/>
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
        <button style={{
            marginTop: '3em',
        }} onClick={this.handleToggleMode.bind(this)}>{
            this.state.reviewing ? "add cards" : "review"}</button>
        <div style={{
            display: 'flex',
            width: '100%',
            height: '60%',
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
