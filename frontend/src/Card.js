import React, { Component } from 'react';

export default class Card extends Component {
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
