import React, { Component } from 'react';

import Card from './Card.js';
import Option from './Option.js';

export default class ReviewManager extends Component {
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
        return <div>
        <Card
            front={this.state.front}
            back={this.state.back}
            type={this.state.type}
        >
            <Option onClick={this.handleClick.bind(this, 0)} front="Again" top={this.state.hypothetical_next_dues[0]}/>
            {this.shouldDisplay1() ? <Option onClick={this.handleClick.bind(this, 1)} front="Hard" top={this.state.hypothetical_next_dues[1]}/> : null}
            <Option onClick={this.handleClick.bind(this, 2)} front="Good" top={this.state.hypothetical_next_dues[2]}/>
            <Option onClick={this.handleClick.bind(this, 3)} front="Easy" top={this.state.hypothetical_next_dues[3]}/>
        </Card>
        <pre style={{maxWidth: '80em', textAlign: 'left' }}>{JSON.stringify(this.state, null, 2)}</pre>
        </div>
    }
}
