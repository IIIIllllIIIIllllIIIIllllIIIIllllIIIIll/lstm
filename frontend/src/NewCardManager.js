import React, { Component } from 'react';

import MakeNew from './MakeNew.js';

export default class NewCardManager extends Component {
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
